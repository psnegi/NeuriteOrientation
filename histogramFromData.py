# -*- coding: utf-8 -*-
"""
Created on Fri Nov 20 00:38:16 2015

@author: pankaj
"""
import numpy as np
import matplotlib.pyplot as plt
import pycircstat as pcirc


def histogramFromData(angleData,numBins,**kwargs):
  
  ''' This function plots the histograms of angles with the number of bins
        equal to numBins, assuming the angles are between 0 and 180.    
  '''
  kwargs = {'title': 'Bobby', 'ylimit': 0.1}
  binsRange = [ ((2.0*i+1)/2)*(180.0/numBins) for i in xrange(-1,numBins)]
  bins =np.array( binsRange)
  hist1, bins = np.histogram(angleData,bins = bins)
  widths = np.zeros(numBins)   # @TODO not required. better way to look
  center = (bins[:-1] + bins[1:]) / 2
  widths = np.diff(bins)
  histplt=hist1/np.sum(hist1*widths)
  plt.bar(center, histplt, align='center', width=widths,facecolor='c')
  plt.ylim(0,kwargs['ylimit'])
  plt.title(kwargs['title']) 
  plt.show()
  
  print('Total number of pixels on the centerline is = {}'.format(len(angleData)))
  mean=(0.5)*pcirc.mean(2*np.array(angleData)*np.pi/180)
  var=pcirc.var(2*np.array(angleData)*np.pi/180)
  print('The circular mean and variance are ' + str(mean*180/np.pi)+
  ' and ' + str(var) +' respectively.' )  
  
#histogramFromData(angleData,numBins,title,ylimit,**kwargs)