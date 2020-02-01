from res.models.erfnet import Net

import torch
import torch.nn.functional as F
from torch.autograd import Variable

import numpy as np
import cv2

import os

COLORS_DEBUG = [(255,0,0), (0,0,255)]


class lane_detector_nn():
    
    def __init__(self,debug=False):
        self.resize_factor = 5
        self.debug = debug
        self.cnn = Net().cpu()
        # weights_name = 'weights_erfnet_road.pth'
        weights_name = 'weights_erfnet.pth'


        weights_path = os.path.join('res', 'weights', weights_name)
        # weights_path = 'state_dict.pth'

        if torch.cuda.is_available():
            torch.cuda.device(0)
            self.cnn = torch.nn.DataParallel(self.cnn).cuda()
        
        
        self.cnn.load_state_dict(torch.load(weights_path))
        # torch.save(self.cnn.state_dict(),'state_dict.pt')
        # print('saved')
        
        self.cnn.eval()
    
    def img_received_callback(self, image):
        input_tensor = torch.from_numpy(image)
        input_tensor = torch.div(input_tensor.float(), 255)
        input_tensor = input_tensor.permute(2,0,1).unsqueeze(0)

        with torch.no_grad():
            input_tensor = Variable(input_tensor).cuda()
            # input_tensor = Variable(input_tensor).cpu()
            
            output = self.cnn(input_tensor)
        
        # output, output_road = output
        output = output

        # road_type = output_road.max(dim=1)[1][0]
        
        ### Classification
        output = output.max(dim=1)[1]
        output = output.float().unsqueeze(0)

        ### Resize to desired scale for easier clustering

        size = (int(output.size(2) / self.resize_factor), int(output.size(3) / self.resize_factor))
        output = F.interpolate(output,
                            size= size,
                            mode='nearest')

        ### Obtaining actual output
        ego_lane_points = torch.nonzero(output.squeeze() == 1)
        other_lanes_points = torch.nonzero(output.squeeze() == 2)

        ego_lane_points = ego_lane_points.view(-1).cpu().numpy()
        other_lanes_points = other_lanes_points.view(-1).cpu().numpy()

        if self.debug:
            # Convert the image and substitute the colors for egolane and other lane
            output = output.squeeze().unsqueeze(2).data.cpu().numpy()
            output = output.astype(np.uint8)

            output = cv2.cvtColor(output, cv2.COLOR_GRAY2RGB)
            output[np.where((output == [1, 1, 1]).all(axis=2))] = COLORS_DEBUG[0]
            output[np.where((output == [2, 2, 2]).all(axis=2))] = COLORS_DEBUG[1]

            # Blend the original image and the output of the self.
            output = cv2.resize(output, (image.shape[1], image.shape[0]), interpolation=cv2.INTER_NEAREST)
            image = cv2.addWeighted(image, 1, output, 0.4, 0)
            
            # Visualization
            cv2.imshow("frame", cv2.resize(image, (320, 240), cv2.INTER_NEAREST))
            cv2.waitKey(1)