import cv2
import cv2.cv as cv
import threading

print "Press Escape to Quit"

class MyThread(threading.thread):
    def threadOne(self):
        print 'running first'

class threadTwo(threading.thread):
    def run(self):
        print 'running second'
