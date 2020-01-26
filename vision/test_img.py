from find_lane import line_detector
import cv2



#load image 
img = cv2.imread('data/imgs/2_lane_curvey.jpg')

detector = line_detector(debug=True)

# find lines 
lines = detector.get_lines(img)
# detector.lines_histogram(img)
# averaged_lines = average_slope_intercept(frame,lines)

while True:
    if(cv2.waitKey(0) == 27):
        cv2.destroyAllWindows()
        break

# # load vedio file