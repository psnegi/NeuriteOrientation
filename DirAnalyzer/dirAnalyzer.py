from  __future__ import division
#import cv2 as cv
from scipy import ndimage
import numpy as np
import matplotlib.pyplot as plt
import itertools
import time
from Util.biMorpAnalysis import connectedComponents
from  Util.measures import klDiv, rotationInvariantMinMeasure

#import pycircstat as pcirc

class DirAnalyzer:
  ''' This is the main class for orientation analysis framework'''
  def  __init__(self, centerlineGen, filters):
    ''' Initilization code for this class
    INPUT:
    -fileFactory: this provies iterator like interface for image handling
    -centerlineGen: this function generator centerline for given image
    - filters: filters generator for  image analysis
    '''
    #self._ImgGen = fileFactory
    self._centGen = centerlineGen
    self._fltGen = filters

  def _buildDirMap(self, fltParam):
    '''This function builds filters and estimates orientation Map for image I'''
    
  def buildMultiScaleDirMap(self, fltParamList, fileFactory, **kwargs):
    ''' This is multiscale version where list of filters fltL are used to
    estimate orientations at an image I as per given filters  list
    INPUT:-
    - filtParamL: list of pair for (filter size, directional bands) 
    - I: Image for filter analysis
    '''
    
    directionalFilters=[(mSize,nBands,self._fltGen(mSize,nBands)) for 
                                    (mSize, nBands) in fltParamList]      
    histInformation=[]    
    for xSeg, name in fileFactory:
      # Find the connected components and process them individually
      centerLineExtStart = time.clock()
      xMask = np.zeros(xSeg.shape, dtype = np.uint8)
      conCmpsIdx = connectedComponents(xSeg, numPixels =
                              kwargs['conCompThreshold'])         
      #########################################################################
      # To get the centerline by processing each connected component
      # indivisually
      listofCLinfo=[]            
      for i, cmpIdx in enumerate(conCmpsIdx):
        xMask[:] = 0
        xMask[cmpIdx] = 1
        xCenterLine = self._centGen(xMask)         
        listofCLinfo.append(np.flatnonzero(xCenterLine))
      centerLineExtEnd = time.clock()
      centerLineExtTime = centerLineExtEnd - centerLineExtStart
      print('Centerline extraction time for file {0} is {1}'.format(
        name, centerLineExtTime ))  
      #########################################################################
      ## Get the histogram for the image at different scales
      #histContainer = [[] for i in range(0, len(fltParamList))]
      histContainer = []
      for scale, (mSize, nBands) in enumerate(fltParamList):
        angleinfo=[]
        # curDirFilters, directions = self._fltGen(mSize,nBands)
        #Relook at this
        curDirFilters=directionalFilters[scale]
        angleEstStart = time.clock()
        for i, cmpIdx in enumerate(conCmpsIdx):
          xMask[:] = 0
          xMask[cmpIdx]=1          
          # xCenterLine = self._centGen(xMask) 
          dirFilters = self._AdjustFilter(len(listofCLinfo[i]), curDirFilters,
                                                          fltParamList, scale)  
          # dirFilters = self._AdjustFilter(np.sum(listofCLinfo[i]),
          # curDirFilters, fltParamList, scale)
          directionalOutput=[ndimage.convolve(xMask, dirFilter,
            mode ='constant', cval=0.0) for dirFilter  in dirFilters[2][0]]
          collectDirOutputsAs3D=np.dstack(directionalOutput)
          #TO DO  fix filtering issue cv2. remove .0001 magicnumber
          collectDirOutputsAs3D[collectDirOutputsAs3D<.00001]=0;
          maximumResponseAngles = np.argmax(collectDirOutputsAs3D,
                                                axis=2)*180/nBands

          ### just for plotting ##
          #xMask[:] = 0
          #xMask.ravel()[listofCLinfo[i]] = 1
          #plt.imshow(maximumResponseAngles*xMask);
          #plt.colorbar(); plt.show()
          ###
#          angleinfo.append(maximumResponseAngles[xCenterLine==1])
          angleinfo.append(maximumResponseAngles[np.unravel_index(listofCLinfo[i],xMask.shape)])
