# -*- coding: utf-8 -*-
"""
Created on Wed Nov 11 22:29:24 2015

@author: pankaj
"""

from skimage.filters import threshold_otsu
from skimage.filters import gaussian_filter
import matplotlib.pyplot as plt
from skimage import io
from os import listdir
from os.path import isfile, join
import numpy as np
import cv2 as cv

path = '.\Data\AngleJ_data\DataSet1'
filename='1.png'
img=io.imread(join(path,filename))
thr=threshold_otsu(img)
segImg = np.zeros((img.shape[0], img.shape[1]), dtype=np.uint8)
mask = (img < thr*0.8)
segImg[~mask] = 255

#io.imsave(join(path,'seg_'+filename),segImg)

blurredImg=cv.GaussianBlur(img,2,2)

plt.imshow(img)
plt.colorbar()
plt.show()

plt.imshow(blurredImg)
plt.colorbar()
plt.show()

plt.imshow(segImg)
plt.show()

plt.imshow(blurredImg>120)
plt.colorbar()
plt.show()