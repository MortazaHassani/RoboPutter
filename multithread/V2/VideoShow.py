from threading import Thread
import cv2
import numpy as np

class VideoShow:
    """
    Class that continuously shows a frame using a dedicated thread.
    """

    def __init__(self, frame=None):
        self.frame = frame
        self.stopped = False

    def start(self):
        Thread(target=self.show, args=()).start()
        return self

    def show(self):
        while not self.stopped:
            
            if self.frame is not None:
                gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
            
                aruco_dict = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_4X4_50)
                parameters =  cv2.aruco.DetectorParameters()
                detector = cv2.aruco.ArucoDetector(aruco_dict, parameters)
                corners, markerIds, rejectedCandidates = detector.detectMarkers(gray)
                int_corners = np.int0(corners)
                cv2.polylines(self.frame, int_corners, True, (0, 255, 0), 5)
                
                cv2.imshow("Video", self.frame)
            if cv2.waitKey(1) == ord("q"):
                self.stopped = True

    def stop(self):
        self.stopped = True
