from picamera2 import Picamera2
import time
picam2 = Picamera2()
time.sleep(1) 
picam2.configure(picam2.create_preview_configuration()) 
time.sleep(2)
picam2.start()
time.sleep(3)
(buffer, ), metadata = picam2.capture_buffers(["main"]) 
img = picam2.helpers.make_image(buffer, picam2.camera_configuration()["main"])
#picam2.helpers.save('./true.jpg')
from PIL import Image
import numpy as np
open_cv_image = np.array(img)
image = open_cv_image[:,:,::-1].copy()
#image = open_cv_image.copy()
import cv2


hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
lower = np.array([10,150,150])
upper = np.array([40,255,255])
mask = cv2.inRange(hsv, lower, upper)
result = cv2.bitwise_and(image, image, mask=mask)





cv2.imwrite('./mask.jpg', mask)
cv2.imwrite('./result.jpg', result)
#cv2.waitKey()

#picam2.helpers.save(img, metadata, "file.jpg")