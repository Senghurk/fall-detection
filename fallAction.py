import cv2
import numpy as np
import collections

class fallAction:

    def __init__(self):
        self.init = False
        self.detectedAngles = collections.deque([0]*5, 5)

    def check(self, angle):

        if angle is not None:

            if not self.init:
                
                self.detectedAngles.appendleft(angle)
                if all(i >= 70 for i in self.detectedAngles) and all(i <= 100 for i in self.detectedAngles):
                    print("Fall Detected!!!")

