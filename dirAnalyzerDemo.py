# standard import
from __future__ import division 
import numpy as np
import pickle
import skimage.morphology as skiMorph

# projects based imports
from DirAnalyzer.dirAnalyzer import DirAnalyzer
import DirAnalyzer.drawHistograms_measurements as drawHist
from DirFilter.dirFilter2D import GetAngleAssignment, dirFilter2D
from Data.fileFactory import SyntheticLineFileFactory
import Util.geometry as gm
import Util.measures as msr
  
def main():

  # pass the path of directory containing segmented images
  fileFactory = SyntheticLineFileFactory(path = './Data/Hippocampus/Seg', flt =  lambda x: x.endswith('.png'))
#  fileFactory = SyntheticLineFileFactory(path = './Data/Synthetic')
  
  dirAnalyzer = DirAnalyzer(skiMorph.skeletonize, dirFilter2D )
  # we can utilize this estimate of neurites widths and lengths
  # for building filter width
  minWidth, maxWidth , minLength, maxLength= gm.estimateScaleRange(fileFactory,
                                                                           10)
  # build  number of scales to use
  # in this example filters are build  for 3 scale with
  # size 36, 54 and 72
  # but minWidth, maxWidth , minLength, maxLength can also be used to decide
  # appropriate scale and filter size
  numStep = 4
  startStep, endStep, stepSz = 36, numStep*18, 18
  filtSzList = xrange(startStep, endStep+1, stepSz)
  dirBands = [18]*((endStep - startStep)//stepSz +1)
  algoConfig = {'conCompThreshold': 30}
  # Build multiscale directional map using directional filters
  # based estimation of orientation along centerline of neurites
  msMap = dirAnalyzer.buildMultiScaleDirMap(zip(filtSzList, dirBands),
                                              fileFactory, **algoConfig)
  histSaveDataFile = 'store.pckl'
  with open(histSaveDataFile, 'w') as f:
    pickle.dump(msMap, f)

  histRange = (0, 180)
  drawHist.drawHistograms(fileFactory, msMap, histRange)
  klDivScore = dirAnalyzer.calculateMeasures(fileFactory, msMap, histRange, msr.klDiv)
  print klDivScore
  # emd calculation
  numBands=msMap[0][0][0][0]
  
  # build distance matrix
  distMat =  np.fromfunction(lambda i ,j : np.minimum( 10*np.abs(i-j), 180 -10*np.abs(i-j)), (numBands, numBands) )
  emdScore = dirAnalyzer.calculateMeasures(fileFactory, msMap, histRange, msr.emdDist, distanceMatrix = distMat)
  print emdScore
  print('Normalized by 45 EMD score are')
  print np.array(emdScore)/45.0

  l2Score = dirAnalyzer.calculateMeasures(fileFactory, msMap, histRange, msr.L2Dist)
  print l2Score
  
  return msMap


if __name__ == '__main__':
    main()  
