# -*- coding: utf-8 -*-
"""
Created on Sat Feb 27 16:37:29 2016

@author: s0568630

Module containing three subclasses of TSPAlgorithm class. All are 
implementations of different versions of Hills climber algorithms.
"""

import numpy as np
import sys 
import time
import unittest
import random
import GeoFuncs as gf
from TSPAlgorithm import TSPAlgorithm
  
    
#==============================================================================


class LocalMixerHC (TSPAlgorithm):
    """Subclass of TSPA Algorithm to implement a Hill CLimber algorithm
    Which will carry out proximate search of solution space by randomly
    alternating between swapItems and reverseSection methods from GeoFuncs
    """  

    def __init__(self, data):
        
        TSPAlgorithm.__init__(self, data)            

#------------------------------------------------------------------------------           
    def resultHeader(self):
        """Method to customise header for results"""
        if self._solved:
            print '---------------------------------------------------'
            print '             |  LOCAL MIXER RESULTS  |             '
            print '---------------------------------------------------'

#------------------------------------------------------------------------------    
    def solve(self, iterations, v=0):
        """solve method using hillclimber algorithm which randomly swaps
        between swapping items in, and reversing sections of, route list,
        to search local solution space"""
        t = time.clock()        
        n = self._length
        guess = range(1,n)
        random.shuffle(guess)
        
        for i in range(1,iterations+1):
            swapC=bool(random.getrandbits(1))
            if swapC:
                newGuess = gf.swapItems(guess[:])
                newD = gf.calcroute(newGuess,self._distMatrix)
                if self.checkBest(newD,newGuess,i,v):
                    guess = newGuess
                if v == 1:
                    print 'guess made with swapItems'
            else:
                newGuess = gf.reverseSection(guess[:])
                newD = gf.calcroute(newGuess,self._distMatrix)
                if self.checkBest(newD,newGuess,i,v):
                    guess = newGuess
                if v == 1:
                    print 'guess made with reverseSection'

        self._solved = 1        
        self._bestD = gf.calcroute(guess,self._distMatrix)
        self._bestTour = [0]+guess+[0] 
        self._timer = time.clock() - t
        
        if v == 1:
            self.resultFormatter()
    

#==============================================================================
#==============================================================================


class LocalImproverHC (TSPAlgorithm):
    """Subclass of TSPA Algorithm to implement a Hill CLimber algorithm
    Which will abandon proximate search of solution space when no improvement
    reached before threshold. Wil then pursue broader search loking for other
    local minima clloser to optimal."""    
    
    def __init__(self, data):
        
        TSPAlgorithm.__init__(self, data)
            

                    
#------------------------------------------------------------------------------           
    def resultHeader(self):
        """Method to customise header for results"""
        if self._solved:
            print '---------------------------------------------------'
            print '          |  LOCAL IMPROVER RESULTS  |             '
            print '---------------------------------------------------'
            
#------------------------------------------------------------------------------   
    def solve(self, iterations, v=0):
        """Solve method redefined from parent class. Takes iterations as
        int type argument. Solves TSP by  searching proximate solution space
        via swapitems and reverseSection Functions, but when threshold is 
        reached, changes to searching larger portion of solution space via 
        double bridge function.
        Becasue of this TSPO instance must be for n=4 locations."""
        if self._length > 4: #to ensure double bridge can work        
            t = time.clock()        
            n = self._length
            guess = range(1,n)
            random.shuffle(guess)
            
            for i in range(1,iterations+1):
    #           #Define Threshold
                if i > (self._iteration+(self._length**2)):
                    newGuess = gf.doubleBridge(guess)
                    newD = gf.calcroute(newGuess,self._distMatrix)
                    if self.checkBest(newD,newGuess,i,v):
                        guess = newGuess
                    if v == 1:
                        print 'guessed with DBridge after',i,' iterations'
                else:
                    swapC=bool(random.getrandbits(1))
                    if swapC:
                        newGuess = gf.swapItems(guess[:])
                        newD = gf.calcroute(newGuess,self._distMatrix)
                        if self.checkBest(newD,newGuess,i,v):
                                guess = newGuess
                        if v == 1:
                            print 'guessed with swapItems after',i,' iterations'
                    else:
                        newGuess = gf.reverseSection(guess[:])
                        newD = gf.calcroute(newGuess,self._distMatrix)
                        if self.checkBest(newD,newGuess,i,v):
                            guess = newGuess
                        if v == 1:
                            print 'guessed with reverseSection after',i,' iterations'
    
            self._solved = 1        
            self._bestD = gf.calcroute(guess,self._distMatrix)
            self._bestTour = [0]+guess+[0] 
            self._timer = time.clock() - t
            
            if v == 1:
                self.resultFormatter()
        else:
            raise Exception("self._length < 5 so double bridge method can't work")


