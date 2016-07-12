# -*- coding: utf-8 -*-
"""
Created on Mon Feb 08 10:41:35 2016

@author: s0568630

‘Swiss army knife’ module. Contains functions to:
-Load and manipulate network data.
-perform list manipulation for hill climber algorithms.
-convert routes to Point2D objects and Polyline objects

"""

import math
import csv
import random
import numpy as np
from Points import Point2D
from Polylines import Polyline
import unittest

#------------------------------------------------------------------------------
def load_Locations(fname):
    """Method takes CSV filename as argument, shoudl be in form country,
    city,latlong where latlong is in degrees and minutes.
    Returns list of lists, with each item of the primary list being 
    a list: [cityname, latitude, longitude,......]. """
    
    print 'Opening file:',fname
    
    f=open(fname,"r")
    allrows=[]

    for row in csv.reader(f):
        allrows.append(row)
    f.close()
    
    placeInfo=[]
    #Cut off header and select all other rows
    for row in allrows[1:]:
        country=row[0] #country is in first column
        city=row[1]    #city name is in second column
        locations=row[2].split() #latlong in 3rd column. split by space
        latstuff = locations[0].split("\xb0")
        #print 'latstuff is: ',latstuff
        lngstuff = locations[1].split("\xb0")
        #print 'longstuff is: ',lngstuff
        
        latdeg=int(latstuff[0])
        #print 'latdeg is: ',latdeg
        lngdeg=int(lngstuff[0])
        #print 'lngdeg is: ',lngdeg
        
        latstuff=latstuff[1].split("'")
        lngstuff=lngstuff[1].split("'")
    
        latdeg=latdeg+(int(latstuff[0])/60.)
        #print 'latdeg is now: ',latdeg
        lngdeg=lngdeg+(int(lngstuff[0])/60.)
        #print 'lngdeg is now: ',lngdeg

        if latstuff[1]=='S':
            latdeg = latdeg*-1
        if lngstuff[1] == 'W':
            lngdeg = lngdeg*-1
            
        info=[city, latdeg, lngdeg, country]                
        placeInfo.append(info)
            
    return placeInfo
    
#------------------------------------------------------------------------------    
def load_distance_matrix(fname):
    print 'Opening File:',fname
    f=open(fname,'r')
    allrows=[]
    for row in csv.reader(f):
        allrows.append(row)
    f.close()
    
    cities=allrows[0][1:]
    n=len(cities)
    keys = range(n)
    city_lookup = dict(zip(keys, cities))
    
    allrows=allrows[1:]
    data=np.zeros((n, n),dtype=np.int)
    
    for i in range(n):
        for j in range(n):
            data[i,j]=allrows[i][j+1]
            
    return city_lookup,data

#------------------------------------------------------------------------------    
def distance_on_unit_sphere(lat1, long1, lat2, long2, radius=1.0):
    # Radius determines units '1' gives units of earth radius.
    # lat and long in decimal degrees
    # radius=6371 km for earth
    # Convert latitude and longitude to 
    # spherical coordinates in radians.
    degrees_to_radians = math.pi/180.0
         
    # phi = 90 - latitude
    phi1 = (90.0 - lat1)*degrees_to_radians
    phi2 = (90.0 - lat2)*degrees_to_radians
         
    # theta = longitude
    theta1 = long1*degrees_to_radians
    theta2 = long2*degrees_to_radians
         
    # Compute spherical distance from spherical coordinates.
    # For two locations in spherical coordinates 
    # (1, theta, phi) and (1, theta', phi')
    # cosine( arc length ) = 
    #    sin phi sin phi' cos(theta-theta') + cos phi cos phi'
    # distance = rho * arc length
     
    cos = (math.sin(phi1)*math.sin(phi2)*math.cos(theta1 - theta2) + 
           math.cos(phi1)*math.cos(phi2))
    arc = math.acos( cos )
 
    # Remember to multiply arc by the radius of the earth 
    # in your favorite set of units to get length.
    radius = 6371
    return arc*radius

#------------------------------------------------------------------------------
def getKey2(item):
    return item[1]    
    

    
