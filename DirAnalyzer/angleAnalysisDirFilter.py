# -*- coding: utf-8 -*-
"""
Created on Fri Sep 12 15:34:09 2014
@author: pankaj
"""

import cv2 as cv
import numpy as np
from os import listdir
from os.path import isfile, join
from matplotlib import pyplot as plt

import sys
sys.path.insert(1,join('..','ThirdParty','python-emd'))

from dirFilter2D import GetAngleAssignment, dirFilter2D
#from calculateEMDMetric import calculateEMDMetric

#this is the metric for EMD
def distance(x,y):
    angleDistance=np.abs(x-y)
    return np.minimum(angleDistance,np.abs(180-angleDistance))
def calOrientationViaDF(mypath, ac):
  """
  This function caluclates orientation using dirctional filters
  mypath:- path of directory containing roi and segmented files
  ac:- configuration dictionary for directional filters and algorithms
  """
  
  # this is for removing small components
  thrSz=20
  mSize=80
  nBands=36 #Verify from matlab code
  thrSz = ac['thrSmallComp']
  mSize = ac['dirFilterSz']
  nBands = ac['dirFilterNum']
  roifiles = [ f for f in listdir(mypath) if isfile(join(mypath,f)) and f.endswith('_roi.tif')]
  #histogramContainer for WT(first list) and KO files(second list)
  histContainer=[[],[]]

  #This loops build angle based histogram for WT and KO in respective container
  for i, roiFile in enumerate(roifiles):


      shearDenoised = cv.imread(join(mypath,roiFile.replace('_roi.tif','_shd.tif')),cv.IMREAD_GRAYSCALE)
      plt.imshow(shearDenoised)
      plt.title('2D shearlet Denoised: '+ roiFile.replace('_roi.tif','_shd.tif'))
      plt.show()

      segMask=cv.imread(join(mypath,roiFile.replace('_roi.tif','_seg.tif')),cv.IMREAD_GRAYSCALE)
      plt.imshow(segMask)
      plt.title('Segmented File: ' + roiFile.replace('_roi.tif','_seg.tif'))
      plt.show()

      roiMask=cv.imread(join(mypath,roiFile),cv.IMREAD_GRAYSCALE)
      plt.imshow(roiMask)
      plt.title('ROI MASK:' + roiFile)
      plt.show()

      segMask1=segMask.copy()
      (_,cnts, _)=cv.findContours(segMask.copy() ,cv.RETR_TREE,cv.CHAIN_APPROX_SIMPLE)
      for i,cts in enumerate(cnts):
         area=cv.contourArea(cts)
         if area> 0 and area <=thrSz:
            cv.drawContours(segMask,cnts,i,(0,0,0))

      xMask=roiMask*segMask
      plt.imshow(xMask)
      plt.title('Segmented and ROIed file ' +
                 roiFile.replace('_roi.tif', '_seg.tif'))
      plt.show()

      dirFilters,angles=dirFilter2D(mSize,nBands)
      DirectionalOutput=[cv.filter2D(xMask,cv.CV_64F,dirFilter) for dirFilter in dirFilters]
      collectDirOutputsAs3D=np.dstack(DirectionalOutput)
      #TO DO  fix filtering issue cv2. remove .0001 magicnumber
      collectDirOutputsAs3D[collectDirOutputsAs3D<.00001]=0;
  #    for i in range(nBands):
  #        plt.imshow(DirectionalOutput[i])
  #        plt.show()

      maximumResponseAngles=180-np.argmax(collectDirOutputsAs3D,axis=2)*180/nBands
      plt.imshow(maximumResponseAngles)#,cmap=plt.cm.gray)
      plt.title(roiFile)
      plt.set_cmap('hot')
      plt.ylim((0,1000))
      plt.colorbar()
      plt.clim(0,180)
      plt.show()

      Mask=maximumResponseAngles*xMask

      plt.imshow(Mask)#,cmap=plt.cm.gray)
      plt.title(roiFile)
      plt.set_cmap('hot')
      plt.ylim((0,1000))
      plt.colorbar()
      plt.clim(0,180)
      plt.show()    

      hist, bins = np.histogram(maximumResponseAngles[xMask==1], bins=nBands, density=True)
      widths = np.diff(bins)
      histplt=hist/np.sum(hist*widths)
      if roiFile.find('WT') >=0:
          histContainer[0].append((roiFile,histplt))
      else:
          histContainer[1].append((roiFile,histplt))

      plt.bar(bins[:-1], histplt, widths)
      plt.show()


  # Calculate rotation invariant emd in same population and across polutation
  #first among WT
  #emdMetricWT={}
  #angles=GetAngleAssignment(nBands)
  #minVal=1000000000
  #
  #emdMetricWT= calculateEMDMetric(histContainer[0], histContainer[0],angles,distance)
  #emdMetricKO= calculateEMDMetric(histContainer[1], histContainer[1],angles,distance)
  #emdMetricWTKO= calculateEMDMetric(histContainer[0], histContainer[1],angles,distance)
  #
  #
  #wtEMDList=[]
  #for dummy,val in emdMetricWT.items():
  #  for v in val:
  #    wtEMDList=wtEMDList+[v[1]]
  #    
  #print('mean of WT-WT mean {0}  std {1}'.format(np.mean(wtEMDList),np.std(wtEMDList)))
  #
  #koEMDList=[]
  #for dummy,val in emdMetricKO.items():
  #  for v in val:
  #    koEMDList=koEMDList+[v[1]]
  #print('mean of KO-KO mean {0}  std {1}'.format(np.mean(koEMDList),np.std(koEMDList)))
  #
  #wtKoEMDList=[]
  #for dummy,val in emdMetricWTKO.items():
  #  for v in val:
  #    wtKoEMDList=wtKoEMDList+[v[1]]
  #print('mean of WT-KO mean {0}  std {1}'.format(np.mean(wtKoEMDList),np.std(wtKoEMDList)))
  #
  #aWT=[]
  #for fileName1,histVal1 in histContainer[0]:
  #    for fileName2,histVal2 in histContainer[0]:
  #        minVal=1000000000;
  #        for rotNum in range(len(angles)):
  #            anglesR=rotate(angles,rotNum)
  #            cVal= emd((angles,histVal1.tolist()),(anglesR,histVal2.tolist()),distance)
  #            if cVal < minVal:
  #              minVal=cVal
  #        if emdMetricWT.get(fileName1) == None:
  #            emdMetricWT[fileName1]=[]
  #        emdMetricWT[fileName1].append((fileName2,minVal))
  ##        aWT.append(minVal)
  #
  #aKO=[]
  #for fileName1,histVal1 in histContainer[1]:
  #    for fileName2,histVal2 in histContainer[1]:
  #        minVal=1000000000;
  #        for rotNum in range(len(angles)):
  #            anglesR=rotate(angles,rotNum)
  #            cVal= emd((angles,histVal1.tolist()),(anglesR,histVal2.tolist()),distance)
  #            if cVal < minVal:
  #              minVal=cVal
  #        if emdMetricWT.get(fileName1) == None:
  #            emdMetricWT[fileName1]=[]
  #        emdMetricWT[fileName1].append((fileName2,minVal))
  #        aKO.append(minVal)
  #                 
  #print 'WT Stats'
  #print np.mean(aWT)
  #print np.std(aWT)
  #        
  #print 'KO Stats'
  #print np.mean(aKO)
  #print np.std(aKO)
  #        
  #
  #    
  #    plt.imshow(xMask)
  #    plt.title('BandNumber')
  #    plt.show()

if __name__ == '__main__':
  mypath = '/home/psnegi/Data/MusaadWTKO/UH_New-DCX_63X-Images_Max-Projections'
  ac = {}
  ac['thrSmallComp'] = 20
  ac['dirFilterSz'] = 80
  ac['dirFilterNum'] = 36 #Verify from matlab code
  calOrientationViaDF(mypath, ac)
    


