# -*- coding: utf-8 -*-
"""
Created on Sat Jun  3 21:08:16 2023

@author: Reymond
"""

import cv2
import numpy as np

# Load image
img = cv2.imread('Field/top2.jpg')

# Convert to grayscale
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

# Detect circles using HoughCircles
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=40, param2=50, minRadius=10, maxRadius=50)

# Draw circles on the original image
if circles is not None:
    circles = np.round(circles[0, :]).astype("int")
    for (x, y, r) in circles:
        cv2.circle(img, (x, y), r, (0, 255, 0), 2)

# # Load object detection model for car robot
# car_cascade = cv2.CascadeClassifier('car.xml')

# # Detect car robots using Haar cascades
# cars = car_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

# # Draw rectangles around the detected cars
# for (x, y, w, h) in cars:
#     cv2.rectangle(img, (x, y), (x+w, y+h), (0, 0, 255), 2)

# Display the result
cv2.imshow("Result", img)
cv2.waitKey(0)
cv2.destroyAllWindows()