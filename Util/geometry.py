#http://stackoverflow.com/questions/13635528/fit-a-ellipse-in-python-given-a-set-of-points-xi-xi-yi
#from skimage.measure import moments

#http://stackoverflow.com/questions/31163133/counting-pixels-within-an-ellipse-from-a-numpy-array

from skimage.measure import moments
import sys
import ThirdParty.boundingBoxTool as bbTool
from biMorpAnalysis import connectedComponents
def estimateScaleRange(dataFactory, thr = 0, **kwargs):
  ''' This function estimates minimum and maximum pixel length and width
  for connected componentsin the data
  '''
  minWidth,  minLength = 2*[sys.maxint]
  maxWidth, maxLength = 2*[0]  
  for xSeg, name in dataFactory:
    conCmpsIdx = connectedComponents(xSeg, numPixels = thr)
    for i, cmpIdx in enumerate(conCmpsIdx):
      (rot_angle, area, width, length, center_point, corner_points) = \
        bbTool.findMinBoundRect(np.array( zip(*cmpIdx) ))
      if width > length:
        width, length = length , width
      if minWidth > width: minWidth = width
      if maxWidth < width: maxWidth = width
      if minLength > length: minLength = length
      if maxLength < length: maxLength = length

  return minWidth, maxWidth, minLength, maxLength              


def fitOnImageEllipse(data):
    '''
    Returns the length of the long and short axis and the angle measure
    of the long axis to the horizontal of the best fit ellipsebased on
    image moments.

    usage: longAxis, shortAxis, angle = fitEllipse(N_by_M_image_as_array)
    '''
    # source:
    #     Kieran F. Mulchrone, Kingshuk Roy Choudhury,
    # Fitting an ellipse to an arbitrary shape:
    # implications for strain analysis, Journal of
    # Structural Geology, Volume 26, Issue 1,
    # January 2004, Pages 143-153, ISSN 0191-8141,
    # <http://dx.doi.org/10.1016/S0191-8141(03)00093-2.>
    #     Lourena Rocha, Luiz Velho, Paulo Cezar P. Carvalho
    # Image Moments-Based Structuring and Tracking of
    # Objects, IMPA-Instituto Nacional de Matematica Pura
    # e Aplicada. Estrada Dona Castorina, 110, 22460
    # Rio de Janeiro, RJ, Brasil,
    # <http://ieeexplore.ieee.org/stamp/stamp.jsp?tp=&arnumber=1167130>

    m = moments(data, 2) # super fast compated to anything in pure python
    xc = m[1,0] / m[0,0]
    yc = m[0,1] / m[0,0]
    a = (m[2,0] / m[0,0]) - (xc**2)
    b = 2 * ((m[1,1] / m[0,0]) - (xc * yc))
    c = (m[0,2] / m[0,0]) - (yc**2)
    theta = .5 * (np.arctan2(b, (a - c)))
    w = np.sqrt(6 * (a + c - np.sqrt(b**2 + (a-c)**2)))
    l = np.sqrt(6 * (a + c + np.sqrt(b**2 + (a-c)**2)))
    return l, w, theta
  
import numpy as np
import numpy.linalg as linalg
import matplotlib.pyplot as plt

def fitEllipse(x,y):
    x = x[:,np.newaxis]
    y = y[:,np.newaxis]
    D =  np.hstack((x*x, x*y, y*y, x, y, np.ones_like(x)))
    S = np.dot(D.T,D)
    C = np.zeros([6,6])
    C[0,2] = C[2,0] = 2; C[1,1] = -1
    E, V =  linalg.eig(np.dot(linalg.inv(S), C))
    n = np.argmax(np.abs(E))
    a = V[:,n]
    return a

def ellipse_center(a):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    num = b*b-a*c
    x0=(c*d-b*f)/num
    y0=(a*f-b*d)/num
    return np.array([x0,y0])

def ellipse_angle_of_rotation( a ):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    return 0.5*np.arctan(2*b/(a-c))

