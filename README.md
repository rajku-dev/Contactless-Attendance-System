# Contactless-Attendance-System

Contactless Attendance System is a three-step process namely face detection, followed by face recognition and finally if a registered person is detected then marks the attendance. This proposed system detects and recognises faces using deep learning algorithms by using a camera to take pictures of an individual. When a match is made in the face database, then attendance is marked of the recognised person with name, date and time. 'face_recognition' Library is used to compute and compare features of different real-time input images to accurately recognize them. Once the recognition step is done, attendance of the respective recognized person will be marked in an excel sheet and firebase realtime database. 

## Environment Setup

The virtual environment used for the application contains the following version of dependencies:

1. Python : version  '3.11.5’
2. face_recognition : version '1.3.0'
3. CMake : version  '3.30.2'
4. dlib : version  '19.24.6' 
5. Pandas: version ‘2.2.2’
6. firebase_admin : version '6.5.0'
7. Tkinter : Tkinter is a Python package for the Tk graphical user interface toolkit. Version used '8.6' 
9. OpenCV : version '4.10.0'

## Application

To use the application clone the repository and run main_gui.py script after creating the virtual environment.
