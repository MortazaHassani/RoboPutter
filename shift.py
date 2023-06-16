import cv2
import numpy as np
import cv2.aruco as aruco #For RaspberryPi
from MQTTClientFYP import MQTTClientFYP
import json
import platform
import multiprocessing as mp
import sys
import random
import socket
import netifaces
import math

json_location = 'setting.json'
with open(json_location) as jfile:
    setting = json.load(jfile)


def update_setting(settingf = setting):
    with open(json_location, 'w') as ujfile:
        json.dump(settingf, ujfile)


def get_ip(setting):
    try:
        interfaces = netifaces.interfaces()
        wireless_interface = None
        for iface in interfaces:
            addrs = netifaces.ifaddresses(iface)
            if netifaces.AF_INET in addrs and netifaces.AF_LINK in addrs:
                if addrs[netifaces.AF_LINK][0]['addr'].startswith('b8:27:eb'):
                    if addrs[netifaces.AF_INET][0]['addr'].startswith('192.168.'):
                        wireless_interface = iface
                        break

        # Get the IP address of the wireless interface

        if wireless_interface is not None:
            ip_address = netifaces.ifaddresses(wireless_interface)[netifaces.AF_INET][0]['addr']
            print("IP address:", ip_address)
            setting['MQTT']['pi_ip'] = ip_address
            update_setting(setting)
        else:
            print("Wireless interface not found")
    except:
        pass


def command_car(flag, setting, command_d):
    client = MQTTClientFYP(
    broker_address=setting['broker']['broker_address'],
    broker_port=setting['broker']['broker_port'],
    topic=setting['broker']['topic'],
    username=setting['broker']['username'],
    password=setting['broker']['password']
    )
    client.start()
    print('MQTT initialized', flush=True)
    while flag.value == 1: # 1 means active
        if len(command_d) != 0:
            cmd_dict = dict(command_d)
            message = json.dumps(cmd_dict)
            client.publish_message(message)
    client.stop()


def random_generate():
    x = random.randint(11,17)
    y = random.randint(11,17)
    if (x % 2 ==0):
        x += 1
    if (y % 2 == 0):
        y += 1
    return (x,y)


def detect_circle(gray,img):
    blurframe = cv2.GaussianBlur(gray, random_generate(), 0)
    # Create a list to store the circles
    circle_list = []
    circles = cv2.HoughCircles(blurframe, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=40, param2=40, minRadius=10, maxRadius=50)
    # Draw circles on the original image and add to the list
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(img, (x, y), r, (0, 255, 0), 2)
            circle_list.append((x, y, r))
        # Sort the circles by their size (radius)
        circle_list = sorted(circle_list, key=lambda x: x[2])
    return circle_list

def aruco_detection(gray, setting):
    try:     
        ### For V 4.7.0 | PC
        if (cv2.__version__=='4.7.0'):
            aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
            parameters =  cv2.aruco.DetectorParameters()
            detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
            corners, markerIds, rejectedCandidates = detector.detectMarkers(gray)
        else:
            ### For v4.5.5 | Raspberry Pi
            
            aruco_dict = aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
            parameters = aruco.DetectorParameters_create()
            corners, markerIds, rejectedCandidates = aruco.detectMarkers(gray, aruco_dict, parameters=parameters)
        int_corners = np.int0(corners)
        # cv2.polylines(img, int_corners, True, (0, 255, 0), 5)

        aruco_perimeter = cv2.arcLength(corners[0], True)
        pixel_cm_ratio = aruco_perimeter / setting['Aruco']['marker_size']
        # print ("pixel_cm_ratio {}".format(pixel_cm_ratio))
        setting['Aruco']['pixel_cm_ratio'] = pixel_cm_ratio
    except:
        pixel_cm_ratio = setting['Aruco']['pixel_cm_ratio']
    
    return pixel_cm_ratio, int_corners


def draw_circle(frame, circle_locations,setting):
    for circle in circle_locations:
        x, y, r = circle
        cv2.circle(frame, (x, y), r, (255, 10, 25), 2)
        cv2.circle(frame, (x, y), 2, (0, 10, 255), 2)
        cv2.putText(frame, " {} cm".format(round((r/setting['Aruco']['pixel_cm_ratio'])*2, 1)), (int(x - 50), int(y - 5)), cv2.FONT_HERSHEY_PLAIN, 1, (100, 200, 0), 1)

