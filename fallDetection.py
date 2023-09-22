import cv2, numpy as np, time
import angleMonitor, fallAction

class backgroundSub:
    
    history = 200
    varThresh = 64
    detectShadows = True
    kernel = np.ones((3,3),np.uint8)
    curFrame = 0

    def MOG(self):

        cap = cv2.VideoCapture("pick.mp4")
        fgbg = cv2.createBackgroundSubtractorMOG2(self.history, self.varThresh, self.detectShadows)

        while True:
            ret, frame = cap.read()
            if not ret:
                break

            if (self.curFrame % 1 == 0):
                fgmask = fgbg.apply(frame, 0)
                bgrThresh = fgmask

                if bgrThresh is not None:
                    _, bgrThresh = cv2.threshold(fgmask, 254, 255, cv2.THRESH_BINARY)
                    bgrThresh = cv2.morphologyEx(bgrThresh, cv2.MORPH_OPEN, self.kernel)
                    bgrThresh = cv2.morphologyEx(bgrThresh, cv2.MORPH_CLOSE, self.kernel)
                    bgrThresh = cv2.dilate(bgrThresh, self.kernel, iterations=2)
                    bgrThresh = cv2.morphologyEx(bgrThresh, cv2.MORPH_OPEN, self.kernel)

                    if cv2.countNonZero(bgrThresh) > 0:
                        fall.check(det.Detect(bgrThresh, self.curFrame, frame))

                self.curFrame += 1

                k = cv2.waitKey(30) & 0xff
                if k == 27:
                    break

        cap.release()
        cv2.destroyAllWindows()
        return 0

bgRemove = backgroundSub()

fall = fallAction.fallAction()

det = angleMonitor.angleMonitor()

bgRemove.MOG()