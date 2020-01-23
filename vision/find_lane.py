import cv2
import numpy as np

        


class line_detector():
    def __init__(self, debug = False):
        self.debug = debug 

    def get_lines(self, img):
        canny_image = self.canny(img)
        cropped_image = self.region_of_interest(canny_image)
        lines = cv2.HoughLinesP(cropped_image,2,np.pi/180,100,np.array([]),minLineLength=10,maxLineGap=5)
        
        if self.debug:
            self.diplay_lines(img, lines)
        
        return lines

    def region_of_interest(self, image):
        height,width = image.shape
        polygons = np.array([
            [(0,height),(width,height),(width,int(height/2)),(0,int(height/2))]
        ])          # Triangle polygon because cv2.fillPoly expects an array of polygons.
        
        mask = np.zeros_like(image)   # Create a black mask to apply the above cube.
        cv2.fillPoly(mask,polygons,255)     # A complete white triangle polygon on a black mask.
        masked_image = cv2.bitwise_and(image,mask)

        if self.debug:
            cv2.imshow("mask",mask)
            cv2.imshow("masked_img",masked_image)

        return masked_image


    def canny(self, image):
        gray = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)
        blur = cv2.GaussianBlur(gray,(5,5),0)   # Kernel size is 5x5
        canny = cv2.Canny(blur,50,150)

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
        
        
        return
        
