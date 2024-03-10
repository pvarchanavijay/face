import cv2
from math import ceil
import sys
import os
import numpy as np

cascPath = 'haarcascade_frontalface_default.xml'
faceCascade = cv2.CascadeClassifier(cascPath)
video_capture = cv2.VideoCapture(0)
recognizer = cv2.face.LBPHFaceRecognizer_create()

#Minimum Confidence required to label a face
min_confidence = 70
#Flag Variable to identify if dataset is trained or not
trained = 0
#To get/create a label directory in 'datasets'


def getNewLabel(name):
	current_directory = os.getcwd()
	final_directory = os.path.join(current_directory, 'photos', name)
	if not os.path.exists(final_directory):
		os.makedirs(final_directory)    	
	return final_directory


def readData():
	images = []
	image_label = []
	names = []
	cd = os.getcwd()
	dataset_dir = os.path.join(cd, 'photos')
	folders = os.listdir(dataset_dir)
	for i in range(len(folders)):
		names.append(folders[i]) 
		wd = os.path.join(dataset_dir,folders[i])
		folder_imgs = os.listdir(wd)
		for j in folder_imgs:
			im = cv2.imread(os.path.join(wd,j),0)
			faces = faceCascade.detectMultiScale(im, 1.1, 5, minSize = (50,50))
			for (x,y,w,h) in faces:
				im_arr = np.array(im[x:x+w,y:y+h],'uint8')
				images.append(im_arr)
				image_label.append(i)
				#cv2.imshow("Adding", im_arr)
				#cv2.waitKey(100)
	cv2.destroyAllWindows()
	return images, image_label, names






#Training on dataset
image_data, labels, names = readData()
if(image_data!=[]):
	recognizer.train(image_data, np.array(labels))
	trained = 1;
#Font for adding text on live web cam
font = cv2.FONT_HERSHEY_DUPLEX

c = 0
res=[]
while True:
	ret,frame = video_capture.read()

	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	faces = faceCascade.detectMultiScale(gray, 1.1, 5, minSize = (50,50))
	for (x,y,w,h) in faces:
		cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,255),2)
		test = gray[x:x+w,y:y+h]
		test_img = np.array(test,'uint8')
		if(trained==1):
			
			if(test_img.any()):
				index, confidence = recognizer.predict(test_img)
			if(confidence>=min_confidence):
				res.append(names[index])
				cv2.putText(frame,names[index],(x,y+h+20),font,.5,(0,255,255))
				cv2.putText(frame,str(ceil(confidence))+"%",(x,y-20),font,.5,(0,255,255))
	cv2.imshow('Video', frame)
	k = cv2.waitKey(1) & 0xFF
	#Press 'Escape' to exit web cam 
	if k == 27:
		print(set(res))
		break
	

video_capture.release()
cv2.destroyAllWindows()