def draw_direction(frame, circle_locations, setting):
    # Calculate the distance between the circles in centimeters
    dx, dy = circle_locations[1][0] - circle_locations[0][0], circle_locations[1][1] - circle_locations[0][1]
    length = np.sqrt(dx**2 + dy**2)
    distance = round(length / setting['Aruco']['pixel_cm_ratio'], 1) # delta
    unit_dx, unit_dy = dx / length, dy / length
    offset = (setting['Aruco']['pixel_cm_ratio'] * setting['car']['offset_distance']) + circle_locations[0][2]
    extended_point = (int(circle_locations[0][0] - offset * unit_dx), int(circle_locations[0][1] - offset * unit_dy))
    # Draw a line from the smaller circle to the larger circle
    cv2.arrowedLine(frame, (circle_locations[0][0], circle_locations[0][1]), (circle_locations[1][0], circle_locations[1][1]), (0, 255, 0), thickness=2)
  
    # Calculate the angle between the two circles in radians
    angle = np.arctan2(circle_locations[0][1] - circle_locations[1][1], circle_locations[0][0] - circle_locations[1][0])


    # Draw a line behind the smaller circle perpendicular to the line from smaller to larger circle
    line_length = circle_locations[0][2] * 2
    
    delta_x = (line_length ) * np.sin(angle)
    delta_y = -(line_length ) * np.cos(angle)

    p1_ = (int(extended_point[0] - delta_x ), int(extended_point[1] - delta_y ))
    p2_ = (int(extended_point[0] + delta_x ), int(extended_point[1] + delta_y ))

    
    cv2.arrowedLine(frame, p1_, p2_, (120, 0, 100), thickness=2)
    
    # Add the distance text to the frame
    text_pos = ((circle_locations[1][0] + circle_locations[0][0])//2, (circle_locations[1][1] + circle_locations[0][1])//2)
    cv2.putText(frame, f"{distance} cm {angle * (180 / math.pi)}\' ", text_pos, cv2.FONT_HERSHEY_SIMPLEX, 1, (100, 10, 0), 2)
    return p1_, p2_

def read_frames(output, flag):
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
    while True:
        ret, frame = cap.read()
        if not ret:
            flag.value = 0
            break
        output.put(frame)
        if flag.value == 0:
            while not output.empty():
                _ = output.get()
            print('End read: Camera Stop', flush=True)
            break
    cap.release()


def algo(input, flag, setting, command_d):
    cv2.namedWindow("MainAlgo", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("MainAlgo", 640, 480)
    circle_locations = []
    while True:
        frame = input.get()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        if (len(circle_locations)!=2):
            circle_locations = detect_circle(gray,frame)
        else:
            draw_circle(frame,circle_locations,setting)
            draw_direction(frame,circle_locations,setting)

            pixel_cm_ratio , corners = aruco_detection(gray, setting)
            command_d['forward']= 10
            cv2.polylines(frame, corners, True, (0, 255, 0), 2)

        cv2.imshow("MainAlgo", frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or flag.value == 0:
            flag.value = 0
            break
    while not input.empty():
        _ = input.get()
    cv2.destroyAllWindows()

    update_setting(setting)

if __name__ == '__main__':
    # Create a multiprocessing Queue to share frames between processes
    frame_queue = mp.Queue(maxsize=10)
    # Create a multiprocessing Value to share the flag variable
    flag = mp.Value('i', 1)
    # Shared dictionary 
    manager = mp.Manager()
    command_dict = manager.dict()

    # initialize processes
    prepare_process = mp.Process(target=get_ip, args=(setting, ))
    prepare_process.start()
    prepare_process.join()

    frame_process = mp.Process(target=read_frames, args=(frame_queue, flag))
    frame_process.daemon = True
    frame_process.start()

    algo_process = mp.Process(target=algo, args=(frame_queue, flag, setting, command_dict))
    algo_process.start()

    mqtt_process = mp.Process(target=command_car, args=(flag, setting, command_dict))
    mqtt_process.start()

    algo_process.join()
    

    flag.value = 0
