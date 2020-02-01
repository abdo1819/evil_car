from find_lane import line_detector
import cv2
import matplotlib.pyplot as plt
from vision_nn.car_detector import car_detector
from vision_nn.lane_detector import lane_detector_nn

detector_nn = lane_detector_nn(debug=True)
car_d = car_detector()



cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
cv2.namedWindow('lines',cv2.WINDOW_NORMAL)
# cv2.namedWindow('mask',cv2.WINDOW_NORMAL)
cv2.namedWindow('masked_img',cv2.WINDOW_NORMAL)
cv2.namedWindow('canny',cv2.WINDOW_NORMAL)
cv2.namedWindow('white',cv2.WINDOW_NORMAL)


# cv2.namedWindow('img',cv2.WINDOW_NORMAL)
#load image 

frame = cv2.imread('data/gta/SharedScreenshot.jpg')
frame = cv2.resize(frame, (640, 360)) 

detector = line_detector(debug=True)

img = detector_nn.img_received_callback(frame)
# find lines 
lines,lines_all = detector.get_lines(img)

img = detector.image_with_lines(img,lines)
detector.draw_ROI(frame)
img_lines = detector.image_with_lines(frame,lines_all)




cars = car_d.find_cars(frame)
if cars is not None:
    img.reshape(frame.shape)
    img = car_d.draw(img, cars)





cv2.imshow('frame',img)
cv2.imshow('lines',img_lines)

cv2.resizeWindow('frame', 820,480)
cv2.resizeWindow('lines', 820,480)
# cv2.resizeWindow('mask', 820,480)
cv2.resizeWindow('masked_img', 820,480)
cv2.resizeWindow('canny', 820,480)
cv2.resizeWindow('white', 820,480)


while True:
    if(cv2.waitKey(0) == 27):
        cv2.destroyAllWindows()
        break

# # load vedio file