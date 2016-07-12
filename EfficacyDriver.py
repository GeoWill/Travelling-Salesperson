# -*- coding: utf-8 -*-
"""
Created on Mon Feb 29 03:24:24 2016

@author: s0568630

Driver Module to test hill climber algorithm classes on a random network and
a geographic network. 
"""

import GeoFuncs as gf
from PointPlotter import PointPlotter
import TSPHillClimber as HC
from TSPAlgorithm import TSPAlgorithm
import PointHandler as ph
import matplotlib.pyplot as mp
pp = PointPlotter()


#-----------------------------------------------------------------------------
myColours = ['magenta','mediumseagreen','chocolate','purple','teal',
             'saddlebrown','fucsia','darkorange']

runs = 1000
localiters = 1000
globalattempts = 10

nloc = 10
if nloc <= 10:
    brute = True
else:
    brute = False

print "\nCreating random data set..."
randPF = ph.rand_PointField(nloc,-180,180,-100,100)
randData = randPF.distanceMatrix()
print "...instantiating algorithms..."
randBF = TSPAlgorithm(randData)
randLM = HC.LocalMixerHC(randData)
randLI = HC.LocalImproverHC(randData)
randGHC = HC.GlobalHC(randData)


if brute:
    #Set up complete solution list for dataset
    randBF.solutionList()
    allSols = randBF.getAllSolutions()
    #Pass it to hill climber algorithms
    randLM.solutionList(allSols)
    randLI.solutionList(allSols)
    randGHC.solutionList(allSols)
print "...random data and algorithms created\n"

print "\nCreating Geographical data set..."
#load all cities as allcities
allcities = gf.load_Locations('CityLocations.csv')
#pick some cities return (dicitonary)  matrix and cities as lists
city_lookup, geogData, cities = gf.selectCitydata(allcities,nloc)
print "...instantiating algorithms..."
geogBF = TSPAlgorithm(geogData)
geogLM = HC.LocalMixerHC(geogData)
geogLI = HC.LocalImproverHC(geogData)
geogGHC = HC.GlobalHC(geogData)


if brute:
    #Set up complete solution list for dataset
    geogBF.solutionList()
    allSols = geogBF.getAllSolutions()
    #Pass it to hill climber algorithms
    geogLM.solutionList(allSols)
    geogLI.solutionList(allSols)
    geogGHC.solutionList(allSols)
      
print "...Geographical data and algorithms created\n"

#-----------------------------------------------------------------------------
print"\nCalculating Efficacy of algorithms..."
#effList is list of lists: (bestDs,efficacys,iters)

randLM.efficacy(runs=runs,iterations=localiters)
randLI.efficacy(runs=runs,iterations=localiters)
randGHC.efficacy(runs=runs,iterations=localiters)
geogLM.efficacy(runs=runs,iterations=localiters)
geogLI.efficacy(runs=runs,iterations=localiters)
geogGHC.efficacy(runs=runs,iterations=localiters)
print"...Efficacy calculated.\n"

randLMEffList, randLMEffMean = randLM.getEfficacy()
randLIEffList, randLIEffMean = randLI.getEfficacy()
randGHCEffList, randGHCEffMean = randGHC.getEfficacy()
geogLMEffList, geogLMEffMean = geogLM.getEfficacy()
geogLIEffList, geogLIEffMean = geogLI.getEfficacy()
geogGHCEffList, geogGHEffMean = geogGHC.getEfficacy()

#-----------------------------------------------------------------------------
print 'With ',nloc,' nodes and'
print 'based on ',runs,' runs, and ',localiters,' iterations'
print 'On a random network: '
print 'LocalMixer Mean Efficacy is: ',randLMEffMean
print 'LocalImprover Mean Efficacy is: ',randLIEffMean
print 'Global Hill Climber Mean Efficacy is: ',randGHCEffMean
print '\nOn a geographical network: '
print 'LocalMixer Mean Efficacy is: ',geogLMEffMean
print 'LocalImprover Mean Efficacy is: ',geogLIEffMean
print 'Global Hill Climber Mean Efficacy is: ',geogGHEffMean

mp.title('Local Mixer on Random Network')          
mp.xlabel('Iterations to Solution')
mp.ylabel('Efficacy')
mp.scatter(randLMEffList[2],randLMEffList[1],c=myColours[0],alpha=0.7)
mp.show() 

mp.title('LocalImprover on Random Network')          
mp.xlabel('Iterations to Solution')
mp.ylabel('Efficacy')
mp.scatter(randLIEffList[2],randLIEffList[1],c=myColours[1],alpha=0.7)
mp.show()

mp.title('Global Hill Climber on Random Network')          
mp.xlabel('Iterations to Solution')
mp.ylabel('Efficacy')
mp.scatter(randGHCEffList[2],randGHCEffList[1],c=myColours[2],alpha=0.7)
mp.show()

mp.title('Local Mixer on Geographical Network')          
mp.xlabel('Iterations to Solution')
mp.ylabel('Efficacy')
mp.scatter(geogLMEffList[2],geogLMEffList[1],c=myColours[3],alpha=0.7)
mp.show() 

mp.title('LocalImprover on Geographical Network')          
mp.xlabel('Iterations to Solution')
mp.ylabel('Efficacy')
mp.scatter(geogLIEffList[2],geogLIEffList[1],c=myColours[4],alpha=0.7)
mp.show()

mp.title('Global Hill Climber on Geographical Network')          
mp.xlabel('Iterations to Solution')
mp.ylabel('Efficacy')
mp.scatter(geogGHCEffList[2],geogGHCEffList[1],c=myColours[5],alpha=0.7)
mp.show()
#------------------------------------------------------------------------------
mp.title('All on Random Network')          
mp.xlabel('Iterations to Solution')
mp.ylabel('Efficacy')
mp.scatter(randLMEffList[2],randLMEffList[1],c=myColours[0],alpha=0.7)

mp.scatter(randLIEffList[2],randLIEffList[1],c=myColours[1],alpha=0.7)

mp.scatter(randGHCEffList[2],randGHCEffList[1],c=myColours[2],alpha=0.7)
mp.show()

mp.title('All on Geographical Network')          
mp.xlabel('Iterations to Solution')
mp.ylabel('Efficacy')
mp.scatter(geogLMEffList[2],geogLMEffList[1],c=myColours[3],alpha=0.7)

mp.scatter(geogLIEffList[2],geogLIEffList[1],c=myColours[4],alpha=0.7)

mp.scatter(geogGHCEffList[2],geogGHCEffList[1],c=myColours[5],alpha=0.7)
mp.show()

###############################################################################
#==============================================================================
###############################################################################









