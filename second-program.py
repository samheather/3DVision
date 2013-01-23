import cv2
import cv2.cv as cv
import threading

print "Press Escape to Quit"

class threadOne(threading.Thread):#I don't understand this or the next line
    def run(self):
        setup()

    def setup():
        defaultCamera = cv2.VideoCapture(0) #set defaultCamera as a video stream from system camera 0
        s, img = defaultCamera.read()
        cascadeFile = cv2.CascadeClassifier('C:\opencv\data\haarcascades\haarcascade_frontalface_default.xml')
        lastFace = [0,0,0,0]
        
        streamWinName = "Camera Stream"
        threeDWinName = "3D View"
        cv2.namedWindow(streamWinName, cv2.CV_WINDOW_AUTOSIZE)
        cv2.namedWindow(threeDWinName, cv2.CV_WINDOW_AUTOSIZE)
        ##cv2.resizeWindow(threeDWinName, 600, 600)
        img2 = cv.CreateImage((400,400), 8, 3)

        while s:
##          Put img's into windows and update img
            cv2.imshow(streamWinName,img)
            cv2.imshow(threeDWinName,img)
            s, img = defaultCamera.read()
##           Call facedetect and draw 
            lastFace = facedetect(img, lastFace, cascadeFile)
##          Exit method
            escapeKey = cv2.waitKey(10)
            if escapeKey == 27:
                cv2.destroyAllWindows()
                break

    def facedetect(img, lastFaceFound, faceCascade):
        gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
        gray = cv2.equalizeHist(gray)
        faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2, minSize=(50, 50), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
        if len(faces) > 0:
            lastFaceFound = faces[0]
        draw_3d(lastFaceFound)
        return lastFaceFound


class threadTwo(threading.Thread):
    def run(self):
        print 'ran'

threadOne().start()
threadTwo().start()
