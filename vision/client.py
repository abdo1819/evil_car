import imagiz
import cv2
from find_lane import line_detector


client=imagiz.Client("cc1",server_ip="192.168.1.7")
vid=cv2.VideoCapture(0)

encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]

while True:
    r,frame=vid.read()
    if r:
        detector = line_detector()
        lines,lines_all = detector.get_lines(frame)
        lines_image  = detector.image_with_lines(frame,lines)

        r, image = cv2.imencode('.jpg', lines_image, encode_param)
        client.send(image)
    else:
        break
