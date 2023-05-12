# -*- coding: utf-8 -*-
"""
Created on Fri May 12 18:07:07 2023

@author: Reymond
"""

import cv2
from object_detector import *
import numpy as np

detectorHomo = HomogeneousBgDetector()
aruco_mode = True


def aruco_detection(aruco_mode, img):
    if aruco_mode:
        try:
            # Load Aruco detector
            aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
            parameters =  cv2.aruco.DetectorParameters()
            detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
            
            #parameters = cv2.aruco.DetectorParameters()
            #aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)
            
            # Get Aruco marker
            corners, markerIds, rejectedCandidates = detector.detectMarkers(img)
            
            # Draw polygon around the marker
            int_corners = np.int0(corners)
            cv2.polylines(img, int_corners, True, (0, 255, 0), 5)
            
            # Aruco Perimeter
            aruco_perimeter = cv2.arcLength(corners[0], True)
            
            # Pixel to cm ratio
            pixel_cm_ratio = aruco_perimeter / 20
        except:
            print('unable to detect Aruco! set to default')
            pixel_cm_ratio = 29.52
    else:
        pixel_cm_ratio = 29.526773834228514
    return pixel_cm_ratio

def contours_detection(contours, img):
    objects_center = []
    # Draw objects boundaries
    for cnt in contours:
        # Get rect
        rect = cv2.minAreaRect(cnt)
        (x, y), (w, h), angle = rect

        # Get Width and Height of the Objects by applying the Ratio pixel to cm
        object_width = w / pixel_cm_ratio
        object_height = h / pixel_cm_ratio

        cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1) #dot inside the center

        #To draw circle around objects
        center = (int(x), int(y))
        radius = int((w+h)/4)
        cv2.circle(img, center, radius, (255, 0, 0), 2)
        # Store center and radius of detected circles
        objects_center.append((center, radius))
        
        cv2.putText(img, "diameter {} cm".format(round((object_width+object_height)/2, 1)), (int(x - 100), int(y - 5)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
        # cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
        # cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
        
    return objects_center


#-------------------------------------------------
# Create a VideoCapture object and open the camera
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Failed to open the camera")
    exit()

while True:
    # Read a frame from the camera
    ret, img = cap.read()

    if not ret:
        print("Failed to capture frame from camera")
        break
#-------------------------------------------------


    #---------------------------- Stream
    pixel_cm_ratio = aruco_detection(aruco_mode, img)
    #print("pixel_cm_ratio:",pixel_cm_ratio)
    contours = detectorHomo.detect_objects(img)
    objects_center = contours_detection(contours, img)
    
    
    cv2.imshow("Image", img)
    
    
    
    # Exit code
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:  # Exit on "q" or "Esc" key press
        break

# Release the VideoCapture and close the window
cap.release()
cv2.destroyAllWindows()
