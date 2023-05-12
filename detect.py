# -*- coding: utf-8 -*-
"""
Created on Fri Mar 31 11:52:05 2023

@author: Reymond
"""

import cv2
from object_detector import *
import numpy as np

aruco_mode = False
# Load Image
img = cv2.imread("top-golf3.jpg")
# Get the image dimensions (height, width, channels)
img_height, img_width, img_channels = img.shape

 # Load Object Detector
detectorH = HomogeneousBgDetector()


if aruco_mode:
    
    # Load Aruco detector
    aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
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
else:
    pixel_cm_ratio = 29.526773834228514
print("pixel_cm_ratio:",pixel_cm_ratio)


contours = detectorH.detect_objects(img)

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
# Draw arrow from center of smaller circle to bigger circle and add distance text
if len(objects_center) == 2:
    # Find smaller and larger circle
    smaller_circle, larger_circle = sorted(objects_center, key=lambda x: x[1])

    # Calculate distance between centers of smaller and larger circles
    distance = round(np.sqrt((larger_circle[0][0] - smaller_circle[0][0])**2 + (larger_circle[0][1] - smaller_circle[0][1])**2) / pixel_cm_ratio, 1)

    # Draw arrow from center of smaller circle to center of larger circle
    cv2.arrowedLine(img, smaller_circle[0], larger_circle[0], (0, 255, 0), thickness=2)

    # Add distance text over the arrow
    text_pos = ((smaller_circle[0][0] + larger_circle[0][0])//2, (smaller_circle[0][1] + larger_circle[0][1])//2)
    cv2.putText(img, f"{distance} cm", text_pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 10, 99), 2)
    
    # Draw line behind smaller circle
    line_len = int(2 * pixel_cm_ratio)  # 2 cm
    angle_rad = np.deg2rad(rect[2])
    line_dir = (larger_circle[0][0] - smaller_circle[0][0], larger_circle[0][1] - smaller_circle[0][1])
    line_dir_len = np.sqrt(line_dir[0]**2 + line_dir[1]**2)
    line_dir = (line_dir[0] / line_dir_len, line_dir[1] / line_dir_len)
    line_start = (int(x - line_len/2 * np.cos(angle_rad)), int(y - line_len/2 * np.sin(angle_rad)))
    line_end = (int(x + line_len/2 * np.cos(angle_rad)), int(y + line_len/2 * np.sin(angle_rad)))
    line_dir_angle = np.arctan2(line_dir[1], line_dir[0])
    line_dir_angle = np.rad2deg(line_dir_angle) - 90
    line_dir_angle_rad = np.deg2rad(line_dir_angle)
    line_start = (int(smaller_circle[0][0] - line_len/2 * np.cos(line_dir_angle_rad)), int(smaller_circle[0][1] - line_len/2 * np.sin(line_dir_angle_rad)))
    line_end = (int(smaller_circle[0][0] + line_len/2 * np.cos(line_dir_angle_rad)), int(smaller_circle[0][1] + line_len/2 * np.sin(line_dir_angle_rad)))
    cv2.line(img, line_start, line_end, (0, 255, 255), thickness=2)
    
    # center of line draw behind the ball
    # line_center = ((line_start[0] + line_end[0])//2, (line_start[1] + line_end[1])//2)
    # print("center of line  {}".format(line_center))
    
    # Calculate the angle between the line and the horizontal axis
    dx = line_end[0] - line_start[0]
    dy = line_end[1] - line_start[1]
    angle_deg = np.rad2deg(np.arctan2(dy, dx))*-1
    
    angle_str = f"{angle_deg:.1f} degrees"
    
    # Print the angle on the image
    text_pos = (int((line_start[0] + line_end[0])/2), int((line_start[1] + line_end[1])/2) - 20)
    cv2.putText(img, angle_str, text_pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 10, 99), 2)
    
    center_ball = smaller_circle[0]
    print("center of ball  {}".format(center_ball))
    
    robot_distance_x = 2 * pixel_cm_ratio
    robot_distance_y = 2 * pixel_cm_ratio
    robot_distance = (robot_distance_x,robot_distance_y)
    if center_ball[1]>=img_height/2:
        robot_position = (int(center_ball[0]-robot_distance_x),int(center_ball[1]-robot_distance_y))
    else:
        robot_position = (int(center_ball[0]-robot_distance_x),int(center_ball[1]+robot_distance_y))

    print("Robot position {}".format(robot_position))
    cv2.circle(img, (robot_position[0], robot_position[1]), 5, (0, 100, 255), -1) #dot inside the center        
cv2.imshow("Image", img)
while True:
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:  # Exit on "q" or "Esc" key press
        break

# Close the window and cleanup
cv2.destroyAllWindows()