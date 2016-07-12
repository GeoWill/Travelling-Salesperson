# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 17:26:35 2012
@author: nrjh
"""
from Points import Point2D
from Points import PointField
from Polylines import Polyline
import numpy as np
import random



def spiral(n=100,a=1,b=8,c=64):
    """Generates a Pointfield in a non logarithmic spiral"""
    i = 0
    t = np.pi/c
    p1 = Point2D(1,1)
    spiralPF = PointField([])
    while i < n:
        p2=p1.clone()
        spiralPF.append(p2)
        p1.move((a*t*np.cos(t)),(a*t*np.sin(t)))
        i += 1
        t = t+np.pi/b
    return spiralPF
    
def pointFieldToPolyline(pf,mylist):
    """Function to convert a pointfield to a polyline. Used when plotting
    routes"""
    chain = Polyline()
    points = pf.getPoints()
    for i in mylist:
        chain.addPoint(points[i])
    
    return chain

def rand_PointField(number_points,xlo=0.,xhi=1.,ylo=0.,yhi=1.):
    """ Generates a point field from random points, for
    a specified number of points and x-y range specified
    as paramters"""
    newPoints=[]
    
#use xrange to generate the number of points in this set    
    for i in xrange(number_points):
#random numbers generated in a specific range
        x=random.uniform(xlo,xhi)
        y=random.uniform(ylo,yhi)
#add point to list
        newPoints.append(Point2D(x,y))
    
    return PointField(newPoints)
    
def rand_Point(xlo=0.,xhi=1.,ylo=0.,yhi=1.):
    """ Generates random point, for
    a specified number of points and x-y range specified
    as parameters"""

#random numbers generated in a specific range
    x=random.uniform(xlo,xhi)
    y=random.uniform(ylo,yhi)
 
    return Point2D(x,y)
    

def getPointField_fromFile(fileName):
    """ Generates a Point field (passed as string) from and x-y file
    assuming first line is a header line"""
    points = []
    myFile=open(fileName,'r')
    
#read first lien    
    myFile.readline()

#iterate through other lines
    for line in myFile.readlines():
        items=line.split('\t')
        x=float(items[0])
        y=float(items[1])
        
#generate and append new point to list        
        p=Point2D(x,y)
        points.append(p)
        
    return PointField(points)
#end of function readPoints    
    

        
#ensuere points are always re