#==============================================================================
#==============================================================================


class GlobalHC (TSPAlgorithm):
    """Subclass of TSPA Algorithm to implement a global Hill CLimber algorithm
    Which will call several versions of local hillclimbers on TSP and keep the
    best results"""
    def __init__(self, data):
        
        TSPAlgorithm.__init__(self, data)
        
                    
#------------------------------------------------------------------------------           
    def resultHeader(self):
        """Method to customise header for results"""
        if self._solved:
            print '---------------------------------------------------'
            print '         |  GLOBAL HILLCLIMBER RESULTS  |             '
            print '---------------------------------------------------'
            
#------------------------------------------------------------------------------
    def localMixer(self, iterations, v=0):    
        """local mixer solve method reproduced. Method searches proximate 
        solution space to initial guess via random switching between swapItems
        and reverseSection Functions"""
        t = time.clock()        
        n = self._length
        guess = range(1,n)
        random.shuffle(guess)
        
        for i in range(1,iterations+1):
            swapC=bool(random.getrandbits(1))
            if swapC:
                newGuess = gf.swapItems(guess[:])
                newD = gf.calcroute(newGuess,self._distMatrix)
                if self.checkBest(newD,newGuess,i,v):
                    guess = newGuess
            else:
                newGuess = gf.reverseSection(guess[:])
                newD = gf.calcroute(newGuess,self._distMatrix)
                if self.checkBest(newD,newGuess,i,v):
                    guess = newGuess

        self._solved = 1        
        self._bestD = gf.calcroute(guess,self._distMatrix)
        self._bestTour = [0]+guess+[0] 
        self._timer = time.clock() - t       
            
#------------------------------------------------------------------------------   
    def solve(self, iterations, attempts=10, v=0):
        """Redefinition of parent solve method. Method now takes iterations and
        parameters as int type arguments. Method will run a local hill climber
        search for every i in range(attempts). class instance will be updated 
        with best result. Local searches will search 'iterations' times.
        pass v= 1 for verbose output"""
        t = time.clock()        
        a = 0
        d = sys.maxint-1
        route = self._bestTour
        
        while a <= attempts:
            self.solveReset()            
            self.localMixer(iterations)
            
            if self._bestD < d:
                d = self._bestD
                route = self._bestTour
            a+=1
            
        self._bestTour = route
        self._bestD = d
        self._timer = time.clock() - t
        
        if v == 1:
            self.resultFormatter()

###############################################################################
#==============================================================================
###############################################################################


class LocalMixerHCTestCase(unittest.TestCase):
    
    def setUp(self):      
        print "Setting up test...\n"
        self.row1 = [0,20,15,10,20]
        self.row2 = [200,0,50,30,45]
        self.row3 = [40,20,0,200,200]
        self.row4 = [200,200,200,0,70]    
        self.row5 = [200,200,200,200,0]  
        self.distanceMatrix = np.array([self.row1,self.row2,self.row3,self.row4,self.row5])
        self.locations = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
        self.hillClimberTSP = LocalMixerHC(self.distanceMatrix)
    
    def tearDown(self):
        self.row1 = None
        self.row2 = None
        self.row3 = None
        self.row4 = None  
        self.row5 = None
        self.distanceMatrix = None
        self.hillClimberTSP.fullReset()
        print "\n...test complete.\n\n"
        print "          ###############################\n\n"        

