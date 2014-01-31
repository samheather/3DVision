3DVision
===============

Important Note
==============
This project is superseeded by 3JVision - the version written in Java, since this version DOES NOT WORK.  Please see http://github.com/samheather/3JVision.

Original Note
=============

The goal of this project is to create a simple 3D cube that rotates as you move
your head as if you were literally moving your head to see it form a different
angle, using the simplest of Python code.

I will put both the face position detection and the cube rendering code in seperate
threads for perforance.

C++ Version uses GLEW for OpenGL.
On Ubuntu?  Glew is dependent, so install:
sudo apt-get install libxmu-dev
sudo apt-get install libxi-dev
