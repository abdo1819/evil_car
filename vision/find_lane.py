import cv2
import numpy as np
import matplotlib.pyplot as plt
from logging import Logger

cascade_file = "cascade_dir/cascade.xml"
class car_detector():
    def __init__(self,cascade_file =cascade_file ,debug=False):
        self.cascade_file = cascade_file
        self.debug = debug

    def get_cars(self, image):
        car_cascade = cv2.CascadeClassifier(self.cascade_file)
        gray_image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)   
        cars = car_cascade.detectMultiScale(gray_image,1.2,5)

        return cars

    def draw_cars(self,img,cars):
        if cars is not None:
            for (x,y,w,h) in cars:
                cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2) 


class line_detector():
    def __init__(self, debug = False):
        self.debug = debug 

    def get_lines(self, img):
        canny_image = self.canny(img)
        cropped_image = self.region_of_interest(canny_image)
        lines = cv2.HoughLinesP(cropped_image,1,np.pi/180,100,np.array([]),minLineLength=15,maxLineGap=20)
        try:
            avg_lines,lines = self.get_lines_slope_intecept(img,lines)
        except :
            return lines,lines

        if self.debug:
           return avg_lines,lines
        
        return avg_lines,[]

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

    def draw_ROI(self,image):
        vertiexs = self.ROI(image)[0]
        lower_left, top_left, top_right, lower_right = vertiexs
        
        color_r = [0, 0, 255]
        color_g = [0, 255, 0]        
        line_width = 5

        cv2.line(image, tuple(lower_left), tuple(top_left), color_r, line_width)
        cv2.line(image, tuple(lower_left), tuple(lower_right), color_r , line_width * 2)
        cv2.line(image, tuple(top_right), tuple(lower_right), color_r, line_width)
        cv2.line(image, tuple(top_right), tuple(top_left), color_g, line_width)
        
        return image
    
    def ROI(self, image):
        ''' return list of numpy array with region vertics
        in order : lower_left, top_left, top_right, lower_right
        '''
        # height,width = image.shape[0:2]

        # bottom_left=(0,height) 
        # bottom_right= (0,int(height/2))
        # top_left=(width,height) 
        # top_right=(width,int(height/2)) 

        # src = np.array([
        #     [bottom_left,top_left,top_right,bottom_right]
        # ])          # Triangle polygon because cv2.fillPoly expects an array of polygons.

        imshape = image.shape
        lower_left = [0,imshape[0]]
        lower_right = [imshape[1],imshape[0]]
        top_left = [imshape[1]/2-imshape[1]/4,imshape[0]/2]
        top_right = [imshape[1]/2+imshape[1]/4,imshape[0]/2]
        vertices = [np.array([lower_left,top_left,top_right,lower_right],dtype=np.int32)]

        return vertices


    def region_of_interest(self, image):
        src = self.ROI(image)
        mask = np.zeros_like(image)   # Create a black mask to apply the above cube.
        cv2.fillPoly(mask,src,255)     # A complete white triangle polygon on a black mask.        
        masked_image = cv2.bitwise_and(image,mask)

        if self.debug:
            # cv2.imshow("mask",mask)
            cv2.imshow("masked_img",masked_image)

        return masked_image

    def color_mask(self,image):
        gray_image = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)  
        
        img_hsv = cv2.cvtColor(image,cv2.COLOR_RGB2HSV)  

        lower_yellow = np.array([30, 100, 100], dtype = "uint8")
        upper_yellow = np.array([100, 255, 255], dtype="uint8")
        mask_yellow = cv2.inRange(img_hsv, lower_yellow, upper_yellow)
        mask_white = cv2.inRange(gray_image, 170, 255)
        mask_yw = cv2.bitwise_or(mask_white, mask_yellow)

        mask_yw_image = cv2.bitwise_and(gray_image, mask_yw)

        if self.debug:
            cv2.imshow('white', mask_white)

        return mask_yw_image


    def canny(self, image):

        mask_yw_image = self.color_mask(image)


        kernel_size = 5
        gauss_gray = cv2.GaussianBlur(mask_yw_image,(kernel_size,kernel_size),0)


        low_threshold = 50
        high_threshold = 150
        canny_edges = cv2.Canny(gauss_gray,low_threshold,high_threshold)

        if self.debug:
            cv2.imshow('canny', canny_edges)
            
        return canny_edges
    

    def image_with_lines(self, img, lines):
        line_image = np.zeros_like(img)
        if lines is not None:
            for line in lines:
                x1,y1,x2,y2 = line.reshape(4)  # Reshaping all the lines to a 1D array.
                cv2.line(line_image,(x1,y1),(x2,y2),(255,0,0),10) # Draw a Blue Line(BGR in OpenCV)

        combo_image = cv2.addWeighted(img,0.8,line_image,1,1)    # Imposing the line_image on the original image
         
        return combo_image


            
    def get_lines_slope_intecept(self,img, lines):
        left_lines = []
        right_lines = []
        left_lengths = []
        right_lengths = []

        def get_line_length( line):
            x1, y1, x2, y2 = line
            return np.sqrt((y2-y1)**2 + (x2-x1)**2)

        def get_line_slope_intercept(line):
            
            x1, y1, x2, y2 = line
            if x2-x1 == 0:
                return np.inf, 0
            
            slope = (y2-y1)/(x2-x1)
            intercept = y1 - slope * x1
            return slope, intercept

        min_slope=-np.pi/8
        max_slope=np.pi/8

        filtered_lines_idx = []

        for idx in np.ndindex(lines.shape[:2]):
            line = lines[idx]
            slope, intercept = get_line_slope_intercept(line)
            if slope == np.inf:
                continue
            line_len = get_line_length(line)
            if slope < 0:
                if np.arctan(slope) < min_slope:
                    left_lines.append((slope, intercept))
                    left_lengths.append(line_len)
                else:
                    filtered_lines_idx.append(idx)
            else :
                if np.arctan(slope) > max_slope:
                    right_lines.append((slope, intercept))
                    right_lengths.append(line_len)
                else:
                    filtered_lines_idx.append(idx)

                
        
        filtered_lines = np.delete(lines,filtered_lines_idx,0)
                
        # average
        left_avg = np.dot(left_lengths, left_lines)/np.sum(left_lengths) if len(left_lengths) > 0 else None
        right_avg = np.dot(right_lengths, right_lines)/np.sum(right_lengths) if len(right_lengths) > 0 else None
        
        y1 = img.shape[0]
        y2 = img.shape[0] * .5


        def convert_slope_intercept_to_line(y1, y2 , line):
    
            slope, intercept = line
            x1 = int((y1- intercept)/slope)
            y1 = int(y1)
            x2 = int((y2- intercept)/slope)
            y2 = int(y2)
            return((x1, y1),(x2, y2))


        left_lane = convert_slope_intercept_to_line(y1, y2, left_avg)
        right_lane = convert_slope_intercept_to_line(y1, y2, right_avg)

        return np.array([left_lane, right_lane]),filtered_lines

