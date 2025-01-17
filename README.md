# Contactless-Attendance-System

The Contactless Attendance System is designed as a three-step process: face detection, face recognition, and attendance marking. The system utilizes deep learning techniques for detecting and recognizing faces using a camera that captures real-time images of individuals. Upon identifying a match from the stored face database, the system records the attendance of the recognized individual along with their name, date, and time. The 'face_recognition' library facilitates feature extraction and comparison to ensure accurate identification. Once a person is recognized, their attendance is updated both in an Excel sheet and in a Firebase Realtime Database for seamless record management.
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
