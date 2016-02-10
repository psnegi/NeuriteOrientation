# Calculate rotation invariant emd in same population and across polutation
#first among WT
from os.path import  join
import sys
sys.path.insert(1,join('..','ThirdParty','python-emd'))
from emd import emd

def rotate(l,n):
  return l[n:]+l[:n]

def calculateEMDMetric(histContainer1, histContainer2,angles,distanceFcn):      
  emdMetricWT={}
  minVal=1000000000
  for fileName1,histVal1 in histContainer1:
    for fileName2,histVal2 in histContainer2:
      minVal=1000000000
      for rotNum in range(len(angles)):
        anglesR=rotate(angles,rotNum)        
        cVal= emd((angles,histVal1.tolist()),(anglesR,histVal2.tolist()),distanceFcn)
        if cVal < minVal:
          minVal=cVal      
      if emdMetricWT.get(fileName1) == None:
        emdMetricWT[fileName1]=[]
      emdMetricWT[fileName1].append((fileName2,minVal))
        
  return emdMetricWT                    
    
