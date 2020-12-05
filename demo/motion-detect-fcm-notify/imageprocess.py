import cv2
import numpy as np


class MotionDetect():
    def __init__(self, prevFrame, curFrame):
        self.dist_threshold = 5
        self.prevFrame = prevFrame
        self.curFrame = curFrame
    
    def distMap(self, curFrame):        
        diff = np.float32(self.prevFrame) - np.float32(curFrame)
        norm32 = np.sqrt(diff[:,:,0]**2 + diff[:,:,1]**2 + diff[:,:,2]**2)/np.sqrt(255**2 + 255**2 + 255**2)
        dist = np.uint8(norm32*255)

        mod = cv2.GaussianBlur(dist, (9, 9), 0)
        _, thresh = cv2.threshold(mod, 100, 255, 0)
        _, stDev = cv2.meanStdDev(mod)

        self.prevFrame = self.curFrame
        self.curFrame = curFrame

        if stDev > self.dist_threshold:
            return True
        else:
            return False