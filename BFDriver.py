# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 17:39:13 2016

@author: s0568630
"""

"""Driver module to implement simple version of brute force solution to 
travelling salesperson."""

import GeoFuncs as gf
from PointPlotter import PointPlotter
from TSPAlgorithm import TSPAlgorithm

pp = PointPlotter()
#load all cities as allcities
allcities = gf.load_Locations('CityLocationTest.csv')
  
numlocs = 10
numiters = 1000
numatt = 100
#pick some cities return (dicitonary)  matrix and cities as lists
city_lookup, dMat, cities = gf.selectCitydata(allcities,numlocs)
#print '\ncity_lookup is: ',city_lookup
#print '\ndistmatrix is: ',distmatrix
#print '\ncities is: ',cities


#Instantiate instance of algorithms
bruteForce = TSPAlgorithm(dMat)

#Set up complete solution list for dataset
bruteForce.solutionList()

print "Everything Solved"


print bruteForce.getOptimalTour()

#get routes as polylines
bFTour = gf.routeToPolyline(bruteForce.getOptimalTour(), cities)

#plot the routes
print "plotting Routes"

#plot basemap
pp.plotWorld(g=0.2, c='grey')
pp.plotPolylines(bFTour,colour='m',width=8,legend='BruteForce')

#show
pp.show()



