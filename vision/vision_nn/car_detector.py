from __future__ import division
import cv2

from .models import Darknet
from .utils.utils import rescale_boxes, non_max_suppression, load_classes
from .utils.datasets import Image

import torch
from torchvision import transforms


class car_detector:
    def __init__(self):
        device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        model_def = 'vision_nn/config/yolov3.cfg'
        self.model = Darknet(model_def,img_size=416).to(device)

        weights_path = 'vision_nn/weights/yolov3.weights'
        self.model.load_darknet_weights(weights_path)



        self.model.eval()



    def find_cars(self, img):
        # Tensor = torch.cuda.FloatTensor if torch.cuda.is_available() else torch.FloatTensor
        # img = Variable(Tensor(img), requires_grad=False)

        transform = transforms.Compose([transforms.ToPILImage(),
                                        transforms.Resize((416, 416), interpolation=Image.NEAREST),
                                        # transforms.CenterCrop(416),
                                        transforms.ToTensor()])

        img_tensor = transform(img).unsqueeze(0).cuda()
        with torch.no_grad():
            # x,y,z = img.shape
            # img = img.view(1,x,y,z)
            # print(img.shape)
            outputs = self.model(img_tensor)
            # if not outputs.shape:
            outputs = non_max_suppression(outputs, .8, .4)[0]
            if outputs is not None:
                outputs = rescale_boxes(outputs, 416, img.shape[:2])



        return outputs

    def draw(self, img, detections):
        class_path = "vision_nn/data/coco.names"
        classes = load_classes(class_path)  # Extracts class labels from file

        if detections is not None:
            for x1, y1, x2, y2, conf, cls_conf, cls_pred in detections:

                w = x2 - x1
                h = y2 - y1
                
                print(type(x1))
                print(type(y1))
                print(type(w))
                print(type(h))

                cv2.rectangle(img,(x1,y1),(x1+w,y1+h),(0,0,255),2)

                font                   = cv2.FONT_HERSHEY_SIMPLEX
                bottomLeftCornerOfText = (x1,y1)
                fontScale              = 1
                fontColor              = (0,255,0)
                lineType               = 2


                cv2.putText(img,classes[int(cls_pred)],
                    bottomLeftCornerOfText,
                    font,
                    fontScale,
                    fontColor,
                    lineType)

        return img


# if __name__ == "__main__":
#     d = car_detector()
#     img = cv2.imread('../data/DATASET/images/469.jpg')
#     # img = torch.tensor(img).cuda()
#     cars = d.find_cars(img)
#     img = d.draw(img, cars)
#     cv2.imshow("dsa",img)
#     cv2.waitKey(0)

if __name__ == "__main__":
    d = car_detector()

    cap = cv2.VideoCapture("../data/gta/simple_two_lane.mp4")
    cv2.namedWindow('frame',cv2.WINDOW_NORMAL)
    # img = torch.tensor(img).cuda()

    while(True):
        # try:

        ret, img = cap.read()

        if ret:
            cars = d.find_cars(img)
            if cars is not None:
                img = d.draw(img, cars)
            cv2.imshow("frame",img)

        if(cv2.waitKey(1) == 27):
            break

