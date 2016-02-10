# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 22:26:00 2015

@author: pankaj
"""

##########################
import pickle
import numpy as np
import matplotlib.pyplot as plt
import pycircstat as pcirc
import itertools

########################################
#f = open('AngleJ_seg_1.pckl', 'w')
#pickle.dump(msMap, f)
#f.close()
#f = open('AngleJ_seg_5.pckl') 
#f = open('TestImage1_Patch_1_test3.pckl')
#msMap = pickle.load(f)
#f.close()  
########################################
#
def drawHistograms(fileFactory, msMap, histRange):
  '''
  INPUT: histRange : (start, end) angle of histogram
         msMap:
  '''
  numBands=msMap[0][0][0][0]
  #@TODO 2,180 can be replace with histRange[1] - histRange[0] ? no use case now
  binsRange = [ ((2.0*i+1)/2)*(180.0/numBands) for i in xrange(-1,numBands)]
  bins =np.array( binsRange) + histRange[0]
  #widths = np.zeros(numBands)   # @TODO not required. better way to look
  center = (bins[:-1] + bins[1:]) / 2
 # @TODO 1, review np.diff   
  widths = np.diff(bins)
  maxYLimit = _estimateYLimit(msMap, histRange, bins, widths)
  for (xSeg, name), (histCont, _) in itertools.izip(fileFactory,msMap):
    #@TODO May be need tom kae color map a parameter
    plt.imshow(xSeg, cmap = plt.get_cmap('gray'))
    plt.title('mutliscale directional histogram for file {0}'.format(name))
    plt.xticks([])
    plt.yticks([])
    plt.show()
    for index, (nBands, mSize, newAngles) in enumerate(histCont):
    #  hist=msMap[index][0][0] # histogram information
    #  newAngles=msMap[index][0][1] # angle information between 0 and 180 degrees
      ## converting angles to angles between -90 and 90 degrees
      if histRange == (-90, 90):
        newAngles1=[-180+angle for angle in newAngles if angle>90]
        newAngles2=[angle for angle in newAngles if angle<=90]
        newAngles=newAngles1+newAngles2
        
        
      #mSize=msMap[index][0][2]

      hist1, bins = np.histogram(newAngles,bins = bins)
      histplt=hist1/np.sum(hist1*widths)

      plt.bar(center, histplt, align='center', width=widths,facecolor='c')
      plt.ylim(0, maxYLimit)
      plt.title('At Scale: '+ str(index)+'_msize_'+str(mSize) + 'Angles density') 
      plt.show()

      print('Total number of pixels on the centerline is = {}'.format(len(newAngles)))
      mean=(0.5)*pcirc.mean(2*np.array(newAngles)*np.pi/180)
      var=pcirc.var(2*np.array(newAngles)*np.pi/180)
      print('The circular mean and variance are ' + str(-180+mean*180/np.pi)+
      ' and ' + str(var) +' respectively.' )



def _estimateYLimit(msMap, histRange, bins, widths):
  maxYLimit = 0
  for histCont, _ in msMap:
    for index, (nBands, mSize, newAngles) in enumerate(histCont):
      #  hist=msMap[index][0][0] # histogram information
      # newAngles=msMap[index][0][1] # angle information between 0 and 180 degrees
      ## converting angles to angles between -90 and 90 degrees
      if histRange == (-90, 90):
        newAngles1=[-180+angle for angle in newAngles if angle>90]
        newAngles2=[angle for angle in newAngles if angle<=90]
        newAngles=newAngles1+newAngles2


      #mSize=msMap[index][0][2]

      hist1, bins = np.histogram(newAngles,bins = bins)
      histplt=hist1/np.sum(hist1*widths)
      maxVal = np.max(histplt)
      if maxYLimit < maxVal:
        maxYLimit = maxVal
  return maxYLimit    

        
######################################################################  
#def histogramFromData(angleData,numBins,title,ylimit,**kwargs):
#  
#  ''' This function plots the histograms of angles with the number of bins
#        equal to numBins, assuming the angles are between 0 and 180.    
#  '''
#  binsRange = [ ((2.0*i+1)/2)*(180.0/numBins) for i in xrange(-1,numBins)]
#  bins =np.array( binsRange)
#  hist1, bins = np.histogram(angleData,bins = bins)
#  histplt=hist1/np.sum(hist1*widths)
#  plt.bar(center, histplt, align='center', width=widths,facecolor='c')
#  plt.ylim(0,ylimit)
#  plt.title(title) 
#  plt.show()
#  
#  print('Total number of pixels on the centerline is = {}'.format(len(angleData)))
#  mean=(0.5)*pcirc.mean(2*np.array(angleData)*np.pi/180)
#  var=pcirc.var(2*np.array(angleData)*np.pi/180)
#  print('The circular mean and variance are ' + str(mean*180/np.pi)+
#  ' and ' + str(var) +' respectively.' )  
#  
  

    
  
