# -*- coding: utf-8 -*-
"""
Created on Sun May 28 12:43:14 2023

@author: Reymond
"""

import cv2
import cv2.aruco as aruco
import numpy as np

# Define the dictionary and marker size
aruco_dict = aruco.getPredefinedDictionary(aruco.DICT_6X6_250)
marker_size = 200

# Generate the marker image
marker_id = 23
marker_image = np.zeros((marker_size, marker_size), dtype=np.uint8)
marker = aruco.drawMarker(aruco_dict, marker_id, marker_size, marker_image, 1)

# Save the marker image
cv2.imwrite('marker23.png', marker)