def ellipse_axis_length( a ):
    b,c,d,f,g,a = a[1]/2, a[2], a[3]/2, a[4]/2, a[5], a[0]
    up = 2*(a*f*f+c*d*d+g*b*b-2*b*d*f-a*c*g)
    down1=(b*b-a*c)*( (c-a)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    down2=(b*b-a*c)*( (a-c)*np.sqrt(1+4*b*b/((a-c)*(a-c)))-(c+a))
    res1=np.sqrt(up/down1)
    res2=np.sqrt(up/down2)
    return np.array([res1, res2])

def find_ellipse(x, y):
    xmean = x.mean()
    ymean = y.mean()
    x -= xmean
    y -= ymean
    a = fitEllipse(x,y)
    center = ellipse_center(a)
    center[0] += xmean
    center[1] += ymean
    phi = ellipse_angle_of_rotation(a)
    axes = ellipse_axis_length(a)
    x += xmean
    y += ymean
    return center, phi, axes





  
def testEllpise():  
    points = [(560036.4495758876, 6362071.890493258),
     (560036.4495758876, 6362070.890493258),
     (560036.9495758876, 6362070.890493258),
     (560036.9495758876, 6362070.390493258),
     (560037.4495758876, 6362070.390493258),
     (560037.4495758876, 6362064.890493258),
     (560036.4495758876, 6362064.890493258),
     (560036.4495758876, 6362063.390493258),
     (560035.4495758876, 6362063.390493258),
     (560035.4495758876, 6362062.390493258),
     (560034.9495758876, 6362062.390493258),
     (560034.9495758876, 6362061.390493258),
     (560032.9495758876, 6362061.390493258),
     (560032.9495758876, 6362061.890493258),
     (560030.4495758876, 6362061.890493258),
     (560030.4495758876, 6362061.390493258),
     (560029.9495758876, 6362061.390493258),
     (560029.9495758876, 6362060.390493258),
     (560029.4495758876, 6362060.390493258),
     (560029.4495758876, 6362059.890493258),
     (560028.9495758876, 6362059.890493258),
     (560028.9495758876, 6362059.390493258),
     (560028.4495758876, 6362059.390493258),
     (560028.4495758876, 6362058.890493258),
     (560027.4495758876, 6362058.890493258),
     (560027.4495758876, 6362058.390493258),
     (560026.9495758876, 6362058.390493258),
     (560026.9495758876, 6362057.890493258),
     (560025.4495758876, 6362057.890493258),
     (560025.4495758876, 6362057.390493258),
     (560023.4495758876, 6362057.390493258),
     (560023.4495758876, 6362060.390493258),
     (560023.9495758876, 6362060.390493258),
     (560023.9495758876, 6362061.890493258),
     (560024.4495758876, 6362061.890493258),
     (560024.4495758876, 6362063.390493258),
     (560024.9495758876, 6362063.390493258),
     (560024.9495758876, 6362064.390493258),
     (560025.4495758876, 6362064.390493258),
     (560025.4495758876, 6362065.390493258),
     (560025.9495758876, 6362065.390493258),
     (560025.9495758876, 6362065.890493258),
     (560026.4495758876, 6362065.890493258),
     (560026.4495758876, 6362066.890493258),
     (560026.9495758876, 6362066.890493258),
     (560026.9495758876, 6362068.390493258),
     (560027.4495758876, 6362068.390493258),
     (560027.4495758876, 6362068.890493258),
     (560027.9495758876, 6362068.890493258),
     (560027.9495758876, 6362069.390493258),
     (560028.4495758876, 6362069.390493258),
     (560028.4495758876, 6362069.890493258),
     (560033.4495758876, 6362069.890493258),
     (560033.4495758876, 6362070.390493258),
     (560033.9495758876, 6362070.390493258),
     (560033.9495758876, 6362070.890493258),
     (560034.4495758876, 6362070.890493258),
     (560034.4495758876, 6362071.390493258),
     (560034.9495758876, 6362071.390493258),
     (560034.9495758876, 6362071.890493258),
     (560036.4495758876, 6362071.890493258)]

    import  skimage.measure as ms
    im = np.zeros((512, 512))

    #for x in xrange(25, 150):
    #    for i in xrange(1, 10):
    #        im[x , x + i ] = 1
    im[ 50:60, 50:150] = 1
    plt.imshow(im), plt.show()
    #l, w, theta = fitOnImageEllipse(im)
    #print('l= {} w = {} theta = {}'.format(l, w, theta))
    
    
    y, x = im.nonzero()
    points = zip(x, y)
    elModel = ms.EllipseModel()
    elModel.estimate(np.array(points))
    print elModel.params
    
    fig, axs = plt.subplots(2, 1, sharex = True, sharey = True)
    a_points = np.array(points)
    x = a_points[:, 0]
    y = a_points[:, 1]
    axs[0].plot(x,y)
    center, phi, axes = find_ellipse(x, y)
    print "center = ",  center
    print "angle of rotation = ",  phi
    print "axes = ", axes

    axs[1].plot(x, y)
    axs[1].scatter(center[0],center[1], color = 'red', s = 100)
    axs[1].set_xlim(x.min(), x.max())
    axs[1].set_ylim(y.min(), y.max())

    plt.show()

def testBoundingBox():
  # make couple of images
  im1 = np.zeros((100, 100));

  im1[40:50, 20:80] = 1
  im2 = np.zeros((100, 100))

  for x in xrange(1, 40):
    im2[x, x] = 1
    for y in xrange(1, 20):
      im2[x,x + y] = 1
  import matplotlib.pyplot as plt
  plt.imshow(im1), plt.show()
  plt.imshow(im2), plt.show()
  dataFactory = [(im1, 'im1'), (im2, 'im2')]
  minWidth, maxWidth , minLength, maxLength= estimateScaleRange(dataFactory, 10)
  print('minWidth= {}, maxWidth = {} , minLength = {}, maxLength = {}'.format(
                                    minWidth, maxWidth , minLength, maxLength))
  

    
if __name__ == '__main__':
  testBoundingBox()
