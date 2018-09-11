import openslide
import os
import PIL
import matplotlib.image as img
import cv2
import numpy as np
import shutil
import glob
from matplotlib import pyplot as plt
from PIL import Image
from openslide.deepzoom import DeepZoomGenerator
from os import listdir
from os.path import isfile, join
from featureSelection import calculateFeaturesForStromaSelection
from k_means import scan_dir

from cropPreparation import initialCropping,cropFilter,delete_dir
from classSplit import labelScratch,splitClasses

#start MAIN
working_directory=os.getcwd()
#os.makedirs(working_directory+'/crop')
#initialCropping(working_directory)

crop_directory=working_directory+'/crop'
#delete_dir(crop_directory)
#print os.getcwd()
#cropFilter(crop_directory)
#print 'cartella corrente:',working_directory
#labelScratch(crop_directory)

classAC=crop_directory+'/AC'
classAD=crop_directory+'/AD'
classH=crop_directory+'/H'

#os.makedirs(classH)
#os.makedirs(classAC)
#os.makedirs(classAD)

TrainingAC=working_directory+'/TrainingAC'
TrainingH=working_directory+'/TrainingH'

#os.makedirs(TrainingAC)
#os.makedirs(TrainingH)

#splitClasses(crop_directory,classH,classAC,classAD)

# caluclate features for AC training set
calculateFeaturesForStromaSelection(TrainingAC,'ACTrainingFeatures.csv')

# caluclate features for AC test set
calculateFeaturesForStromaSelection(classAC,'ACTestFeatures.csv')

# caluclate features for H training set
#calculateFeaturesForStromaSelection(TrainingH,'HTrainingFfeatures.csv')

# caluclate features for H test set
#calculateFeaturesForStromaSelection(classH,'HTestFeatures.csv')

#calculateFeaturesForStromaSelection(classAD,'ADTestFeatures.csv')


#end MAIN