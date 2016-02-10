import numpy as np
from os import listdir
from os.path import isfile, join
from skimage import io,external
import matplotlib.pyplot as plt


class FileFactory(object):
  def __init__(self, dirName = None, nameFilter = lambda x: True, **kwargs):
    ''' nameFilter provides extra test for file inclusion. It return True or
        False [like set nameFilter = lambda f : f.endswith('_roi.tif')]
    '''
    # @TODO need to make it exception safe due to listdir
    # @ TODO need to look into generator comprehension when used multiple time
    # Going ahead with list comprehension right now
    self.files = [ (io.imread(join(dirName,f)), f) for f in listdir(dirName) if
               isfile(join(dirName,f)) and nameFilter(f)]
    
  def __iter__(self):
    return iter(self.files)

class SyntheticLineFileFactory(FileFactory):
  def __init__(self, lineArgs =[], path = None, flt = lambda x: True, **kwargs):
    '''lineArgs:- is list of dictionary like
     [{'lenLines' : 5, 'numLines' : 50, 'angle' : 45, 'x0' : 100, 'y0' : 100}]
    '''
    if  path: # if dirName is not None pickpup prebuild files
      super(SyntheticLineFileFactory, self).__init__(dirName = path, nameFilter = flt, **kwargs)
    else:
      self.files = []
      for line in lineArgs:
        leng = line['lenLines']
        numSeg = line['numLines']
        initinalXcor = line['x0']
        initinalYcor = line['y0']
        siz=leng*numSeg+initinalXcor+initinalYcor;
        patch=np.zeros((siz,siz));
        img=np.zeros((siz,siz));
        seg=range(numSeg)

        for index in seg:
            ycord=initinalYcor+index*leng;
            if seg[index]%2 ==0:
                xcord=initinalXcor+leng;
                for i in range(leng):
                    patch[xcord-i,ycord+i]=1;
                    img[xcord-i,ycord+i-1:ycord+i+2]=1;


            else:
                xcord=initinalXcor;
                for i in range(leng):
                    patch[xcord+i,ycord+i]=1;
                    img[xcord+i,ycord+i-1:ycord+i+2]=1;
                    
        self.files.append((img, 'linewith' + 'Len' + str(leng) + 'Pixel' +
                                                 'Segment' + str(numSeg)))


