import cv2

def setup():
	defaultCamera = cv2.VideoCapture(0)
	s, img = defaultCamera.read()
	cascadeFile = cv2.CascadeClassifier('OpenCV/opencv-2.4.8/data/haarcascades/haarcascade_frontalface_default.xml')
	
	streamWinName = "Camera Stream"
	cv2.namedWindow(streamWinName, cv2.CV_WINDOW_AUTOSIZE)

	while s:
		cv2.imshow(streamWinName,img)
		s, img = defaultCamera.read()
		gray = convertToGray(img)
		faces = cascadeFile.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2, minSize=(10, 10), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        	if len(faces) > 0:
	 		print "Face Found"

            	#Exit method
            	escapeKey = cv2.waitKey(10)
            	if escapeKey == 27:
                	print 'Goodbye'
                	cv2.destroyWindow(streamWinName)
                	break

def convertToGray(inputImg):
        converted = cv2.cvtColor(inputImg, cv2.COLOR_RGB2GRAY)
        return cv2.equalizeHist(converted)
        

setup()
