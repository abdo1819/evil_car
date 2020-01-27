import cv2
import numpy as np
import matplotlib.pyplot as plt
from logging import Logger




class line_detector():
    def __init__(self, debug = False):
        self.debug = debug 

    def get_lines(self, img):
        canny_image = self.canny(img)
        cropped_image = self.region_of_interest(canny_image)
        lines = cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=10,maxLineGap=5)
        # l = line()
        # for line in  lines:
            # if = l.slope(line) 

        # if self.debug:
            # self.diplay_lines(img, lines)
        
        return lines

    def lines_histogram(self, img):
        
        y = np.sum(img,axis=0)
        x = np.arange(0,img.shape[1])
        
        plt.plot(x, y)

        plt.show()

    def WarpPerspective(self, image):
        
        height,width = image.shape[0:2]
        
        y = height
        x = width
        
        src,dst = self.ROI(image)
        # transformation matrix to make lines parallel
        M = cv2.getPerspectiveTransform(src, dst)
        
        return cv2.warpPerspective(image, M, (x,y), flags=cv2.INTER_LINEAR)


    def ROI(self, image):
        height,width = image.shape[0:2]

        

    def ROI(self, image):
        height,width = image.shape[0:2]

        # bottom_left=[0,670] 
        # bottom_right=[1325,670] 
        # top_left=[725,525] 
        # top_right=[1005,525] 

        bottom_left=(0,height) 
        bottom_right= (0,int(height/2))
        top_left=(width,height) 
        top_right=(width,int(height/2)) 

        src = np.array([
            [bottom_left,top_left,top_right,bottom_right]
        ])          # Triangle polygon because cv2.fillPoly expects an array of polygons.
        

        # dst_width = bottom_right - bottom_left
        # dst_hight = height * .6
        # dst = np.array([
            # [bottom_left-50,]
        # ])
        dst= np.float32([[0 ,height], [0  ,0], [width ,0], [width ,height]]) # Destination Points for Image Warp

        return src,dst


    def region_of_interest(self, image):
        src,dst = self.ROI(image)
        mask = np.zeros_like(image)   # Create a black mask to apply the above cube.
        cv2.fillPoly(mask,src,255)     # A complete white triangle polygon on a black mask.
        masked_image = cv2.bitwise_and(image,mask)

        if self.debug:
            cv2.imshow("mask",mask)
            cv2.imshow("masked_img",masked_image)

        return masked_image


    def canny(self, image):
        gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)   # Kernel size is 5x5
        canny = cv2.Canny(blur,100,200)

        if self.debug:
            cv2.imshow('canny', canny)

        return canny
    

    def image_with_lines(self, img, lines):
        line_image = np.zeros_like(img)
        if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line.reshape(4)  # Reshaping all the lines to a 1D array.
                cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10) # Draw a Blue Line(BGR in OpenCV)

        combo_image = cv2.addWeighted(img,0.8,line_image,1,1)    # Imposing the line_image on the original image
         
        return combo_image
        
class line():

    def __init__(self, lines=[]):
        self.lines = lines

    def slope(self, line):
        x1 = line[0,0]
        y1 = line[0,1]
        
        x2 = line[1,0]
        y2 = line[1,1]
        
        return (y2-y1)/(x2-x1)