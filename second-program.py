import cv2
import cv2.cv as cv
import numpy as  np
import threading

print "Press Escape to Quit"

lastPosition = None

class threadOne(threading.Thread):
    def run(self):
        self.setup()

    def setup(self):
        global lastPosition
        defaultCamera = cv2.VideoCapture(0) #set defaultCamera as a video stream from system camera 0
        s, img = defaultCamera.read()
        cascadeFile = cv2.CascadeClassifier('C:\opencv\data\haarcascades\haarcascade_frontalface_default.xml')
        lastFace = [0,0,0,0]
        
        streamWinName = "Camera Stream"
        cv2.namedWindow(streamWinName, cv2.CV_WINDOW_AUTOSIZE)

        while s:
##          Put img's into windows and update img
            cv2.imshow(streamWinName,img)
            s, img = defaultCamera.read()
##           Call facedetect and draw 
            lastFace = self.facedetect(img, lastFace, cascadeFile)
            viewerPosition = self.estimateViewerPosition(lastFace)
            with lock:
                lastPosition = viewerPosition
##          Exit method
            escapeKey = cv2.waitKey(10)
            if escapeKey == 27:
                print 'Goodbye'
                cv2.destroyAllWindows()
                break

    def facedetect(self, img, lastFaceFound, faceCascade):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2, minSize=(50, 50), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        if len(faces) > 0:
            lastFaceFound = faces[0]
        return lastFaceFound

    def estimateViewerPosition(self, face):
        windowWidth = 640
        windowHeight = 480
        frameFromSide = face[0]
        frameFromTop = face[1]
        frameSize = face[2]
##        Z is distance from camera, Y is elevation and X is X position.
        Z = 10*frameSize
        X = frameFromSide
        frameCenterYFromTop = frameFromTop + frameSize/2
        Y = 0
        return [X,Y,Z]


class threadTwo(threading.Thread):
    def run(self):
        global lastPosition
        
        threeDWinName = "3D View"
        cv2.namedWindow(threeDWinName, cv2.CV_WINDOW_AUTOSIZE)
        img2 = np.zeros((600,600),np.float32)
        cv2.imshow(threeDWinName,img2)
        
        while True:
            with lock:
                viewerPosition = lastPosition
            img2 = self.render(viewerPosition, img2)

    def render(self, positionToRenderFor, targetImg):
        cv2.circle(targetImg, (positionToRenderFor[0], positionToRenderFor[1]), positionToRenderFor[2]/2, 255, -1)
        return targetImg
        
        
lock = threading.Lock()

threadOne().start()
threadTwo().start()
