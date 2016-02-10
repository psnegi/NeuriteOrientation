# -*- coding: utf-8 -*-
"""
Created on Tue Nov 17 18:38:03 2015

@author: pankaj
"""

import numpy as np
import csv
import collections
from matplotlib import pyplot as plt
import pycircstat as pcirc
import itertools
from skimage import io
import os

#fpath='./Data/Patches/AISDataImages/TestImage1/Patch1/'
#fname='C3-MAX_220WTm_T1_NeuNg_Caspase-3r_AnkyrinGm_CA1_63X_St-6'
fpath=os.path.normpath("./Data/Synthetic/AngleJ_Experiment_Hist/")
fname='Image4.png'
#Sigma=9
ylimit=0.1
for sigma in range(9):
  Sigma=sigma+1
  

  img=io.imread(os.path.join(fpath,fname))
  
  plt.imshow(img)
  plt.title('Original Image')
  plt.show()
  
  
  f = open(os.path.join(fpath,fname+'_Sigma_'+str(Sigma)+'.txt'), "r")
  lines = f.readlines()
  f.close()
  histInformation=[]
  for row in lines[2:-6]:
  #        print row
          splitrow=row.split(';')
  #        print ab
          collectrow=(int(splitrow[0]),float(splitrow[1]),float(splitrow[2]),int(splitrow[3]))
  #        print ac
          histInformation.append(collectrow)
  
  binNum, lBin,uBin, freq=zip(*histInformation)
  
  bins=(np.array(lBin)+np.array(uBin))/2
  
  hist1=np.array(freq)
  
  widths = np.ones(len(bins))*(bins[1] - bins[0])
  histplt=hist1/np.sum(hist1*widths)
  
  
  newAngles=[bins[i]*np.ones(freq[i]) for i in xrange(len(bins))]
  angles = np.array(list(itertools.chain(*newAngles)))
  
  mean=(0.5)*pcirc.mean(2*np.array(angles)*np.pi/180)
  var=pcirc.var(2*np.array(angles)*np.pi/180)
  
  meanIndegrees=mean*180/np.pi
  if meanIndegrees > 90:
    meanIndegrees=-180+meanIndegrees
    
  print('The circular mean and variance are ' + str(meanIndegrees)+
  ' and ' + str(var) +' respectively.' )
  
  
  histName='Histogram_Sigma_'+str(Sigma)+'_mean'+str(round(meanIndegrees,2))+'_var_'+str(round(var,2))+'.png'
  
  fig=plt.figure()
  plt.bar(bins, histplt, align='center', width=widths,facecolor='r')
  plt.ylim(0,ylimit)
  #plt.title('At Scale: '+ str(index)+'_msize_'+str(mSize) + 'Angles density') 
  plt.show()
  fig.savefig(os.path.join(fpath,fname[:-4]+histName),bbox_inches=None)


#
#histInformation = collections.namedtuple('histInformation',
#                                         'BinNum, lowerBinLim, upperBinLim, binHeight, junk')
#                                                    
#                                                     
#g=fpath+'C3-MAX_220WTm_T1_NeuNg_Caspase-3r_AnkyrinGm_CA1_63X_St-6.tif.txt'
#for emp in map(histInformation._make, csv.reader(open(g, "rb"))):
#    print emp.BinNum, emp.lowerBinLim