#          plt.imshow(xCenterLine);plt.colorbar(); plt.show()
      
        angles = np.array(list(itertools.chain(*angleinfo)))
        angleEstEnd = time.clock()
        print('For File {} centreline + Angle estimation time at scale {} ='
                    '(mSize {}, nBands {}) is {}'.format(name, scale, mSize,
                   nBands, centerLineExtTime + angleEstEnd - angleEstStart))
        histContainer.append((nBands, mSize, angles))
      
      histInformation.append((histContainer,zip(conCmpsIdx, listofCLinfo)))
    return histInformation

  def _AdjustFilter(self, compLen, curFilters, filtParamL, curScale):
    ''' This function checks if current filter length is greater or equal to
    compponent length then it readjust the the filter to previous scale filters
    '''
    # find the right scale
    for scale, (mSize, nBands) in enumerate( reversed( # look back in scale
                        filtParamL[0:curScale + 1] ) ):
      filtWidth =  np.round((np.pi*(mSize/2.0))/nBands)
      if filtWidth >= compLen:
        continue # go down in scale
      else: # build filter with current scale
        if 0 == scale:
          return curFilters
        else:
          return mSize, nBands, self._fltGen(mSize, nBands)


    raise Exception(' could not find right filter scale for currrent comp')   

  def calculateMeasures(self, fileFactory, msMap, histRange, measureFn,
                                                             **kwargs):
    klScores = []
    
    numBands=msMap[0][0][0][0]
    #@TODO 2,180 can be replace with histRange[1] - histRange[0] ? no use case now
    binsRange = [ ((2.0*i+1)/2)*(180.0/numBands) for i in xrange(-1,numBands)]
    bins =np.array( binsRange) + histRange[0]
    #widths = np.zeros(numBands)   # @TODO not required. better way to look
    center = (bins[:-1] + bins[1:]) / 2
   # @TODO 1, review np.diff   
    widths = np.diff(bins)
    totalBins = len(widths)
    #########################################################################
    # build neutral pdf approximated by gussian pdf
    
    #mu, sigma = sum(histRange)/2, 6  # neutral pdf
    #samples = 1000
    #neuSample = np.random.normal(mu, sigma, samples)
    #neuPdf, _ = np.histogram(neuSample,bins = bins)
    #plt.hist(neuDist, len(widths), normed=True)
    #neuPdf = neuPdf/np.sum(neuPdf*widths)
    
    #########else building a hard code pdf to approximate neutral pdf#########
    # with .9 at center and rest of mass distibuted over other bins

    centerMass = .98
    neuPdf = np.array([centerMass if x ==90 else (1- centerMass)/(totalBins -1)
                                                  for x in xrange(0, 180, 10)])
    
    plt.bar(center, neuPdf/widths[0], align='center', width=widths, facecolor='c')
    plt.title('Neutral pdf  with centre probabilty {0} \n and probabilty {1} on'
      ' each of other bins'.format(centerMass,(1- centerMass)/(totalBins -1)))
    print('Total probability = {0}'.format(sum(neuPdf)))
    plt.show()
    for (xSeg, name), (histCont, _) in itertools.izip(fileFactory, msMap):
      plt.imshow(xSeg, cmap = plt.get_cmap('gray'))
      plt.title('mutliscale measures for file {0}'.format(name))
      plt.xticks([])
      plt.yticks([])
      plt.show()

      kl = []
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
        #histplt=hist1/np.sum(hist1*widths)
        histplt=hist1/np.sum(hist1)
        measureCalStart = time.clock()
        measureVal = rotationInvariantMinMeasure( histplt, neuPdf, measureFn,
                                                                    **kwargs)
        print('For File {} measure {} calculation time at scale {} ='
            '(mSize {}, nBands {}) is {}'.format(name, measureFn.__name__,
                    index, mSize, nBands, time.clock() - measureCalStart))

        
        #measureVal = klDiv()
        print('At scale {0}, bands = {1}, size = {2}  measure based on function {3} is {4}'.format(
          index,nBands, mSize, measureFn.__name__, measureVal))
        kl.append(measureVal)
      klScores.append(kl)
      
    return klScores    

  def displayMap(self, orientMap):
    ''' Displays the orientation histogram
    '''
    pass
 

#########################################################################################
##          #angles on the circle
#          indices=np.where(xCenterLine==1)
#          plt.imsave('./Data/Patches/Circle/Circle_Centerline',xCenterLine)
#          center=[287,287]
#          indices=zip(*indices)
##          angles=[np.arctan2(a[1]-center[1],a[0]-center[0]) for a in indices]
#          sortedIndices=indices.sort(key=lambda a: np.arctan2(a[1]-center[1],a[0]-center[0]))
#          indices=filter(lambda a: np.arctan2(a[1]-center[1],a[0]-center[0])>0,indices)
#          actualAng=[np.arctan2(a[1]-center[1],a[0]-center[0])*180/np.pi for a in indices]
#          estimatedAng=[maximumResponseAngles[b[0],b[1]] for b in indices]
##          fig = plt.figure()
#          plt.plot(actualAng,'r-',label='Actual Angle')
#          plt.plot(estimatedAng,'c*',label='Estimated Angle',markersize=3)
#          plt.legend(loc=2,
#           bbox_transform=plt.gcf().transFigure)
#          plt.title('Circle_ mSize'+ str(mSize) +'_numBins_ '+str(nBands)+'_bothAngles')
#          plt.show()
##          fig.savefig('./Data/Patches/Circle/Circle_ mSize'+ str(mSize) +'_numBins_ '+str(nBands)+'_Angles.png',bbox_inches='tight')
#          
#          diffAng=np.minimum(np.abs(np.array(actualAng)-np.array(estimatedAng)),
#                                    180-np.abs(np.array(actualAng)-np.array(estimatedAng)))
#          print('The mean and variance of the error (difference of angles) is '
#          + str(np.mean(diffAng)) +' and ' +str(np.var(diffAng)) +' respectively.')
##          fig = plt.figure()
#                            
#          plt.plot(diffAng,'b^',markersize=3)
#          plt.ylim(0,18)
#          plt.title('Circle_ mSize'+ str(mSize) +'_numBins_ '+str(nBands)+'_diffAngles')
#          plt.show()
##          fig.savefig('./Data/Patches/Circle/Circle_ mSize'+ str(mSize) +'_numBins_ '+str(nBands)+'_diffAngles.png',bbox_inches='tight')
#########################################################################################          
   
  
