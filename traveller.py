import serial
import time
import threading
import dist_sensor
import car_controller
from picamera2 import Picamera2
import numpy as np
import cv2
#import new

sensors_pins = {"F": (13, 15), "R": (16, 33), "L": (18, 35), "B": (22, 37)}

timeout = 0.0001

state = "F"

c = 10

#from new import *

ticks = 0
ff = 0
lock = threading.Lock()
camera_ready = -1
camera_command = ''
picam2 = None

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
            img.save(f'./huy__{epoch}.png')
            open_cv_image = np.array(img.convert('RGB'))
            image = open_cv_image[:,:,::-1].copy()
            hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
            lower = np.array([0,70,50])
            upper = np.array([5,255,255])
            mask = cv2.inRange(hsv, lower, upper)
            lower = np.array([175,70,50])
            upper = np.array([180,255,255])
            mask = mask | cv2.inRange(hsv, lower, upper)
            cv2.imwrite(f'./huyy__{epoch}.png', mask)
            #result = cv2.bitwise_and(image, image, mask=mask)
            image_threshold = 5500
            destination_threshold = 35000
            if np.sum(mask>0) > destination_threshold:
                camera_ready = 0
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


def decide(arduino, sensors_data):
    global state
    global ff
    global ticks
    if state == "F":
        ticks += 1
        if ff == -1  and ticks == 35:
            ff = 0
            car_controller.send_command(arduino, 'R'*60)
            ticks = 0
        if ff == 1 and ticks == 35:
            ff = 0
            ticks = 0
            car_controller.send_command(arduino, 'L'*60) 
        if sensors_data["F"] > 70:
            pass
        elif sensors_data["R"] - sensors_data["L"] > c or sensors_data["L"] < 25:
            car_controller.send_command(arduino, "B" * 5)
            if ff == 1:
                ff = 0
                car_controller.send_command(arduino, 'L'*60)
            if ff == -1:
                ff = 0
                car_controller.send_command(arduino, 'R'*60)
            car_controller.send_command(arduino, 'L'*60)
            state = "R"
        elif sensors_data["L"] - sensors_data["R"] > c or sensors_data["R"] < 25:
            car_controller.send_command(arduino, "B" * 5)
            if ff == 1:
                ff = 0
                car_controller.send_command(arduino, 'L'*60)
            if ff == -1:
                ff = 0
                car_controller.send_command(arduino, 'R'*60)
            car_controller.send_command(arduino, 'R'*60)
            state = "L"
    elif state == "R":
        if sensors_data["F"] > 70 and sensors_data["L"] > 40:
            car_controller.send_command(arduino, 'R'*120)
            state = "F"
            ff = 1
            ticks = 0
        else:
            pass
    elif state == "L":
        if sensors_data["F"] > 70 and sensors_data["R"] > 40:
            car_controller.send_command(arduino, 'L'*120)
            state = "F"
            ff = -1
            ticks = 0
        else:
            pass

import threading

def main():

    global camera_ready, camera_command

    #model = new.init()

    dist_sensor.init_all_sensors(sensors_pins)

    with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
        time.sleep(1)
        
        # Adjust wheels
        if arduino.isOpen():
            time.sleep(3)
            print("{} connected!".format(arduino.port))

        car_controller.send_command(arduino, 'R'*400)
        car_controller.send_command(arduino, 'L'*77)

        lock.acquire()
        camera_ready = 2
        lock.release()
        print("Start")
        while True:
            if camera_ready == 1:
                global ff
                if state == 'F':
                    current_angle = ff*120
                elif state == 'R':
                    current_angle = -100
                else:
                    current_angle = 100
                while True:



                    if camera_ready == 0:
                        print('Peremoga')
                        car_controller.send_command(arduino, 'B')
                        return 0
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
                    car_controller.send_command(arduino, 'F')
                    time.sleep(0.1)
            
#            print("better algos")
            sensors_data = dist_sensor.get_all_sensors_data(timeout, sensors_pins)
            print(sensors_data)
            decide(arduino,sensors_data)
            #time.sleep(0.005)
  #          print(state)
            
            if state == "F":
                car_controller.send_command(arduino, 'F'*10)
            else:
                car_controller.send_command(arduino, 'B'*20)

if __name__ == '__main__':
#w    global picam2
    picam2 = Picamera2()
    time.sleep(1)
    picam2.configure(picam2.create_preview_configuration()) 
    time.sleep(2)
    picam2.start()
    time.sleep(3)
    print('Camera initialized')

    model = 0

    thread_one = threading.Thread(target=main)
    thread_two = threading.Thread(target=get_camera)

    thread_one.start()
    thread_two.start()                  



