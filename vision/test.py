import numpy as np
import cv2
from find_lane import line_detector
import matplotlib.pyplot as plt

debug = False


# use index of reqired camera
index = 0
cap = cv2.VideoCapture("data/gta/simple_two_lane.mp4")
cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
if debug ==True:
    cv2.namedWindow('lines',cv2.WINDOW_NORMAL)
    # cv2.namedWindow('mask',cv2.WINDOW_NORMAL)
    cv2.namedWindow('masked_img',cv2.WINDOW_NORMAL)
    cv2.namedWindow('canny',cv2.WINDOW_NORMAL)
    cv2.namedWindow('white',cv2.WINDOW_NORMAL)


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    detector = line_detector(debug=debug)

    lines,lines_all = detector.get_lines(frame)

    img = detector.image_with_lines(frame,lines)
    img_lines = detector.image_with_lines(frame,lines_all)
    


    # Display the resulting frame
    cv2.imshow('frame',img)
     
    cv2.resizeWindow('frame', 820,480)
    if debug ==True:
        cv2.resizeWindow('lines', 820,480)
        # cv2.resizeWindow('mask', 820,480)
        cv2.resizeWindow('masked_img', 820,480)
        cv2.resizeWindow('canny', 820,480)
        cv2.resizeWindow('white', 820,480)


    if(cv2.waitKey(1) == 27):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()