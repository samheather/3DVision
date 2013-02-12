import cv2
import cv2.cv as cv
import numpy as  np
import pyglet
import threading
from Queue import Queue

print "Press Escape to Quit"

my_queue = Queue()
my_queue.put([10,10,10])

class threadOne(threading.Thread):
    def run(self):
        self.setup()

    def setup(self):
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
            viewerPosition = self.estimateViewerPosition(lastFace, videoHeight, videoWidth)
            my_queue.put(viewerPosition)
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
        C = 0.01
        Z = int(30/(frameSize*C))
        X = int(frameFromSide + frameSize/2)
##        frameCenterYFromTop = frameFromTop + frameSize/2
##        Y = int(-(frameCenterYFromTop - videoHeight/2))
        Y = int(frameFromTop + (frameSize/2) - (videoHeight/2))
        return [X,Y,Z]


class threadTwo(threading.Thread):
    def run(self):

        cubeWindow = pyglet.window.Window(width = 400, height = 400)

        @cubeWindow.event
        def on_draw():

            print 'ran on_draw'

            # Move the camera back a little.
            # TODO(sam): When you want to start rotating the camera, this should move into on_draw,
            # and there should be a call to gRotatef.
            pyglet.gl.glMatrixMode(pyglet.gl.GL_MODELVIEW)
            pyglet.gl.glLoadIdentity()
            pyglet.gl.glTranslatef(0, 0, -6)
            pyglet.gl.glRotatef(0, 0, 0, 0) #seems to rotate c degrees around a point x,y,z???
            
            cubeWindow.clear()
            
            pyglet.gl.glColor4f(1.0,0,0,1.0)

            pyglet.graphics.draw_indexed(8, pyglet.gl.GL_LINES, [0, 1, 1, 2, 2, 3, 3, 0,# front square
                                                                 4, 5, 5, 6, 6, 7, 7, 4,# back square
                                                                 0, 4, 1, 5, 2, 6, 3, 7],# connectors
                                   ('v3f', (-1, -1, 0,
                                            1, -1, 0,
                                            1, 1, 0,
                                            -1, 1, 0,
                                            -1, -1, -1,
                                            1, -1, -1,
                                            1, 1, -1,
                                            -1, 1, -1)))
        
        @cubeWindow.event
        def on_show():
            pyglet.gl.glClear(pyglet.gl.GL_COLOR_BUFFER_BIT | pyglet.gl.GL_DEPTH_BUFFER_BIT)
            # Set up projection matrix.
            pyglet.gl.glMatrixMode(pyglet.gl.GL_PROJECTION)
            pyglet.gl.glLoadIdentity()
            pyglet.gl.gluPerspective(45.0, float(cubeWindow.width)/cubeWindow.height, 0.1, 360)
            print 'ran on_show'
        pyglet.app.run()
        
        while True:
            queueToSkip = int(my_queue.qsize()) - 1## this is approximate size - cause problem?
            for queueIndex in range(0, queueToSkip):
                my_queue.get()
            viewerPosition = my_queue.get()

            on_draw()

        
        

        
        
lock = threading.Lock()

threadOne().start()
threadTwo().start()
