import cv2
import cv2.cv as cv
import numpy as  np
import threading

print "Press Escape to Quit"

lastPosition = [10,10,10]

class threadOne(threading.Thread):
    def run(self):
        self.setup()

    def setup(self):
        global lastPosition
        defaultCamera = cv2.VideoCapture(0) #set defaultCamera as a video stream from system camera 0
        s, img = defaultCamera.read()
        cascadeFile = cv2.CascadeClassifier('C:\opencv\data\haarcascades\haarcascade_frontalface_default.xml')
        lastFace = [200,40,240,240]
        
        streamWinName = "Camera Stream"
        cv2.namedWindow(streamWinName, cv2.CV_WINDOW_AUTOSIZE)
        videoWidth = defaultCamera.get(cv.CV_CAP_PROP_FRAME_WIDTH)
        videoHeight = defaultCamera.get(cv.CV_CAP_PROP_FRAME_HEIGHT)

        while s:
##          Put img's into windows and update img
            cv2.imshow(streamWinName,img)
            s, img = defaultCamera.read()
##           Call facedetect and draw 
            lastFace = self.facedetect(img, lastFace, cascadeFile)
##            viewerPosition = self.estimateViewerPosition(lastFace, videoHeight, videoWidth)
##            with lock:
##                lastPosition = viewerPosition
##          Exit method
            escapeKey = cv2.waitKey(10)
            if escapeKey == 27:
                print 'Goodbye 1'
                cv2.destroyWindow('Camera Stream')
                break

    def facedetect(self, img, lastFaceFound, faceCascade):
        gray = self.convertToGray(img)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2, minSize=(100, 100), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        if len(faces) > 0:
            lastFaceFound = faces[0]
        print lastFaceFound
        return lastFaceFound

    def convertToGray(self, inputImg):
        converted = cv2.cvtColor(inputImg, cv2.COLOR_RGB2GRAY)
        converted = cv2.equalizeHist(converted)
        return converted

    def estimateViewerPosition(self, face, videoWidth, videoHeight):
        frameFromSide = face[0]
        frameFromTop = face[1]
        frameSize = face[2]
##        Z is distance from camera, Y is elevation and X is X position.
        C = 0.1
        Z = int(30/(frameSize*C))
        X = int(frameFromSide + frameSize/2)
##        frameCenterYFromTop = frameFromTop + frameSize/2
##        Y = int(-(frameCenterYFromTop - videoHeight/2))
        Y = frameFromTop + (frameSize/2) - (videoHeight/2)
        print Y
        return [X,Y,Z]


class threadTwo(threading.Thread):
    def run(self):
        global lastPosition
        
        threeDWinName = "3D View"
        cv2.namedWindow(threeDWinName, cv2.CV_WINDOW_AUTOSIZE)
        img2 = cv2.imread('white.png', 0)
        cv2.imshow(threeDWinName,img2)
        cv2.circle(img2, (100,100),100,255,1)
        cv2.imshow(threeDWinName,img2)
        
        while True:
            with lock:
                viewerPosition = lastPosition
##            img2 = self.render(viewerPosition, img2)

    def render(self, positionToRenderFor, targetImg):
        print positionToRenderFor
##      Exit method
        escapeKey = cv2.waitKey(10)
        if escapeKey == 27:
            print 'Goodbye 2'
            cv2.destroyWindow('3D View')
##        cv2.circle(targetImg, (positionToRenderFor[0], positionToRenderFor[1]), positionToRenderFor[2]/2, 255, -1)
        cv2.circle(targetImg, (100,100),100,255,-1)
        return targetImg
        
        
lock = threading.Lock()

##threadOne().start()
threadTwo().start()
