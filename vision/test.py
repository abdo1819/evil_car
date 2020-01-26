import numpy as np
import cv2
from find_lane import line_detector
import matplotlib.pyplot as plt

# use index of reqired camera
index = 0
cap = cv2.VideoCapture("data/vedio/out.mp4")
cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
cv2.namedWindow('canny_image',cv2.WINDOW_NORMAL)

fig = plt.figure()
fig.show()

while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()

    # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    detector = line_detector()
    # lines = detector.get_lines(frame)
    # img = detector.image_with_lines(frame,lines)
    
    img = detector.WarpPerspective(frame)
    canny_image = detector.canny(img)
    # detector.lines_histogram(fig, img)
    # cropped_image = self.region_of_interest(canny_image)


    # Display the resulting frame
    cv2.imshow('frame',img)
    cv2.imshow('canny_image',canny_image)
     
    cv2.resizeWindow('frame', 820,480)
    cv2.resizeWindow('canny_image', 820,480)


    if(cv2.waitKey(1) == 27):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()