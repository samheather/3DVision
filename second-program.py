import cv2
import cv2.cv as cv
import threading

print "Press Escape to Quit"

lastPosition = None

class threadOne(threading.Thread):#I don't understand this or the next line
    def run(self):
        self.setup()

    def setup(self):
        global lastPosition
        defaultCamera = cv2.VideoCapture(0) #set defaultCamera as a video stream from system camera 0
        s, img = defaultCamera.read()
        cascadeFile = cv2.CascadeClassifier('C:\opencv\data\haarcascades\haarcascade_frontalface_default.xml')
        lastFace = [0,0,0,0]
        
        streamWinName = "Camera Stream"
        threeDWinName = "3D View"
        cv2.namedWindow(streamWinName, cv2.CV_WINDOW_AUTOSIZE)
        cv2.namedWindow(threeDWinName, cv2.CV_WINDOW_AUTOSIZE)
##        cv2.resizeWindow(threeDWinName, 640, 680)
        img2 = cv.CreateImage((320, 240), 32, 1)

        while s:
##          Put img's into windows and update img
            cv2.imshow(streamWinName,img)
            cv2.imshow(threeDWinName,img2)
            s, img = defaultCamera.read()
##           Call facedetect and draw 
            lastFace = self.facedetect(img, lastFace, cascadeFile)
            viewerPosition = self.estimateViewerPosition(lastFace)
            with lock:
                print viewerPosition
                lastPosition = viewerPosition
                print lastPosition
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
        frameFromX = face[0]
        frameFromTop = face[1]
        frameSize = face[2]
##        Z is distance from camera, Y is elevation and X is X position.
        Z = 10*frameSize
        X = frameFromX
        
        return face[0]


class threadTwo(threading.Thread):
    def run(self):
        global lastPosition
        while True:
            with lock:
                print 'hello', lastPosition
        
lock = threading.Lock()

threadOne().start()
##threadTwo().start()