#------------------------------------------------------------------------------   
    def test_localMixer(self):
        print "Testing Local Mixer"
        self.hillClimberTSP.solve(10,v=0)
        self.assertEqual(6,len(self.hillClimberTSP._bestTour))
        self.assertGreaterEqual(self.hillClimberTSP._bestD,335)
        print "Local Mixer Testing Complete"      

#------------------------------------------------------------------------------    
    def test_gets(self):
        """class variables assigned directly to preserve unit testing"""
        print "Testing gets"
        
        self.hillClimberTSP._optimalTour = [0, 2, 1, 3, 4, 0]
        self.hillClimberTSP._optimalD = 335
        self.hillClimberTSP._worstTour = [0, 4, 2, 3, 1, 0]
        self.hillClimberTSP._worstD = 820
        self.hillClimberTSP._optSolved = True
        self.hillClimberTSP._solved = True
        self.hillClimberTSP._iteration = 666
        self.hillClimberTSP._allSolutions = [(335, [0, 2, 1, 3, 4, 0]), (360, [0, 1, 3, 4, 2, 0]), (370, [0, 3, 4, 1, 2, 0]), (470, [0, 4, 2, 1, 3, 0]), (475, [0, 3, 2, 1, 4, 0]), (480, [0, 2, 1, 4, 3, 0]), (490, [0, 4, 1, 3, 2, 0]), (495, [0, 3, 1, 4, 2, 0]), (500, [0, 3, 4, 2, 1, 0]), (505, [0, 1, 4, 3, 2, 0]), (510, [0, 4, 3, 1, 2, 0]), (540, [0, 1, 2, 3, 4, 0]), (640, [0, 4, 3, 2, 1, 0]), (645, [0, 2, 4, 1, 3, 0]), (650, [0, 1, 3, 2, 4, 0]), (660, [0, 2, 3, 1, 4, 0]), (660, [0, 3, 1, 2, 4, 0]), (665, [0, 1, 4, 2, 3, 0]), (670, [0, 1, 2, 4, 3, 0]), (670, [0, 4, 1, 2, 3, 0]), (685, [0, 2, 3, 4, 1, 0]), (810, [0, 3, 2, 4, 1, 0]), (815, [0, 2, 4, 3, 1, 0]), (820, [0, 4, 2, 3, 1, 0])]
        self.hillClimberTSP._timer = 42        
        
        self.assertListEqual(self.hillClimberTSP.getAllSolutions(),[(335, [0, 2, 1, 3, 4, 0]), (360, [0, 1, 3, 4, 2, 0]), (370, [0, 3, 4, 1, 2, 0]), (470, [0, 4, 2, 1, 3, 0]), (475, [0, 3, 2, 1, 4, 0]), (480, [0, 2, 1, 4, 3, 0]), (490, [0, 4, 1, 3, 2, 0]), (495, [0, 3, 1, 4, 2, 0]), (500, [0, 3, 4, 2, 1, 0]), (505, [0, 1, 4, 3, 2, 0]), (510, [0, 4, 3, 1, 2, 0]), (540, [0, 1, 2, 3, 4, 0]), (640, [0, 4, 3, 2, 1, 0]), (645, [0, 2, 4, 1, 3, 0]), (650, [0, 1, 3, 2, 4, 0]), (660, [0, 2, 3, 1, 4, 0]), (660, [0, 3, 1, 2, 4, 0]), (665, [0, 1, 4, 2, 3, 0]), (670, [0, 1, 2, 4, 3, 0]), (670, [0, 4, 1, 2, 3, 0]), (685, [0, 2, 3, 4, 1, 0]), (810, [0, 3, 2, 4, 1, 0]), (815, [0, 2, 4, 3, 1, 0]), (820, [0, 4, 2, 3, 1, 0])])
        self.assertListEqual(self.hillClimberTSP.getOptimalTour(),[0, 2, 1, 3, 4, 0])
        self.assertEqual(self.hillClimberTSP.getOptimalD(),335)
        self.assertEqual(self.hillClimberTSP.getWorstTour(),[0, 4, 2, 3, 1, 0])
        self.assertEqual(self.hillClimberTSP.getworstD(),820)
        self.assertEqual(self.hillClimberTSP.getLength(),5)
        self.assertEqual(self.hillClimberTSP.getTime(),42)
        self.assertEqual(self.hillClimberTSP.getIter(),666)        
        print "gets Testing Complete"        
        
