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
#from k_means import scan_dir, k_means

def makemydir(whatever):
    try:
        os.makedirs(whatever)
    except OSError:
        pass
    # cd into the specified directory
    os.chdir(whatever)

def initialCropping(working_directory):
    """ This function crops the initial svs images:
        - it scans the dataset directory 
        - use the Python Wrapper of the OpenSlide library to perform an image cropping on different magnification levels
        - the dimension of the crops are 510 and the overlap value is 1
        - the output of this function is a directory called as the image itself that contain a variable number of directory."""
    print '---- START CROPPING PROCEDURE ----'
    print 'current directory:',working_directory
    try:
        images_folder='/dataset'
        path=working_directory+images_folder
        onlyfiles = [f for f in listdir(path) if isfile(join(path, f))]
        somma = len(onlyfiles)
        for i in range(somma):
            if onlyfiles[i].endswith('.svs'):
                osr=openslide.OpenSlide('dataset/'+onlyfiles[i])
                namefolder,formato=onlyfiles[i].split(".")
                pz,label,ROIid=namefolder.split("_")
                dz=DeepZoomGenerator(osr,510,1,True)
                for level in range(dz.level_count):
                    tiledir = os.path.join(working_directory+"/crop/"+"crop_"+namefolder, str(level))
                    if not os.path.exists(tiledir):
                        os.makedirs(tiledir)
                    cols, rows = dz.level_tiles[level]
                    for row in range(rows):
                        for col in range(cols):
                            tilename = os.path.join(tiledir, '%s_%d_%d.jpeg' % (label,col,row))
                            tile=dz.get_tile(level,(col,row))
                            tile.save(tilename, quality=90)
                print "crop",namefolder,"created"

	print '---- END CROPPING PROCEDURE ----'
    except OSError:
        print 'Error Cropping image' 


def cropFilter(working_directory):
    """ This function filter our crops:
        - it scans the directory of the choosen magnification level
        - cut out all the elements in it that have dimension different from the one whe choose 
          and also all the crops that have a grey-level value grater than 80%
    """
    print '---- START CROPPING FILTER ----'
    print 'current directory:',working_directory
    count = 0 
    percent = 0.8
    outlier_counter=0
    try:
        outlierPath = working_directory+'/outlier'
        os.makedirs(outlierPath)
        for dirName, subdirList, fileList in os.walk(working_directory):
          os.chdir(dirName)
          for fname in fileList:
            if(fname.endswith('.jpeg') and dirName!=outlierPath):
                im_grayscale = cv2.imread(fname,0)
                blur = cv2.GaussianBlur(im_grayscale,(5,5),0)
                ret,th = cv2.threshold(blur,180,255,cv2.THRESH_BINARY)
                dimension = im_grayscale.shape
                height = dimension[0]
                width = dimension[1]
                count = 0
                name,formato=fname.split('.')
                cl,pz,roi=name.split('_')

                for i in range(height):
                    for j in range(width):
                        if(th[i][j])==255:
                            count = count +1
                if(count>=percent*width*height):
                    outlier_counter+=1
                    new_dst_file_name = os.path.join(outlierPath,str(cl)+'_'+str(pz)+'_'+str(roi)+'_outlier'+str(outlier_counter)+'.jpeg')
                    shutil.move(fname,new_dst_file_name)
                elif (width<500 or height<500):
                    print 'delete '+fname
                    outlier_counter+=1
                    new_dst_file_name = os.path.join(outlierPath,str(cl)+'_'+str(pz)+'_'+str(roi)+'_outlier'+str(outlier_counter)+'.jpeg')
                    shutil.move(fname,new_dst_file_name)

	print '---- END CROPPING FILTER ----'
    except OSError:
        print 'Error Filtering Crops'  




def delete_dir(path_stroma):
    """ This function select only magnification 20 directory:
        - it scan the starting dir and deletes all the non intresting directories
    """

    print '---- SELECTING MAGNIFICATION 20 DIRECTORY ----' 
    print 'current directory:',path_stroma

    try:
        for f in listdir(path_stroma):
            crop_dir=path_stroma+'/'+f
            a=listdir(crop_dir)
            b=[]

            for i in range(len(a)):
                t = int(a[i])
                b.append(t)
            b.sort()
            magnification20=b[-2]

            for f2 in a:
                if int(f2) != magnification20:
                    dir_to_delete=crop_dir+'/'+f2
                    shutil.rmtree(dir_to_delete)

    	print '---- SELECTION ENDS ----'
    except OSError:
        print 'Error in selecting magnification 20 directory'