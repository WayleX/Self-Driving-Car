import numpy as np
import cv2
import threading

camera_ready = -1

def init():
    model = 0
    return model
def check(model, picam2):
    global camera_ready, camera_command
    
    while True:
        (buffer, ), metadata = picam2.capture_buffers(["main"]) 
        pil_image = picam2.helpers.make_image(buffer, picam2.camera_configuration()["main"])
        x_size = pil_image.width



def get_camera():
    global picam2
    global camera_command
    global camera_ready
    epoch = 0
    while True:
        if camera_ready == 2:
            epoch += 1
            (buffer, ), metadata = picam2.capture_buffers(["main"]) 
            img = picam2.helpers.make_image(buffer, picam2.camera_configuration()["main"])
            open_cv_image = np.array(img.convert('RGB'))
            image = open_cv_image[:,:,::-1].copy()
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            lower = np.array([0,70,50])
            upper = np.array([10,255,255])
            mask = cv2.inRange(hsv, lower, upper)
            lower = np.array([170,70,50])
            upper = np.array([180,255,255])
            mask = mask | cv2.inRange(hsv, lower, upper)
            #result = cv2.bitwise_and(image, image, mask=mask)
            image_threshold = 1000
            destination_threshold = 5000
            if np.sum(mask>0) > destination_threshold:
                print('Peremoga')
            if np.sum(mask>0) > image_threshold:
                #ss = cv2.Sobel(mask, ddepth=cv2.CV_64F, dx = 1, dy =1,ksize=5)
                ss = mask
                ss = np.absolute(ss)
                ss = ss[100:,:]
                ss_sums = np.sum(ss, axis = 0)
                #print(np.sum(ss_sums))
                sum = 0
                for x in range(640):
                    sum += ((x-320)**2)*ss_sums[x]*np.sign(x-320)
                standartized_sum = sum/(np.sum(ss_sums)*320**2)
                #colsums = np.sum(ss,axis=1)
                #print(standartized_sum)
                if standartized_sum >= 0:
                    camera_command = 127*  min(1, 1.9 * (standartized_sum))
                elif standartized_sum < 0:
                    camera_command = 127*  max(-1, 1.9 * (standartized_sum))
                lock.acquire()
                camera_ready = 1
                lock.release()
