import numpy as np
import sys
from pyemd import emd   # for details look at https://github.com/wmayner/pyemd
def klDiv(p, q, **kwargs):
  """Kullback-Leibler divergence D(P || Q) for discrete distributions

  Parameters
  ----------
  p, q : array-like, dtype=float, shape=n
  Discrete probability distributions.
  """
  p = np.asarray(p, dtype=np.float)
  q = np.asarray(q, dtype=np.float)

  return np.sum(np.where(p != 0, p * np.log(p / q), 0))

def shift(l, n):
    return l[n:] + l[:n]

def emdDist(pdf1, pdf2, **kwargs):
  distMat = kwargs['distanceMatrix']
  return emd(pdf1, pdf2, distMat)
  
def rotationInvariantMinMeasure(pdf1, pdf2, measureFn, **kwargs):
  minVal = sys.float_info.max 
  for n in xrange(len(pdf1)):
    measureVal = measureFn(np.roll(pdf1, n), pdf2, **kwargs)
    minVal = measureVal if measureVal < minVal else minVal

  return minVal  
    
def L2Dist(p, q, **kwargs):
  p = np.asarray(p, dtype=np.float)
  q = np.asarray(q, dtype=np.float)
  a = p-q
  return np.sqrt(np.sum(a**2))

