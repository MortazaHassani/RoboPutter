from threading import Thread
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

    def start(self):
        Thread(target=self.detect, args=()).start()
        return self

    def detect(self):
        while not self.stopped:
            gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            
            aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
            parameters =  cv2.aruco.DetectorParameters()
            detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
            corners, markerIds, rejectedCandidates = detector.detectMarkers(gray)
            int_corners = np.int0(corners)
            cv2.polylines(self.frame, int_corners, True, (0, 255, 0), 5)
            print("marker ID {}".format(markerIds))
            self.gray = gray
            if self.gray is not None:
                cv2.imshow("Gray", self.gray)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True
   

    def stop(self):
        self.stopped = True
