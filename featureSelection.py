import openslide
import os
import PIL
import matplotlib.image as img
import cv2
import scipy
import numpy as np
import shutil
import glob
from matplotlib import pyplot as plt
from PIL import Image
from openslide.deepzoom import DeepZoomGenerator
from os import listdir
from os.path import isfile, join
import skimage
from skimage.io import imread
from skimage.feature import greycomatrix
from skimage.feature import greycoprops
from skimage import exposure
import pandas as pd
from matplotlib import pyplot as plt
from skimage import feature
from sklearn.cluster import KMeans
import csv

   
def calculateFeaturesForStromaSelection(path,fileFeatures):
#    fileFeatures=os.path.join(path,'features.csv')
    feature_csv = open(fileFeatures, "w") 
    print feature_csv
    for fileName in glob.glob(os.path.join(path,'*.jpeg')):
        retrieve_features(fileName,feature_csv)
    feature_csv.close()

def retrieve_features(filename,fileToWrite):
    im = imread(filename, as_gray=True)
    im = skimage.img_as_ubyte(im)

    g = skimage.feature.greycomatrix(im, [1], [0], levels=256, symmetric=False, normed=True)
    #contrast= skimage.feature.greycoprops(g, 'contrast')[0][0]
    energy= skimage.feature.greycoprops(g, 'energy')[0][0]
    homogeneity= skimage.feature.greycoprops(g, 'homogeneity')[0][0]
    correlation=skimage.feature.greycoprops(g, 'correlation')[0][0]
    #dissimilarity=skimage.feature.greycoprops(g, 'dissimilarity')[0][0]
    ASM=skimage.feature.greycoprops(g, 'ASM')[0][0]

    #add contrast
    # min=im.min()
    # max=im.max()
    # out_range=(min+50,max-50)
    # im = exposure.rescale_intensity(im,out_range)

    hist=retrieveLBPHisyogram(24,8,im)
 
    stringa='%s'%(filename)
    #stringa=stringa+',%s,%s,%s,%s,%s,%s'%(contrast,energy,homogeneity,correlation,dissimilarity,ASM)

    stringa=stringa+',%s,%s,%s,%s'%(energy,homogeneity,correlation,ASM)
    
    counter=0
    for f in hist:
        counter+=1
        if(counter==2 or counter==11 or counter==12 or counter==13 or counter==14 or counter==15 or counter==16 or counter==23 or counter==25):
            stringa=stringa+',%s'%f

    fileWithoutPAth=os.path.basename(filename)

    imageClass=-1
    if(fileWithoutPAth.startswith('gland')):
        imageClass=0
    elif(fileWithoutPAth.startswith('stroma')):
        imageClass=1


    stringa1=stringa+','+str(imageClass)
    stringaF=stringa1+'\n'
    
    fileToWrite.write(stringaF)

def assign_labels(labels,data):
    print data
    countElement=0
    for element in data.iloc[:,0]:
        fileName=str(element)
        name,formato=fileName.split('.')
        newFileName=name+'_'+str(labels[countElement])+'.'+formato
        shutil.move(fileName, newFileName)
        countElement=countElement+1


def retrieveLBPHisyogram(numPoints,radius,image):
	# compute the Local Binary Pattern representation
	# of the image, and then use the LBP representation
	# to build the histogram of patterns
    
    eps=1e-7
    lbp = feature.local_binary_pattern(image,numPoints,radius,method="uniform")
    (hist, _) = np.histogram(lbp.ravel(),bins=np.arange(0, numPoints + 3),range=(0, numPoints + 2))

    # normalize the histogram
    hist = hist.astype("float")
    hist /= (hist.sum() + eps)

    # return the histogram of Local Binary Patterns
    return hist

