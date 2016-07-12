# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 01:38:38 2016

@author: s0568630

Driver Module to act as functionality test for TSPHillclimber 
and associated modules.
"""

import GeoFuncs as gf
from PointPlotter import PointPlotter
import TSPHillClimber as HC
from TSPAlgorithm import TSPAlgorithm

pp = PointPlotter()
#load all cities as allcities
allcities = gf.load_Locations('CityLocations.csv')
  
numlocs = 9
numiters = 1000
numatt = 100
if numlocs <= 10:
    brute = True
else:
    brute = False
    
#pick some cities return (dicitonary)  matrix and cities as lists
city_lookup, dMat, cities = gf.selectCitydata(allcities,numlocs)
#print '\ncity_lookup is: ',city_lookup
#print '\ndistmatrix is: ',distmatrix
#print '\ncities is: ',cities

#Instantiate instance of algorithms
bruteForce = TSPAlgorithm(dMat)
localMixer = HC.LocalMixerHC(dMat)
localImprover = HC.LocalImproverHC(dMat)
globalHC = HC.GlobalHC(dMat)

if brute:
    #Set up complete solution list for dataset
    bruteForce.solutionList()
    allSols = bruteForce.getAllSolutions()
    #Pass it to hill climber algorithms
    localMixer.solutionList(allSols)
    localImprover.solutionList(allSols)
    globalHC.solutionList(allSols)

#Solve run all nonbruteforce algorithms
localMixer.solve(numiters)
localImprover.solve(numiters)
globalHC.solve(numatt, numiters)

print "Everything Solved"

#print results
localMixer.resultFormatter()
localImprover.resultFormatter()
globalHC.resultFormatter()

#get routes as polylines
if brute:
    optimalTour = bruteForce.getOptimalTour()

lMTour = localMixer.getBestTour()
lITour = localImprover.getBestTour()
gHCTour = globalHC.getBestTour()

#------------------------------------------------------------------------------
#plot the routes
print "plotting Routes"

#plot basemap
pp.plotWorld(g=0.2, c='grey')

#------------------------------------------------------------------------------
if brute:
    pp.plotRoute(optimalTour,cities,c='m',routeWidth=8,legend='BruteForce')

pp.plotRoute(lMTour,cities,c='green',routeWidth=4,legend='localMixer')
pp.plotCities(cities,labels=brute)
pp.legend()
#show
pp.show(title = "Local Mixer Hill Climber", xlabel = "Longitude", ylabel="Latitude",
        grid=True)

#------------------------------------------------------------------------------
#plot basemap
pp.plotWorld(g=0.2, c='grey')

if brute:
    pp.plotRoute(optimalTour,cities,c='m',routeWidth=8,legend='BruteForce')

pp.plotRoute(lITour,cities,c='blue',routeWidth=4,legend='localImprover')
pp.plotCities(cities, labels=brute)
pp.legend()
#show
pp.show(title = "Local Improver Hill Climber", xlabel = "Longitude", ylabel="Latitude",
        grid=True)

#------------------------------------------------------------------------------
#plot basemap
pp.plotWorld(g=0.2, c='grey')

if brute:    
    pp.plotRoute(optimalTour,cities,c='m',routeWidth=8,legend='BruteForce')

pp.plotRoute(gHCTour,cities,c='orange',routeWidth=4,legend='GlobalHC')
pp.plotCities(cities,labels=brute)
pp.legend()
#show
pp.show(title = "Global Hill Climber", xlabel = "Longitude", ylabel="Latitude",
        grid=True)

