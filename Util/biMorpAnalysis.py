from skimage import data
from matplotlib import pyplot as plt
import numpy as np
from skimage import measure, io


def connectedComponents1(mask,numPixels):
    #finding the connected components and labeling each component
    #with a different label; the option 'background=0' labels background
    #pixels as -1
    connComp=measure.label(mask,background=0)
    
    
    for comp in range(connComp.max()+1):
        newMask=(connComp==comp);
        
        if np.size(np.where(connComp==comp)[1])> numPixels:
            #Right now, we are just creating the place holders
            #we could replace it by histogram or whatever we 
            #would like to replace by
            all_Con_Comp=newMask;
            
    return all_Con_Comp

def connectedComponents(mask, numPixels = 0):
    #finding the connected components and labeling each component
    #with a different label; the option 'background=0' labels background
    #pixels as -1
    connComp=measure.label(mask,background=0)
    
    #indexContainer = [[] for i in range(connComp.max()+1)]
    indexContainer = []
    #collecting indices of each connected component
    for comp in range(connComp.max()+1):
        #newMask=(connComp==comp);
        one_Con_Comp=np.where(connComp==comp);
        if np.size(one_Con_Comp[1])> numPixels:
            #Right now, we are just creating the place holders
            #we could replace it by histogram or whatever we 
            #would like to replace by
            indexContainer.append(one_Con_Comp)
            
    return indexContainer

  
def connectedComponents2(mask,pixelsThr = 0):
    ''' take imput mask and return the indices of connected components
    if size if component is more thna numPixels
    '''    
    #finding the connected components and labeling each component
    #with a different label; the option 'background=0' labels background
    #pixels as -1
    componentsIdx = []
    connComp=measure.label(mask,background=0)
    for comp in range(connComp.max()+1):
        newMask=(connComp==comp);
        if np.size(np.where(connComp==comp)[1])> pixelsThr:
            #Right now, we are just creating the place holders
            #we could replace it by histogram or whatever we 
            #would like to replace by
            componentsIdx.append(newMask.nonzero())
            
    return componentsIdx

  
if __name__ == '__main__':
  #just to test if the idea works:

  fpath='C:\Users\pankaj\Documents\AngleAnalysis'

  fname=fpath +'\\C3-testImage.tif'


  testBlue=io.imread(fname);
  #Segmentation by Thresholding 
  testSeg=testBlue>2*testBlue.mean()

  #getting the connected components and doing whatever we would 
  #like to do

  all_the_con_comp=connectedComponents(testSeg,100)



