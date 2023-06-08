from threading import Thread
# from multiprocessing import Process
import cv2
import numpy as np

class ArucoProc:
    """
    Class that continuously perform Aruco detection on frame using a dedicated thread.
    """

    def __init__(self, frame=None):
        self.frame = frame
        self.gray = None
        self.stopped = False
        self.aruco_dict = None
        self.parameters = None
        if (cv2.__version__)=='4.7.0':
            self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
            self.parameters =  cv2.aruco.DetectorParameters()
            self.detector = cv2.aruco.ArucoDetector(self.aruco_dict, self.parameters)
        else:
            self.aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
            self.parameters = cv2.aruco.DetectorParameters_create()
            
        self.int_corners = None

    def start(self):
        Thread(target=self.detect, args=()).start()
        # Process(target=self.detect, args=()).start()
        return self

    def detect(self):
        while not self.stopped:
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            if (cv2.__version__)=='4.7.0':
                corners, markerIds, rejectedCandidates = self.detector.detectMarkers(gray)
            else:
                corners, markerIds, rejectedCandidates = cv2.aruco.detectMarkers(gray, self.aruco_dict, parameters=self.parameters)
            self.int_corners = np.int0(corners)
            #cv2.polylines(self.frame, self.int_corners, True, (0, 255, 0), 5)
            print("marker ID {}".format(markerIds))
            self.gray = gray
            # if self.gray is not None:
            #     cv2.imshow("Gray", self.gray)
            # if cv2.waitKey(1) == ord("q"):
            #     self.stopped = True
            

    def stop(self):
        self.stopped = True
