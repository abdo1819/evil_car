import cv2
from lane_detector import lane_detector_nn 

img= cv2.imread('../data/gta/img_staight _.png')
resized_image = cv2.resize(img, (640, 360)) 

detector = lane_detector_nn(debug=True)

detector.img_received_callback(img)

cv2.waitKey(0)