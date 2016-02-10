Multiscale analysis of neurite orientation
==========================================
code in this repository is based on our paper
**Multiscale analysis of neurite orientation and spatial organization inneuronal images**

Installation for ubuntu 14.04 TLS
---------------------------------
Code depends on standard python based scientifc packages like scipy. numpy
matplotlib and scikit-image

some extra dependency are 
1) pycircstat <a href="https://github.com/circstat/pycircstat">https://github.com/circstat/pycircstat/</a>
 2) pyemd <a href="https://github.com/wmayner/pyemd">https://github.com/wmayner/pyemd</a>

3) opencv 

which can be installed using

pip install pycircstat

pip install pyemd


sudo apt-get install libopencv-dev python-opencv

Using code
---------
please check the demo file dirAnalyzerDemo.py for setting the parameter
There is a associated  jupyter notebook dirAnalyzerDemo.ipynb

As code depends on presegmentation of images there is an
another notebook localOstuBasedSegmentationUtility.ipynb 
for elementary segmentation based on OSTU


