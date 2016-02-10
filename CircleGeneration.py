# -*- coding: utf-8 -*-
"""
Created on Tue Oct 20 17:13:19 2015

@author: pankaj
"""

from skimage.draw import circle
from skimage import io
import numpy as np
from matplotlib import pyplot as plt
import scipy as sc


#center=(100,100);
radius1=200;
radius2=205;
siz=np.round(2*radius2*1.40);
img1=np.zeros((siz,siz));
img2=np.zeros((siz,siz));
center=np.round([siz/2,siz/2]);

rr1, cc1 = circle(center[0],center[1], radius1)
img1[rr1, cc1] = 1

rr2, cc2 = circle(center[0],center[1], radius2)
img2[rr2, cc2] = 1

circ=sc.logical_xor(img2,img1)
circ.astype(int)

plt.imshow(img1)
plt.show()
io.imshow(img2)
io.imshow(circ)
io.imsave('Circle_radius'+str(radius1)+'.png',circ)


 #          #angles on the circle
#          indices=np.where(xCenterLine==1)
##          randperm=np.random.permutation(len(indices[0]))
#          randperm=range(len(indices[0]))
#          
#          #consider 2% random points on the circle
#          numPts=np.ceil(1.00*len(randperm))
#          numPts=numPts.astype(int)
#          circAngle=np.zeros(numPts, dtype = np.float)
#          filteredAngle=np.zeros(numPts, dtype = np.float)
#          for pt in range(numPts):
#              circAngle[pt]=np.arctan2(120-indices[1][randperm[pt]],indices[0][randperm[pt]]-120)*180/np.pi
#              filteredAngle[pt]=maximumResponseAngles[indices[0][randperm[pt]],indices[1][randperm[pt]]]
#              
#          posAng=circAngle*(circAngle>0)
#          negAng=circAngle*(circAngle<0)
#          newNegAng=negAng+180
#          newNegAng=newNegAng*(circAngle<0)
#          convAng=180-(posAng+newNegAng)
##          fig = plt.figure()
#          plt.plot(convAng,'r',label='Actual Angle')
#          plt.plot(filteredAngle,'b',label='Estimated Angle')
#          plt.legend()
#          plt.show()
##          fig.savefig('./Data/Circle_At Scale_'+ str(scale) + 'CompareAngles.png',bbox_inches='tight')
#          diffAng=np.minimum(np.abs(convAng-filteredAngle),180-np.abs(convAng-filteredAngle))
##          fig = plt.figure()
#          plt.plot(diffAng)
#          plt.show()
##          fig.savefig('./Data/Circle_At Scale_'+ str(scale) + 'AngleDiff.png',bbox_inches='tight')