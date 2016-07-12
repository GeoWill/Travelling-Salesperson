# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 14:05:10 2016

@author: s0568630
"""

import numpy as np
import sys 
import itertools as it
import math
import time
import unittest


#============================================================================== 


class TSPAlgorithm(object):
    """Parent class for Travelling Sales Person Algorithms.
    Instantiate and instance with a n*n numpy array corresponding to distance 
    matrix of network to be solved.
    This class can only solve by brute force, so keep distance matrix small.
    """
    
    def __init__(self, data):
        """constructor to instantiate an instance"""
        
        if isinstance(data,np.ndarray):
            self._distMatrix = data
            self._length = len(self._distMatrix[0])
            self._iteration = math.factorial((self._length-1))
            self._optimalD = sys.maxint #best possible solution solved wiht brute force via full solve
            self._bestD = sys.maxint #best from some other algorithm, via solve, in TSPAlgorithm class this is still  brute force
            self._worstD = 0 #worst possible solution solved with brute force via fullsolve
            self._optimalTour = [] #optimal tour
            self._bestTour = [] #best tour found by solve
            self._worstTour = [] #worst possible tour
            self._optSolved = False #checker for if full solve has been run
            self._solved = False #checker for it solve has been run
            self._timer = 0
            self._allSolutions = [] #List of all possible solutions for self._distmatrix
            self._allrange = 0
            self._efficacyList = []
            self._efficacyMean = 0
            self._solutionsrange = 0
        else:
            raise Exception("data must by type 'np.ndarray'. import numpy as np")
            


#------------------------------------------------------------------------------            
    def getData(self):
        """return self._distMatrix"""
        return self._distMatrix

#------------------------------------------------------------------------------        
    def getAllSolutions(self):
        """return list of all possible solution as list of tuples, 
        (dist, route) types: (int,list). If solutionList hasn't been run 
        raise exception."""
        if len(self._allSolutions) > 1:
            return self._allSolutions
        else:
            raise Exception('self._allSolutions = []. Run self.solutionList()')        
#------------------------------------------------------------------------------    
    def getOptimalD(self):
        """Return optimal distance as int. If not fullsolved raise exception"""
        if self._optSolved:
            return self._optimalD
        else:
            raise Exception("self._optSolved = False")
        
#------------------------------------------------------------------------------        
    def getOptimalTour(self):
        """Return optimal tour as list. If not fullsolved raise exception"""
        if self._optSolved:
            return self._optimalTour
        else:
            raise Exception("self._optSolved = False")
            
#------------------------------------------------------------------------------    
    def getworstD(self):
        """Return Worst distance as int. If not fullsolved raise exception"""

        if self._optSolved:
            if self._worstD > 0:
                return self._worstD
            else:
                raise Exception("must run fullSolved to return self._worstD")    
        else:
            raise Exception("self._optSolved = False")
            
#------------------------------------------------------------------------------    
    def getWorstTour(self):
        """Return worst tour as list. If not fullsolved raise exception"""

        if self._optSolved:
            if self._worstD > 0:
                return self._worstTour
            else:
                raise Exception("must run fullSolved to return self._worstTour")    
        else:
            raise Exception("self._solved = False")
            
#------------------------------------------------------------------------------    
    def getBestD(self):
        """Return best distance as int. If not solved raise exception"""
        if self._Solved:
            return self._optimalD
        else:
            raise Exception("self._Solved = False")
        
#------------------------------------------------------------------------------        
    def getBestTour(self):
        """Return best tour as list. If not solved raise exception"""
        if self._solved:
            return self._bestTour
        else:
            raise Exception("self._solved = False")
        
#------------------------------------------------------------------------------    
    def getIter(self):
        """method to return iterations required to reach bestD"""
        return self._iteration
        
#------------------------------------------------------------------------------    
    def getTime(self):
        """method to return time required to solve"""
        if self._timer>0:
            return self._timer
        else:
            raise Exception("must run solve to calulate time")
        
#------------------------------------------------------------------------------            
    def getOptSolved(self):
        """method to check state of algorithm re being optimally solved
        returns bool"""
        return self._optSolved
        
#------------------------------------------------------------------------------            
    def getSolved(self):
        """method to check state of algorithm re being solved
        returns bool"""
        return self._solved

#------------------------------------------------------------------------------            
    def getLength(self):
        """return length of self._distMatrix as int"""
        return self._length

#------------------------------------------------------------------------------        
    def checkOptimal(self,d,route,v=0):
        """Method to check if new d is shorter than optimald and update steps
        accordingly. pass v=1 for verbose"""
        if d < self._optimalD:
            self._optimalD = d
            self._optimalTour = route
            if v == 1:
                print 'current optimal dist is: ',self._optimalD
                print 'current optimal Tour is: ',self._optimalTour
#------------------------------------------------------------------------------        
    def checkBest(self,d,route,i,v=0):
        """Method to check if new d is shorter than bestD and update steps
        accordingly. pass v=1 for verbose"""
        if d < self._bestD:
            self._bestD = d
            self._iteration = i
            if v == 1:
                print 'current best dist is: ',self._bestD
                print 'self._bestTour is: ',self._bestTour
            return True     
        else:
            return False
#------------------------------------------------------------------------------                
    def checkWorst(self,d,route,v=0):
        """Method to check if new d is longer than worstd and update steps
        accordingly. pass v=1 for verbose"""
        if d > self._worstD:
            self._worstD = d
            self._worstTour = route
            if v == 1:
                print 'current worst dist is: ',self._worstD

#------------------------------------------------------------------------------           
    def resultFormatter(self):
        """Method to print formatted results"""
        self.resultHeader()
        if self._solved:
            print '\nBest Route from solve is: ',self._bestTour
            print '\nShortest distance from solve is: ',self._bestD
            print '\nFound best route after ',self._iteration,' iterations'
            print '\nTime taken was',self._timer,' seconds'
        if self._optSolved:
            print '\nOptimal route is: ',self._optimalTour
            print '\nOptimal distance from fullsolve is: ',self._optimalD
            print '\nWorst distance from fullsolve is: ',self._worstD
        if not(self._solved or self._optSolved):
            print '\nNo results'
        print '---------------------------------------------------'
                
#------------------------------------------------------------------------------    
    def fullReset(self): 
        """reset states to as they were for instantiation"""
        self.solveReset()
        self._optimalD = sys.maxint
        self._worstD = 0
        self._optimalTour = []
        self._worstTour = []
        self._optSolved = False
        self._allSolutions = [] #List of all possible solutions for self._distmatrix
        self._allrange = 0
        self._timer = 0
        self._bestD = sys.maxint
        self._bestTour = []
        self._efficacyList = []
        self._efficacyMean = 0
        self._solutionsrange = 0
        
#------------------------------------------------------------------------------
    def solveReset(self):
        """reset states to as thtey were before solve"""
        self._bestD = sys.maxint
        self._bestTour = []
        self._timer = 0
        self._solved = False
        
#------------------------------------------------------------------------------
    def fullSolve(self,v=0):
        """solve using brute force algorithm"""
        n=self._length
        print '\nstart fullsolve'
        for l in it.permutations(range(1,n)):
            fullRoute=[0]+list(l)+[0]
            iters = 0
            dist=0
            for j in range(n):    
                c1=fullRoute[j]
                c2=fullRoute[j+1]
                d=self._distMatrix[c1,c2]
                dist=dist+d
                
            self.checkOptimal(dist,fullRoute,v)
            self.checkWorst(dist,fullRoute,v)
            self._allrange = self._worstD-self._optimalD                
            
            if v == 1:
                iters += 1
                if iters%1000000 == 0:
                    print 'number of iterations: ',iters
                    
        self._optSolved = True  #update self._optSolved
        print 'end fullsolve'
        
#------------------------------------------------------------------------------    
    def solve(self,v=0,**kwargs):
        """Method to solve just checking for best_D should be (slightly)
        faster than fullsolve"""
        n=self._length
        i=0
        t = time.clock()
        
        for l in it.permutations(range(1,n)):
            fullRoute=[0]+list(l)+[0]
            i += 1
            dist=0
            for j in range(n):    
                c1=fullRoute[j]
                c2=fullRoute[j+1]
                d=self._distMatrix[c1,c2]
                dist=dist+d
            if dist < self._bestD:
                self._bestD = dist
                self._bestTour= fullRoute 
            
        self._solved = True  #update self._optSolved
        self._timer = time.clock() - t
        
#------------------------------------------------------------------------------        
    def solutionList(self,sols=[],v=0):
        """Method equivalent to fullSolve, but which makes a list of
        every possible solution for self._distMatrix. 
        List will be (self._length-1)! long
        Can pass already computed set as list"""
        t = time.clock()        
        if len(sols)>0:
            self._allSolutions = sols
        else:    
            n=self._length
            print '\nstart solution list'
            print 'calculating ',math.factorial(n-1),' solutions...'
            routes = []
            dists = []
            iters=0
            for l in it.permutations(range(1,n)):
                fullRoute=[0]+list(l)+[0]
                routes.append(fullRoute)            
                dist=0
                for j in range(n):    
                    c1=fullRoute[j]
                    c2=fullRoute[j+1]
                    d=self._distMatrix[c1,c2]
                    dist=dist+d
                dists.append(dist)
                
                if v == 1:
                    iters += 1
                    if iters%1000000 == 0:
                        print 'number of iterations: ',iters
                
            self._allSolutions = sorted(zip(dists,routes), key = lambda pair : pair[0])
            #print self._allSolutions
        print '...finished generating solution list \n'
        if self._optSolved == False:
            self._optimalD = self._allSolutions[0][0]
            self._worstD = self._allSolutions[-1][0]
            self._optimalTour = self._allSolutions[0][1]
            self._worstTour = self._allSolutions[-1][1]
            self._optSolved = True
            self._timer = self._timer = time.clock() - t
            
            
#------------------------------------------------------------------------------        
    def efficacy(self,runs=100,iterations=1000,**kwargs):
        """Method takes number of runs and iterations, then evaluates efficacy
        for self.solve(). self._optSolved must be True"""
        i = 0
        dists=[]
        effs = []
        iters = []
        if not self._optSolved:
            self.fullSolve()
        while i < runs:
            self.solveReset()
            self.solve(iterations = iterations,**kwargs)
            #print "self._bestD is: ",self._bestD
            #print "self._optimalD is: ",self._optimalD
            efficacy = ((float(self._bestD) - float(self._optimalD))/float(self._optimalD))
            dists.append(self._bestD)            
            effs.append(efficacy)
            iters.append(self._iteration)
            i += 1
        self._efficacyList = [dists,effs,iters]
        self._efficacyMean = float(sum(effs)/float(runs))
        
        return self._efficacyList, self._efficacyMean
        
#------------------------------------------------------------------------------        
    def getEfficacy(self):
        """method returns list of lists [bestDs,efficacys,iterss] and their mean"""
        return self._efficacyList,self._efficacyMean


#============================================================================== 


class TSPAlgorithm_TestCase(unittest.TestCase):
    def setUp(self):
        print "Setting up test...\n"
        self.row1 = [0,20,15,10,20]
        self.row2 = [200,0,50,30,45]
        self.row3 = [40,20,0,200,200]
        self.row4 = [200,200,200,0,70]    
        self.row5 = [200,200,200,200,0]    
        self.distanceMatrix = np.array([self.row1,self.row2,self.row3,
                                        self.row4,self.row5])
        self.locations = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
        self.myTSPAlgorithm = TSPAlgorithm(self.distanceMatrix)
 
        
#------------------------------------------------------------------------------        
    def tearDown(self):
        self.row1 = None
        self.row2 = None
        self.row3 = None
        self.row4 = None
        self.row5 = None        
        self.distanceMatrix = None
        self.myTSPAlgorithm.fullReset()
        print "\n...test complete.\n\n"
        print "          ###############################\n\n"  

#------------------------------------------------------------------------------    
    def test_getEfficacy(self):
        print "Testing getEfficacy"
        self.myTSPAlgorithm.efficacy(runs=5)
        efflist,effmean = self.myTSPAlgorithm.getEfficacy()
        self.assertEqual(len(efflist),3)
        self.assertEqual(len(efflist[0]),5)
        self.assertEqual(len(efflist[1]),5)
        self.assertEqual(len(efflist[2]),5)
        self.assertEqual(effmean,0)
        print "getEfficacy Testing Complete"


#------------------------------------------------------------------------------    
    def test_efficacy(self):
        print "Testing efficacy"
        self.myTSPAlgorithm.efficacy(runs=5)
        self.assertEqual(len(self.myTSPAlgorithm._efficacyList),3)
        self.assertEqual(len(self.myTSPAlgorithm._efficacyList[0]),5)
        self.assertEqual(len(self.myTSPAlgorithm._efficacyList[1]),5)
        self.assertEqual(len(self.myTSPAlgorithm._efficacyList[2]),5)
        self.assertEqual(self.myTSPAlgorithm._efficacyMean,0)
        print "efficacy Testing Complete"
        
#------------------------------------------------------------------------------    
    def test_solve(self):
        print "Testing Solve"
        self.myTSPAlgorithm.solve()
        self.assertListEqual([0, 2, 1, 3, 4, 0],self.myTSPAlgorithm._bestTour)
        self.assertListEqual([],self.myTSPAlgorithm._worstTour)
        self.assertEqual(335,self.myTSPAlgorithm._bestD)
        self.assertLessEqual(self.myTSPAlgorithm._iteration,24)
        print "solve Testing Complete"
        
#------------------------------------------------------------------------------    
    def test_fullSolve(self):
        print "TestingfullSolve"
        self.myTSPAlgorithm.fullSolve()
        self.assertListEqual([0, 2, 1, 3, 4, 0],self.myTSPAlgorithm._optimalTour)
        self.assertEqual(335,self.myTSPAlgorithm._optimalD)
        self.assertListEqual([0, 4, 2, 3, 1, 0],self.myTSPAlgorithm._worstTour)
        self.assertEqual(820,self.myTSPAlgorithm._worstD)
        print "fullSolve Testing Complete"

#------------------------------------------------------------------------------    
    def test_solutionList(self):
        print "Testing solutionList"
        self.myTSPAlgorithm.solutionList()
        self.assertIsInstance(self.myTSPAlgorithm._allSolutions[0],tuple)
        self.assertEqual(24,len(self.myTSPAlgorithm._allSolutions))
        self.assertEqual(335,self.myTSPAlgorithm._allSolutions[0][0])
        self.assertEqual(820,self.myTSPAlgorithm._allSolutions[23][0])
        self.myTSPAlgorithm.fullSolve()
        self.assertListEqual([0, 2, 1, 3, 4, 0],self.myTSPAlgorithm._optimalTour)
        self.assertEqual(335,self.myTSPAlgorithm._optimalD)
        self.assertListEqual([0, 4, 2, 3, 1, 0],self.myTSPAlgorithm._worstTour)
        self.assertEqual(820,self.myTSPAlgorithm._worstD)
        print "solutionList Testing Complete"

#------------------------------------------------------------------------------    
    def test_getSolved(self):
        print "Testing getoptSolved"
        self.assertFalse(self.myTSPAlgorithm.getOptSolved())
        self.myTSPAlgorithm._optSolved = True
        self.assertTrue(self.myTSPAlgorithm.getOptSolved())
        "getoptSolved Testing Complete"
        
#------------------------------------------------------------------------------    
    def test_gets(self):
        """class variables assigned directly to preserve unit testing"""
        print "Testing gets"
        
        self.myTSPAlgorithm._optimalTour = [0, 2, 1, 3, 4, 0]
        self.myTSPAlgorithm._optimalD = 335
        self.myTSPAlgorithm._worstTour = [0, 4, 2, 3, 1, 0]
        self.myTSPAlgorithm._worstD = 820
        self.myTSPAlgorithm._optSolved = True
        self.myTSPAlgorithm._allSolutions = [(335, [0, 2, 1, 3, 4, 0]), (360, [0, 1, 3, 4, 2, 0]), (370, [0, 3, 4, 1, 2, 0]), (470, [0, 4, 2, 1, 3, 0]), (475, [0, 3, 2, 1, 4, 0]), (480, [0, 2, 1, 4, 3, 0]), (490, [0, 4, 1, 3, 2, 0]), (495, [0, 3, 1, 4, 2, 0]), (500, [0, 3, 4, 2, 1, 0]), (505, [0, 1, 4, 3, 2, 0]), (510, [0, 4, 3, 1, 2, 0]), (540, [0, 1, 2, 3, 4, 0]), (640, [0, 4, 3, 2, 1, 0]), (645, [0, 2, 4, 1, 3, 0]), (650, [0, 1, 3, 2, 4, 0]), (660, [0, 2, 3, 1, 4, 0]), (660, [0, 3, 1, 2, 4, 0]), (665, [0, 1, 4, 2, 3, 0]), (670, [0, 1, 2, 4, 3, 0]), (670, [0, 4, 1, 2, 3, 0]), (685, [0, 2, 3, 4, 1, 0]), (810, [0, 3, 2, 4, 1, 0]), (815, [0, 2, 4, 3, 1, 0]), (820, [0, 4, 2, 3, 1, 0])]
        self.myTSPAlgorithm._timer = 42        
        
        self.assertListEqual(self.myTSPAlgorithm.getAllSolutions(),[(335, [0, 2, 1, 3, 4, 0]), (360, [0, 1, 3, 4, 2, 0]), (370, [0, 3, 4, 1, 2, 0]), (470, [0, 4, 2, 1, 3, 0]), (475, [0, 3, 2, 1, 4, 0]), (480, [0, 2, 1, 4, 3, 0]), (490, [0, 4, 1, 3, 2, 0]), (495, [0, 3, 1, 4, 2, 0]), (500, [0, 3, 4, 2, 1, 0]), (505, [0, 1, 4, 3, 2, 0]), (510, [0, 4, 3, 1, 2, 0]), (540, [0, 1, 2, 3, 4, 0]), (640, [0, 4, 3, 2, 1, 0]), (645, [0, 2, 4, 1, 3, 0]), (650, [0, 1, 3, 2, 4, 0]), (660, [0, 2, 3, 1, 4, 0]), (660, [0, 3, 1, 2, 4, 0]), (665, [0, 1, 4, 2, 3, 0]), (670, [0, 1, 2, 4, 3, 0]), (670, [0, 4, 1, 2, 3, 0]), (685, [0, 2, 3, 4, 1, 0]), (810, [0, 3, 2, 4, 1, 0]), (815, [0, 2, 4, 3, 1, 0]), (820, [0, 4, 2, 3, 1, 0])])
        self.assertListEqual(self.myTSPAlgorithm.getOptimalTour(),[0, 2, 1, 3, 4, 0])
        self.assertEqual(self.myTSPAlgorithm.getOptimalD(),335)
        self.assertEqual(self.myTSPAlgorithm.getWorstTour(),[0, 4, 2, 3, 1, 0])
        self.assertEqual(self.myTSPAlgorithm.getworstD(),820)
        self.assertEqual(self.myTSPAlgorithm.getLength(),5)
        self.assertEqual(self.myTSPAlgorithm.getIter(),24)
        self.assertEqual(self.myTSPAlgorithm.getTime(),42)
        print "gets Testing Complete"
        
#==============================================================================     


if __name__ == "__main__":
    
    unittest.main()
    

        
        
            
            
            