# -*- coding: utf-8 -*-
"""
Created on Thu Sep 24 14:34:42 2015

@author: pankaj
"""
import numpy as np
from matplotlib import pyplot as plt, cm
from scipy import misc


leng=15;
numSeg=30;
width=2;
initinalXcor=100;
initinalYcor=100;
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
            img[xcord-i,ycord+i-width:ycord+i+width+1]=1;
            
        
    else:
        xcord=initinalXcor;
        for i in range(leng):
            patch[xcord+i,ycord+i]=1;
            img[xcord+i,ycord+i-width:ycord+i+width+1]=1;

            
plt.imshow(patch)
plt.show()

plt.imshow(img)
plt.show()

#misc.imsave('image3.png', patch)
#misc.imsave('image4.png', img)





#plt.waitforbuttonpress()