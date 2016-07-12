# -*- coding: utf-8 -*-
"""
Created on Sun Nov 11 17:35:18 2014

@author: nrjh
"""

import GeoFuncs as gf
import matplotlib.pyplot as mp
from Polylines import Polyline
from Points import Point2D
from ChainHandler import ChainLoader

class PointPlotter(object):
    
    
                

    def PointFieldScatter(self,pointField,colour = 'black',
                          size = 10,symbol='o',legend=""):
        x=[]
        y=[]
        ap=pointField.getPoints()
        
        for point in ap:
            x.append(point.get_x())
            y.append(point.get_y())
        mp.scatter(x,y,color=colour,s=size,
                   marker=symbol,label=legend)
    
    def show(self, title="", xlabel="", 
        ylabel="", grid=False):
        mp.title(title)          
        mp.xlabel(xlabel)
        mp.ylabel(ylabel)
        mp.grid(grid)
        mp.show() 
    
    def legend(self,**kwargs):
        mp.legend(**kwargs)
    #end of function plotPoints
    
    def plotPoint(self,point,colour='black'):
        if isinstance(point,Point2D):
            mp.scatter([point.get_x()],[point.get_y()],color=colour)
        elif isinstance(point,list):
            x=[]
            y=[]
            for p in point:
                if isinstance(p,Point2D):
                    x.append(p.get_x())
                    y.append(p.get_y())
            mp.scatter(x,y,color=colour)
    
    def set_axis(self,xlo,xhi,ylo,yhi):
        mp.axis([xlo,xhi,ylo,yhi])
        mp.axis("equal")
        
    def clf(self):
        mp.clf()
    
    def plotVector(self,p1,p2,colour='black'):
        xs=[p1.get_x(),p2.get_x()]
        ys=[p1.get_y(),p2.get_y()]
        mp.plot(xs,ys,color=colour)
        
    def plotSegment(self,seg,colour='black'):
        p1=seg.getStart()
        p2=seg.getEnd()
        xs=[p1.get_x(),p2.get_x()]
        ys=[p1.get_y(),p2.get_y()]
        mp.plot(xs,ys,color=colour)
        
    def plotBox(self,box,colour='black'):
    
        xs=[box[0],box[0],box[2],box[2],box[0]]
        ys=[box[1],box[3],box[3],box[1],box[1]]
        
        mp.plot(xs,ys,color=colour)
     
        
    def plotPolylines(self,chains,colour='black',width=1,legend=""):
        if isinstance(chains,Polyline):
            xys=chains.getPointsAsLists()
            mp.plot(xys[0],xys[1],color=colour,linewidth=width,
                label=legend)
        elif isinstance(chains,list):
            for chain in chains:
                if isinstance(chain,Polyline):
                    xys=chain.getPointsAsLists()
                    mp.plot(xys[0],xys[1],color=colour,linewidth=width,
                label=legend)   
                    
    def plotCities(self,cities,colour='red',size = 50,symbol='o',labels=False):
        """argument is a list of lists where each list in the 
        primary list city name, latitude, longitude returns a 
        closed loop finishing at original city"""
        for city in cities:
            mp.scatter(city[2],city[1],color=colour,s=size,marker=symbol)
            if labels:
                mp.annotate(city[0],(city[2],city[1]),bbox=dict(boxstyle="round,pad=.2",fc="0.95"))
    
    def plotWorld(self,g = 0, c='black'):
        """method to plot global country borders"""
        
        print '\nplotting global outline'
        all_lines=ChainLoader('global_borders_ungen.txt')
        
        if g != 0:
            summer=0
            for line in all_lines:
                summer+=line.size()
            #print 'Original data contains ',str(summer),' nodes'
            gen_lines=[]
            print 'Generalising'
            for line in all_lines:
                gen_lines.append(line.generalise(g))
            summer=0
            for line in gen_lines:
                summer+=line.size()
            #print 'Generalised data contains ',str(summer),' nodes'
            #print 'Plotting'
            self.plotPolylines(gen_lines, colour = c)
            print 'world plotted\n'
        else:
            self.plotPolylines(all_lines, colour = c)
            print 'world plotted\n'
    
    def plotRoute(self, route, nodeInfo, routeWidth=5, c='red', legend=""):
        """method that takes route as a valid TSP solution path type list of 
        ints, or as list of lists, nodeInfo must be a list of lists, with each item of the primary list being 
        a list: [cityname, latitude, longitude,......].
        routewidth is route width, c is route colour legend is lenged."""
        
        routePL = gf.routeToPolyline(route, nodeInfo)
        self.plotPolylines(routePL, colour = c, width = routeWidth, 
                               legend = legend)

if __name__ == "__main__":
    
    pp = PointPlotter()
    pp.plotWorld()
    pp.show()
    
