# -*- coding: utf-8 -*-
"""
Created on Sun Feb 28 14:46:59 2016

@author: s0568630

Module to run local mixer as a functionality test
"""

import GeoFuncs as gf
from PointPlotter import PointPlotter
import TSPHillClimber as HC


pp = PointPlotter()
#load all cities as allcities
allcities = gf.load_Locations('CityLocations.csv')
  
numlocs = 10
numiters = 1000
numatt = 100
#pick some cities return (dicitonary)  matrix and cities as lists
city_lookup, dMat, cities = gf.selectCitydata(allcities,numlocs)
#print '\ncity_lookup is: ',city_lookup
#print '\ndistmatrix is: ',distmatrix
#print '\ncities is: ',cities

#Instantiate instance of algorithms
localMixer = HC.LocalMixerHC(dMat)

#Set up complete solution list for all of them
localMixer.solutionList()

#Solve run all nonbruteforece algorithms
localMixer.solve(numiters, v=1)

#print results
localMixer.resultFormatter()
