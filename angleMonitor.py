import cv2
class angleMonitor:
    count = 0
    font = cv2.FONT_HERSHEY_PLAIN

    def Detect(self, frame, curFrame, origFrame):
        returnAngle = None

        contours, hierarchy = cv2.findContours(frame, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        if contours:
            maxContour = max(contours, key = cv2.contourArea)

            rows, cols = frame.shape[:2]
            [vx, vy, x, y] = cv2.fitLine(maxContour, cv2.DIST_L2, 0, 0.01, 0.01)
            lefty = int((-x * vy / vx) + y)
            righty = int(((cols - x) * vy / vx) + y)

            frame = cv2.cvtColor(frame, cv2.COLOR_GRAY2RGB)
            screenText = ""

            if len(maxContour) > 4:
                (x, y), (MA, ma), angle = cv2.fitEllipse(maxContour)
                returnAngle = angle
                maxArea = cv2.contourArea(maxContour)

                if maxArea > 100:
                    try:
                        ellipse = cv2.fitEllipse(maxContour)
                        cv2.ellipse(origFrame, ellipse, (0, 255, 0), 2)
                        cv2.line(origFrame, (cols - 1, righty), (0, lefty), (0, 0, 255), 2)
                    except OverflowError as e:
                        print(f"OverflowError: {e}")
                    
                    screenText = 'Angle: ' + str(round(angle, 1))
                else:
                    screenText = "Area too small: " + str(maxArea)
            else:
                print("Less than 5 points in contour array")
                screenText = "Less than 5 points in contour array"
        else:
            print("No contours found")
            screenText = "No contours found"

        cv2.putText(origFrame, screenText, (3, 25), self.font, 2, (242, 238, 26), 2, cv2.LINE_AA)
        cv2.imshow("Fall Detection", origFrame)
        cv2.imshow("Background Removal", frame)

        return returnAngle
