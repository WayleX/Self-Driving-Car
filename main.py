import serial
import time
import threading
import dist_sensor
import car_controller
from picamera2 import Picamera2
import cv2
import numpy as np
picam2 = 0
camera_ready = 0
camera_command = ''

lock = threading.Lock()
def main():
    dist_sensor.init_sensor()

    with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
        time.sleep(1)
        
        if arduino.isOpen():
            time.sleep(3)
            print("{} connected!".format(arduino.port))

        car_controller.send_command(arduino, 'R'*400)
        car_controller.send_command(arduino, 'L'*72)
        epoch = 0
        global camera_ready
        global camera_command
        current_angle = 0
        lock.acquire()
        camera_ready = 2
        lock.release()
        while True:
            if camera_ready == 1:
                command = camera_command - current_angle
                #current_angle = camera_command

                if command < -2:
                    current_angle = camera_command
                    print('Livo', current_angle, command)
                    car_controller.send_command(arduino, abs(int(command)//2)*'L')
                    car_controller.send_command(arduino, abs(int(command)//2)*'L')
                elif command > 2:
                    current_angle = camera_command
                    print('Pravo', current_angle, command)
                    car_controller.send_command(arduino, abs(int(command))*'R')
                else:
                    print('Pryamo', current_angle)
                    pass
                time.sleep(0.1)
                lock.acquire()
                camera_ready = 2
                lock.release()
            epoch += 1
            d = dist_sensor.get_distance(timeout = 0.0001)
            if d < 27.0:
                d = dist_sensor.get_distance(timeout = 0.0001)
                if d <27.0:
                    print("STOOOP!")
                    # car_controller.send_command(arduino, "S")
                    car_controller.send_command(arduino, 20 * 'B')
                    break
                else:
                    car_controller.send_command(arduino, 7*'F')
            else:
                car_controller.send_command(arduino, 7 * 'F')


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
            #img.save(f'./res1{count}.png')
            open_cv_image = np.array(img.convert('RGB'))
            image = open_cv_image[:,:,::-1].copy()
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            lower = np.array([14,90,90])
            upper = np.array([20,255,255])
            mask = cv2.inRange(hsv, lower, upper)
            #result = cv2.bitwise_and(image, image, mask=mask)
            image_threshold = 1000
            if np.sum(mask>0) > image_threshold:
                ss = cv2.Sobel(mask, ddepth=cv2.CV_64F, dx = 1, dy =1,ksize=5)
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

            """
            height, width, _ = result.shape
            right_quarter = np.sum(result[:70, :width//4-40])
            left_quarter = np.sum(result[:70, 40 + 3*width//4:])
            left_half = result[:70, :-130+ width // 2]
            right_half = result[:70,130+ width // 2:]
            left_sum = np.sum(left_half)
            right_sum = np.sum(right_half)
            
            #cv2.imwrite(f'./res2{count}.jpg',result)
            if (right_sum > (left_sum+9000)*4):
                camera_ready = 1
                camera_command = max(-72,-15-4*right_quarter/right_sum)
                print('L', camera_command)
            elif(left_sum  > (right_sum+9000)*4):
                camera_ready = 1
                camera_command = min(72,15+4*left_quarter/left_sum)
                print('R', camera_command)
            """



if __name__ == "__main__":
    picam2 = Picamera2()
    time.sleep(1)
    picam2.configure(picam2.create_preview_configuration()) 
    time.sleep(2)
    picam2.start()
    time.sleep(3)
    print('Camera initialized')
    thread_one = threading.Thread(target=main)
    thread_two = threading.Thread(target=get_camera)

    thread_one.start()
    thread_two.start()
