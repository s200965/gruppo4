#from distutils.dir_util import copy_tree
import os
import shutil

def copy_rename(source, dest,newName,oldName):
    src_file = os.path.join(source, oldName)
    new_dst_file_name = os.path.join(dest,newName)
    shutil.move(src_file,new_dst_file_name)


def labelScratch(working_directory):
	
	newfilename=''
	imageCounterAC=0
	imageCounterAD=0
	imageCounterH=0

	outlierPath = working_directory+'/outlier'

	destDir=''
	magnificationDir=''
	for dirName,subdirList,fileList in os.walk(working_directory):
		if os.path.isdir(dirName):
			baseName=os.path.basename(dirName)
			if "_" in baseName:
				crop,pz,cl,roi=baseName.split('_')
				newfilename=cl+'_'
				destDir=dirName
		for file in fileList:
			if(file.endswith('jpeg') and dirName!=outlierPath):
				if os.path.isdir(file):
					print file,' is a directory'
				else:
					if (cl=='AC'):
						newfilename=cl+'_'+str(imageCounterAC)+'.jpeg'
						imageCounterAC+=1
					elif (cl=='AD'):
						newfilename=cl+'_'+str(imageCounterAD)+'.jpeg'
						imageCounterAD+=1
					elif (cl=='H'):
						newfilename=cl+'_'+str(imageCounterH)+'.jpeg'
						imageCounterH+=1
					magnificationDir=dirName
					copy_rename(dirName,destDir,newfilename,file)

		if os.path.exists(magnificationDir) and os.path.isdir(magnificationDir):
			if len(os.listdir(magnificationDir)) == 2:
				print 'magnificationDir',magnificationDir
				shutil.rmtree(magnificationDir)

def makemydir(whatever):
  try:
    os.makedirs(whatever)
  except OSError:
    pass
  # cd into the specified directory
  os.chdir(whatever)


def splitClasses(working_directory,classH,classAC,classAD):
	print '---- START SPLITTING PATCHES INTO CLASSES ----'
	for dirName,subdirList,fileList in os.walk(working_directory):

		os.chdir(dirName)
		outlierPath = working_directory+'/outlier'
	
		name = os.path.basename(dirName)
		if name.startswith('crop'):
			for file in fileList:
				if file.endswith('.jpeg'):
					print "file:", fileList
					filename=os.path.basename(file)

					if filename.startswith('H'):
						dst=classH
					elif filename.startswith('AC'):
						dst=classAC
					elif filename.startswith('AD'):
						dst=classAD

					print 'file', file
					src_file = os.path.join(dirName, file)
					new_dst_file_name = os.path.join(dst,file)
					print 'src',src_file
					print 'dst',new_dst_file_name

					shutil.move(src_file,new_dst_file_name)


# working_directory=os.getcwd() 
# name_toDirectory='/dataset'
# working_directory=working_directory+name_toDirectory
# #os.chdir(toDirectory)
# labelScratch(working_directory)


# splitClasses(working_directory)