#------------------------------------------------------------------------------   
    def test_getSolved(self):
        print "Testing getSolved"
        self.assertFalse(self.hillClimberTSP.getSolved())
        self.hillClimberTSP._solved = True
        self.assertTrue(self.hillClimberTSP.getSolved())
        print "getSolved Testing Complete"
        
        
#==============================================================================        
        
        
class LocalImproverHCTestCase(unittest.TestCase):
    
    def setUp(self):      
        print "Setting up test...\n"
        self.row1 = [0,20,15,10,20]
        self.row2 = [200,0,50,30,45]
        self.row3 = [40,20,0,200,200]
        self.row4 = [200,200,200,0,70]    
        self.row5 = [200,200,200,200,0]  
        self.distanceMatrix = np.array([self.row1,self.row2,self.row3,self.row4,self.row5])
        self.locations = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
        self.hillClimberTSP = LocalImproverHC(self.distanceMatrix)
    
    def tearDown(self):
        self.row1 = None
        self.row2 = None
        self.row3 = None
        self.row4 = None  
        self.row5 = None
        self.distanceMatrix = None
        self.hillClimberTSP.fullReset()
        print "\n...test complete.\n\n"
        print "          ###############################\n\n"        

#------------------------------------------------------------------------------        
    def test_localImprover(self):
        print "Testing Local Improver"
        self.hillClimberTSP.solve(50,v=0)
        self.assertEqual(6,len(self.hillClimberTSP._bestTour))
        self.assertGreaterEqual(self.hillClimberTSP._bestD,335)
        print "Local Improver Testing Complete"    
        

#==============================================================================             
        
        
class GlobalHCTestCase(unittest.TestCase):
    
    def setUp(self):      
        print "Setting up test...\n"
        self.row1 = [0,20,15,10,20]
        self.row2 = [200,0,50,30,45]
        self.row3 = [40,20,0,200,200]
        self.row4 = [200,200,200,0,70]    
        self.row5 = [200,200,200,200,0]  
        self.distanceMatrix = np.array([self.row1,self.row2,self.row3,self.row4,self.row5])
        self.locations = {1: 'a', 2: 'b', 3: 'c', 4: 'd'}
        self.hillClimberTSP = GlobalHC(self.distanceMatrix)
    
    def tearDown(self):
        self.row1 = None
        self.row2 = None
        self.row3 = None
        self.row4 = None  
        self.row5 = None
        self.distanceMatrix = None
        self.hillClimberTSP.fullReset()
        print "\n...test complete.\n\n"
        print "          ###############################\n\n"        

#------------------------------------------------------------------------------        
    def test_globalHC(self):
        print "Testing globalHC"
        self.hillClimberTSP.solve(10,10,v=0)
        self.assertEqual(6,len(self.hillClimberTSP._bestTour))
        self.assertGreaterEqual(self.hillClimberTSP._bestD,335)
        print "Local globalHC Testing Complete"
  
        

#==============================================================================            
        

if __name__ == "__main__":
    unittest.main()
    