#------------------------------------------------------------------------------
def selectCitydata(allcities,c,citiesAsDict=1):
    """allcities is a list of lists with each item of the primary list being 
    a list: [cityname, latitude, longitude,......].
    Only the first three items are used. Locatiions are in decimal degrees.
    Second argument 'c' is a number for sample size or list required.    
    third argument is 1 or zero indicating dictiona
    Return a dictionary or list of sequentially ordered city names, as distance
    matrix and subset of the input cities data in the original format order by 
    latitude"""
    
    if type(c)==list:
        selected=c
    else:
        selected =random.sample(range(len(allcities)),c)
    n = len(selected)
    cities=[]
    print 'selected',selected
     
    for i in range(n):
        cities.append(allcities[selected[i]])
     
    cities = sorted(cities,key=getKey2,reverse=True)
    
    city_names = []
     
    data = np.zeros((n,n),dtype=np.int)
     
    for i in range(n):
        city1=cities[i]
        city_names.append(city1[0])
        for j in range(n):
            city2=cities[j]
            if i==j:
                data[i,j]=0
            else: #correct units
                data[i,j]=distance_on_unit_sphere(city1[1], city1[2], city2[1], city2[2],6371)
    print data    
    if citiesAsDict == 1:    
        keys=range(n)
        city_lookup = dict(zip(keys, city_names))
    else:
        city_lookup = city_names
        
    print city_lookup
    print '-------------------------------------------------------------------'
    print '\n                      CITY DATA SELECTED        '
    print '\n------------------------------------------------------------------'
    return city_lookup,data,cities       

#------------------------------------------------------------------------------   
#based on code from Sai Panyam - http://www.saipanyam.net/
#The double-bridge move involves partitioning a permutation into 4 pieces
#(a,b,c,d) and putting it back together in a specific and jumbled ordering
#(a,d,c,b) - This equivalent to a 4-opt move
def doubleBridge(guess):
    # make four slices
    sliceLength = len(guess)/4
    p1 = 1 + random.randrange(0,sliceLength)
    p2 = p1 + 1 + random.randrange(0,sliceLength)
    p3 = p2 + 1 + random.randrange(0,sliceLength)
    # Combine first and fourth slice in order
    # Combine third and second slice in order
    # return the combination of the above two combined slices
    return guess[0:p1] + guess[p3:] + guess[p2:p3] + guess[p1:p2]
        
#------------------------------------------------------------------------------
def swapItems(mylist):
    selection = random.sample(range(len(mylist)),2)
    c1 = mylist[selection[0]]
    c2 = mylist[selection[1]]
    mylist[selection[0]] = c2
    mylist[selection[1]] = c1
    return mylist    

#------------------------------------------------------------------------------    
def reverseSection(mylist):
    markers = random.sample(range(len(mylist)),2)
    if markers[0] < markers[1]:
        c1 = markers[0]
        c2 = markers[1]
    else:
        c1 = markers[1]
        c2 = markers[0]
    subl = mylist[c1:c2] #or subl = mylist[::-1]
    subl.reverse()    
    mylist = mylist[:c1]+subl+mylist[c2:]
    return mylist
    
#------------------------------------------------------------------------------    
def calcroute(route,data):
    """function which calculates distance of route from a distance matrix, data.
    assumes route is permutations of n-1 locations and will be circular,
    so location 0 is appended to the beginning and end of the route."""
    route=[0]+route+[0]
    d=0
    for i in range(len(data)):
        d=d+data[route[i]][route[i+1]]
    return d    

#------------------------------------------------------------------------------    
def routeToPoints(route,cityData):
    """takes list of numbers in order to be plotted, and list of lists
    where each list in the primary list city name, latitude, longitude"""
    cityPointList = []    
    for i in route:
        #print 'adding ',cityData[i][0],' to point list'
        cityP = Point2D(cityData[i][2],cityData[i][1])
        cityPointList.append(cityP)
    return cityPointList
    
#------------------------------------------------------------------------------    
def routeToPolyline(route,cityData):
    """takes list of numbers in order to be plotted, and list of lists
    where each list in the primary list city name, latitude, longitude
    returns a closed loop finishing at original city"""
    cityPolyline = Polyline([])    
    for i in route:
        #print 'adding ',cityData[i][0],' to point polyline'
        cityP = Point2D(cityData[i][2],cityData[i][1])
        cityPolyline.addPoint(cityP)
    cityPolyline.addPoint(Point2D(cityData[0][2],cityData[0][1]))
    return cityPolyline
    



#============================================================================== 
#Testing for this module is incomplete.

class geofuncs_TestCase(unittest.TestCase):
    
    def setUp(self):
        print "Setting up test...\n"
    
   
#------------------------------------------------------------------------------        
    def tearDown(self):

        print "\n...test complete.\n\n"
        print "          ###############################\n\n"  

#------------------------------------------------------------------------------    
    def test_load_Locations(self):
        print "Testing load_Locations"
        citydata = load_Locations('CityLocationTest.csv')
        self.assertAlmostEqual(citydata[0][1],34.3333333333)
        self.assertAlmostEqual(citydata[0][2],62.2)
        self.assertAlmostEqual(citydata[3][1],-14.2666666666)
        self.assertAlmostEqual(citydata[3][2],-170.716666666)
        print "load_Locations Testing Complete"
    
        
#==============================================================================     


if __name__ == "__main__":
    
    unittest.main()    
        