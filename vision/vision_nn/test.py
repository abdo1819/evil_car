import numpy as np
import cv2
from lane_detector import lane_detector_nn 
from car_detector import car_detector
import matplotlib.pyplot as plt

debug = True


# use index of reqired camera
index = 0
cap = cv2.VideoCapture("../data/gta/simple_two_lane.mp4")
cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
detector = lane_detector_nn(debug=debug)
car_d = car_detector()


while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
    frame = cv2.resize(frame, (640, 360)) 

    # Our operations on the frame come here

    img = detector.img_received_callback(frame)
    
    cars = car_d.find_cars(frame)
    if cars is not None:
        img.reshape(frame.shape)
        img = car_d.draw(img, cars)

    # Display the resulting frame
    cv2.imshow('frame',img)
     
    cv2.resizeWindow('frame', 640,360)

    if(cv2.waitKey(1) == 27):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()