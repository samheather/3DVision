import cv2
import cv2.cv as cv
from random import randrange

count = 0

def simple():
	global count
	defaultCamera = cv2.VideoCapture(0)
	s, img = defaultCamera.read()
	cascadeFile = cv2.CascadeClassifier('OpenCV/opencv-2.4.8/data/haarcascades/haarcascade_frontalface_default.xml')
	
	streamWinName = "Camera Stream"
	cv2.namedWindow(streamWinName, cv.CV_WINDOW_NORMAL)

	while s:
		cv2.imshow(streamWinName,img)
		s, img = defaultCamera.read()
		gray = convertToGray(img)
		faces = cascadeFile.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        	if len(faces) > 0:
			# [top left x, top left y, width, height]
			centreX = faces[0][0]+faces[0][2]/2
			centreY = faces[0][1]+faces[0][3]/2			
			diameter = (faces[0][2]+faces[0][3])/3.5
	 		count += 1
			if (count%70 == 15):			
				print faces[0]
			cv2.circle(img, (centreX, centreY), diameter, (100,100,255))

            	#Exit method
            	escapeKey = cv2.waitKey(10)
            	if escapeKey == 27:
                	print 'Goodbye'
                	cv2.destroyWindow(streamWinName)
                	break

def convertToGray(inputImg):
        converted = cv2.cvtColor(inputImg, cv2.COLOR_RGB2GRAY)
        return cv2.equalizeHist(converted)
        

simple()
