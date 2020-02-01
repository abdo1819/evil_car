import imagiz
import cv2

server=imagiz.Server()

import numpy as np
import cv2
from find_lane import line_detector , car_detector
import matplotlib.pyplot as plt
from vision_nn.car_detector import car_detector
from vision_nn.lane_detector import lane_detector_nn

detector_nn = lane_detector_nn(debug=True)
car_d = car_detector()


# debug = True
debug = False


# use index of reqired camera
index = 0
# cap = cv2.VideoCapture("data/gta/simple_two_lane.mp4")
# cap = cv2.VideoCapture("data/vedio/1.mp4")
# cap = cv2.VideoCapture(2)


cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
if debug ==True:
    cv2.namedWindow('lines',cv2.WINDOW_NORMAL)
    # cv2.namedWindow('mask',cv2.WINDOW_NORMAL)
    cv2.namedWindow('masked_img',cv2.WINDOW_NORMAL)
    cv2.namedWindow('canny',cv2.WINDOW_NORMAL)
    cv2.namedWindow('white',cv2.WINDOW_NORMAL)


detector = line_detector(debug=debug)
car_detector = car_detector()
while(True):
    # Capture frame-by-frame
    # ret, frame = cap.read()
    message=server.receive()
    frame=cv2.imdecode(message.image, 1)
    cv2.imshow("",frame)
    cv2.waitKey(1)

    # Our operations on the frame come here
    frame = cv2.resize(frame, (640, 360)) 
    img = detector_nn.img_received_callback(frame)

    # cars = car_detector.get_cars(frame)
    # car_detector.draw_cars(frame,cars)

    lines,lines_all = detector.get_lines(frame)

    img = detector.image_with_lines(img ,lines)
    
    cars = car_d.find_cars(frame)
    if cars is not None:
        img.reshape(frame.shape)
        img = car_d.draw(img, cars)



    # Display the resulting frame
    cv2.imshow('frame',img)
     
    cv2.resizeWindow('frame', 820,480)

    if debug ==True:
        detector.draw_ROI(img)
        img_lines = detector.image_with_lines(frame,lines_all)
        cv2.imshow('lines',img_lines)

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