# -*- coding: utf-8 -*-
"""
Created on Sun Oct 11 21:35:48 2015

@author: pankaj
"""

import numpy as np
import math
import cv2 as cv
from matplotlib import pyplot as plt
import scipy as sc
"""
dirFilter2D this function calculates the direction filter
  Arg:
    mSize: size of filter
    nBands: number of  bands
    Output
    filts: filter list
    dirs:  contains x,y coordinate of the unit circle

"""
def dirFilter2D(mSize,nBands):
    filts=[]
    dirs=np.zeros((2,nBands),np.float)
    theta=np.array(range(nBands))*math.pi/nBands
    rho=np.ones(nBands)
    X,Y=cv.polarToCart(rho,theta)
    #X=np.cos(theta)
    #Y=np.sin(theta)
    dirs[0,:] =X.transpose()
    dirs[1,:] =Y.transpose()
    for k in np.array(range(nBands),np.float): 
       ang1 = (k-0.5)*math.pi/nBands;
       ang2 = (k+ 0.5)*math.pi/nBands;
       theta = np.array([ang1, ang2, ang1, ang2, ang1],float)
       if flag==0:
           #triangular section generation
           Ang1=k*math.pi/nBands;
           Ang2=(k+1)*math.pi/nBands;
           Theta=np.array([Ang1,Ang2],float)
           Rho1=np.array([1,1],float)*math.floor(mSize/2)
        #       xCor,yCor=cv.polarToCart(Rho,Theta)
           x=Rho1*np.cos(Theta)+math.ceil(mSize/2)
           y=Rho1*np.sin(Theta)+math.ceil(mSize/2)
           
           Mask1=np.zeros((mSize,mSize),np.float)
           polyVerticesTemp=np.array(np.round([[x[0],y[0]],[x[1],y[1]],[mSize/2,mSize/2]]),np.int32)
        #       polyVertices=polyVerticesTemp.reshape(2,3)
        #       polyVerticesNew=polyVertices.transpose()
           Mask1=cv.fillConvexPoly(Mask1, polyVerticesTemp, 1)
           
           Rho2=np.array([-1,-1],float)*math.floor(mSize/2)
        #       xCor,yCor=cv.polarToCart(Rho,Theta)
           x=Rho2*np.cos(Theta)+math.ceil(mSize/2)
           y=Rho2*np.sin(Theta)+math.ceil(mSize/2)
           
           Mask2=np.zeros((mSize,mSize),np.float)
           polyVerticesTemp=np.array(np.round([[x[0],y[0]],[x[1],y[1]],[mSize/2,mSize/2]]),np.int32)
        #       polyVertices=polyVerticesTemp.reshape(2,3)
        #       polyVerticesNew=polyVertices.transpose()
           Mask2=cv.fillConvexPoly(Mask2, polyVerticesTemp, 1)
                  
           Mask=sc.logical_or(Mask1, Mask2)
           Mask=Mask.astype(float)
           plt.imshow(Mask)
           N=np.float(cv.countNonZero(Mask))
           plt.title(N)       
           plt.show()
       else:
           #rectangle generation
           rho = np.array([1,1,-1,-1,1],float)*(mSize/2)
           X,Y=cv.polarToCart(rho,theta)
           #X=np.cos(theta)*rho
           #Y=np.sin(theta)*rho
#           X=X+math.ceil(mSize/2)
#           Y=Y+math.ceil(mSize/2)
           X=np.round(X+mSize/2)
           Y=np.round(Y+mSize/2)
           Mask=np.zeros((mSize,mSize),np.float)
           polyVerticesTemp=np.array([X,Y],np.int32)
           polyVertices=polyVerticesTemp.reshape(2,5)
           polyVerticesNew=polyVertices.transpose()
           Mask=cv.fillConvexPoly(Mask, polyVerticesNew, 1)
           plt.imshow(Mask)
           N=np.float(cv.countNonZero(Mask))
           plt.title(N)
           plt.show()
           
           filts.append(Mask/N)
           filts.append(Mask)
           
           


       
    return filts, dirs

def GetAngleAssignment(nBands):
    deltaAngle=180.0/nBands
    angles=[]
    for i in range(nBands):
        angles.append((i*deltaAngle))
    return angles

flag=1    
filts, dirs=dirFilter2D(8,8)
total=0*filts[0]
#total[:]=0
for i in range(len(filts)):
    total=total+filts[i]
#    plt.imshow(total)
#    plt.colorbar()
##    plt.imsave(str(i)+' Mask.png', total)
#    plt.show()
    
plt.imshow(total)
plt.colorbar()
plt.show()



#import turtle 
#
#polygon = turtle.Turtle()
#
#num_sides = 6
#side_length = 70
#angle = 360.0 / num_sides 
#
#for i in range(num_sides):
#    polygon.forward(side_length)
#    polygon.right(angle)
#    
#turtle.done()    