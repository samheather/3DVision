import cv2
import cv2.cv as cv

print "Press Escape to Quit"

defaultCamera = cv2.VideoCapture(0) #set defaultCamera as a video stream from system camera 0
s, img = defaultCamera.read()
lastFace = [0,0,0,0]

def facedetect(img, lastFaceFound):
    faceCascade = cv2.CascadeClassifier('C:\opencv\data\haarcascades\haarcascade_frontalface_default.xml')
    gray = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
    gray = cv2.equalizeHist(gray)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=2, minSize=(50, 50), flags = cv2.cv.CV_HAAR_SCALE_IMAGE)
    if len(faces) > 0:
        lastFaceFound = faces[0]
    draw_3d(lastFaceFound)
    return lastFaceFound

def draw_3d(point):
    print point
    cv2.circle(img, (point[0]+point[2]/2,point[1]+point[2]/2), point[2]/2, 255, -1)

streamWinName = "Camera Stream"
threeDWinName = "3D View"
cv2.namedWindow(streamWinName, cv2.CV_WINDOW_AUTOSIZE)
cv2.namedWindow(threeDWinName, cv2.CV_WINDOW_AUTOSIZE)
##cv2.resizeWindow(threeDWinName, 600, 600)
img2 = cv.CreateImage((400,400), 8, 3)

while s:
##    Put img's into windows and update img
    cv2.imshow(streamWinName,img)
    cv2.imshow(threeDWinName,img)
    s, img = defaultCamera.read()
##    Call facedetect and draw 
    lastFace = facedetect(img, lastFace)
##    Exit method
    escapeKey = cv2.waitKey(10)
    if escapeKey == 27:
        cv2.destroyAllWindows()
        break
