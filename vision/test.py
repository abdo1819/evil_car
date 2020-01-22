import numpy as np
import cv2
from find_lane import line_detector

# use index of reqired camera
index = 0
cap = cv2.VideoCapture(index)

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    detector = line_detector()
    lines = detector.get_lines(frame)
    detector.diplay_lines(frame,lines)

    if(cv2.waitKey(1) == 27):
        break

cap.release()
cv2.destroyAllWindows()