# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 21:08:16 2023

@author: Reymond
"""

import cv2
import numpy as np
from MQTTClientFYP import MQTTClientFYP
import cv2.aruco as aruco #For RaspberryPi
import json
import platform
with open('setting.json') as jfile:
    setting =json.load(jfile)
    

aruco_mode = setting['Aruco']['aruco_mode']
arucoerror = False
command = ''

def aruco_detection(gray):
    global arucoerror    
    try:     
        ### For V 4.7.0 | PC
        if (cv2.__version__=='4.7.0'):
            aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
            parameters =  cv2.aruco.DetectorParameters()
            detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
            corners, markerIds, rejectedCandidates = detector.detectMarkers(gray)
            #print("markerIds {} - corners: {}".format(markerIds, corners))
        else:
            ### For v4.5.5 | Raspberry Pi
            
            aruco_dict = aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
            parameters = aruco.DetectorParameters_create()
            corners, markerIds, rejectedCandidates = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        # Draw polygon around the marker
        int_corners = np.int0(corners)
        #cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
        
        # Aruco Perimeter
        aruco_perimeter = cv2.arcLength(corners[0], True)
        
        # Pixel to cm ratio
        pixel_cm_ratio = aruco_perimeter / 20
        if (arucoerror):
            arucoerror = False
            print ("pixel_cm_ratio {}".format(pixel_cm_ratio))
    except:
        if (arucoerror != True):
            arucoerror = True
            print('unable to detect Aruco! set to default')
        pixel_cm_ratio = 29.52
    
    return pixel_cm_ratio, int_corners
def gaussian_filter(gray):
        # Apply Gaussian blur filter with kernel size 5x5 and sigma value of 0
        gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply non-local means denoising with h=10 and search window size=21x21
        gray_denoised = cv2.fastNlMeansDenoising(gray_blur, None, h=10, searchWindowSize=21)

        return gray_blur
def detect_circle(gray,img):
    # Create a list to store the circles
    circle_list = []
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=40, param2=40, minRadius=10, maxRadius=50)
    # Draw circles on the original image and add to the list
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            #cv2.circle(img, (x, y), r, (0, 255, 0), 2)
            circle_list.append((x, y, r))
        # Sort the circles by their size (radius)
        circle_list = sorted(circle_list, key=lambda x: x[2])
    return circle_list

def draw_objects(img,circles):
    for i, (x, y, r) in enumerate(circles):
        cv2.circle(img, (x, y), r, (0, 255, 0), 2)
def pro_camera():
    # Load Camera 
    if (platform.system()=='Windows'):
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)
        width = setting['camera']['width']
        height = setting['camera']['height']
        cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)
        cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter_fourcc('M', 'J', 'P', 'G'))
        cap.set(cv2.CAP_PROP_FPS, setting['camera']['FPS'])
    if not cap.isOpened():
        print("Failed to open the camera")
        exit()
    while True:
        # Read a frame from the camera
        ret, img = cap.read()

        if not ret:
            print("Failed to capture frame from camera")
            break
        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        gfi = gaussian_filter(gray)
        circle_list = detect_circle(gfi, img)    

        draw_objects(img,circle_list)
        cv2.imshow("Image", img)
        # Exit code
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q') or key == 27:  # Exit on "q" or "Esc" key press
            break

    cap.release()
    cv2.destroyAllWindows()

def pro_image():
    # Load image
    img = cv2.imread('Field/top3.jpg')
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    if aruco_mode:
        pixel_cm_ratio, maker_corner = aruco_detection(img)
    else:
        pixel_cm_ratio = 29.526773834228514
    circle_list = detect_circle(gray,img)    
    print(maker_corner)
    # Display the result
    cv2.imshow("Result", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

if __name__ == "__main__":
    #pro_image()
    pro_camera()

# # Load object detection model for car robot
# car_cascade = cv2.CascadeClassifier('car.xml')

# # Detect car robots using Haar cascades
# cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# # Draw rectangles around the detected cars
# for (x, y, w, h) in cars:
#     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)