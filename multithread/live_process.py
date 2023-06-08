import cv2
import numpy as np
import cv2.aruco as aruco #For RaspberryPi
import json
import platform
import multiprocessing as mp
import sys

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
        pixel_cm_ratio = setting['Aruco']['pixel_cm_ratio']
    
    return pixel_cm_ratio, int_corners

def detect_circle(gray,img):
    # Create a list to store the circles
    circle_list = []
    circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, dp=1, minDist=20, param1=40, param2=40, minRadius=10, maxRadius=50)
    # Draw circles on the original image and add to the list
    if circles is not None:
        circles = np.round(circles[0, :]).astype("int")
        for (x, y, r) in circles:
            cv2.circle(img, (x, y), r, (0, 255, 0), 2)
            circle_list.append((x, y, r))
        # Sort the circles by their size (radius)
        circle_list = sorted(circle_list, key=lambda x: x[2])
    return circle_list

def gaussian_filter(gray):
        # Apply Gaussian blur filter with kernel size 5x5 and sigma value of 0
        gray_blur = cv2.GaussianBlur(gray, (5, 5), 0)

        # Apply non-local means denoising with h=10 and search window size=21x21
        gray_denoised = cv2.fastNlMeansDenoising(gray_blur, None, h=10, searchWindowSize=21)

        return gray_denoised

# Function to read frames from the camera
def read_frames(output, image_queue, flag, initial_frames):
    if (platform.system()=='Windows'):
        cap = cv2.VideoCapture(0)
    else:
        cap = cv2.VideoCapture(0, cv2.CAP_V4L2)  # Use 0 for the default camera

        # Set the desired resolution
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
        if initial_frames.value < 11:
            image_queue.put(frame)
            initial_frames.value += 1
        if flag.value == 0:
            while not output.empty():
                _ = output.get()
            print('End read: Camera Stop', flush=True)
            break
    cap.release()

# Function to convert frames to grayscale and display them
def convert_to_grayscale(input, flag):
    cv2.namedWindow("Grayscale", cv2.WINDOW_NORMAL)
    cv2.resizeWindow("Grayscale", 640, 480)
    while True:
        frame = input.get()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        if aruco_mode:
            pixel_cm_ratio, maker_corner = aruco_detection(gray)
        else:
            pixel_cm_ratio = setting['Aruco']['pixel_cm_ratio']
        cv2.polylines(frame, maker_corner, True, (0, 255, 0), 5)
        circle_list = detect_circle(gray, frame) 

        cv2.imshow("Grayscale", frame)
        if cv2.waitKey(1) & 0xFF == ord('q') or flag.value == 0:
            flag.value = 0
            break
    while not input.empty():
        _ = input.get()
    cv2.destroyAllWindows()

if __name__ == '__main__':
    # Create a multiprocessing Queue to share frames between processes
    frame_queue = mp.Queue()

    # img queue
    image_queue = mp.Queue(maxsize=10)
    initial_frames = mp.Value('i', 1)
    # Create a multiprocessing Value to share the flag variable
    flag = mp.Value('i', 1)  # 1 means the program should continue running

    # Create the processes
    frame_process = mp.Process(target=read_frames, args=(frame_queue, image_queue, flag, initial_frames))
    frame_process.daemon = True
    frame_process.start()

    grayscale_process = mp.Process(target=convert_to_grayscale, args=(frame_queue, flag))
    grayscale_process.start()

    # Wait for the user to terminate the program
    grayscale_process.join()
    flag.value = 0
    # frame_process.join()

    while not image_queue.empty():
        frame = image_queue.get()
        cv2.imshow("Frame", frame)
        cv2.waitKey(1000)  # Wait for 2 seconds
    cv2.destroyAllWindows()

    sys.exit()  # Terminate the program