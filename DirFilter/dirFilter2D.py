import numpy as np
import math
import cv2 as cv
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
       rho = np.array([1,1,-1,-1,1],float)*(mSize/2)
       X,Y=cv.polarToCart(rho,theta)
       #X=np.cos(theta)*rho
       #Y=np.sin(theta)*rho
       X=np.round(X+mSize/2)
       Y=np.round(Y+mSize/2)
       Mask=np.zeros((mSize,mSize),np.float)
       polyVerticesTemp=np.array([X,Y],np.int32)
       polyVertices=polyVerticesTemp.reshape(2,5)
       polyVerticesNew=polyVertices.transpose()
       Mask=cv.fillConvexPoly(Mask, polyVerticesNew, 1)
       N=np.float(cv.countNonZero(Mask))
       filts.append(Mask/N)

    # correcting the orientation counter clockwise   
    temp = filts[1:]
    temp.reverse()
    filt0 = filts[0]
    filts = [filt0] + temp
    return filts, dirs

def GetAngleAssignment(nBands):
    deltaAngle=180.0/nBands
    angles=[]
    for i in range(nBands):
        angles.append((i*deltaAngle))
    return angles
    
