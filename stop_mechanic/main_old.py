import serial
import time
import threading
import helping_files.dist_sensor as dist_sensor
import helping_files.car_controller as car_controller
from picamera2 import Picamera2
import cv2
import numpy as np
picam2 = 0
camera_ready = 0
camera_command = ''
def main():
    #dist_sensor.init_sensor()

    with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
        time.sleep(1)
        
        if arduino.isOpen():
            time.sleep(3)
            print("{} connected!".format(arduino.port))

        
        # car_controller.send_command(arduino, "R" * 3)
        #car_controller.send_command(arduino, "R" * 10)
        # car_controller.send_command(arduino, "R" * 3)
        #car_controller.send_command(arduino, "R" * 10)

        car_controller.send_command(arduino, 'R'*400)
        car_controller.send_command(arduino, 'L'*50)
        #car_controller.send_command(arduino, 'F'*300)
        #time.sleep(3)
        #car_controller.send_command(arduino, "L" * 4)
        #car_controller.send_command(arduino, "L" * 3)

        # return
        count = 0
        global camera_ready
        global camera_command
        current_angle = 0
        while False:
            if camera_ready == 1:
                camera_ready = 0
                angle_true = camera_command
                command = angle_true - current_angle
                current_angle = angle_true
                if command < 0:
                    print('HUy left', abs(int(command)))
                    car_controller.send_command(arduino, abs(int(command))*'L')
                elif command > 0:
                    print('Huy right', command)
                    car_controller.send_command(arduino, abs(int(command))*'R')
                else:
                    print('pizduy')
                continue
            
            count += 1
            d = dist_sensor.get_distance(timeout = 0.0003)
            #print(current_angle)
            if d < 20.0:
                d = dist_sensor.get_distance(timeout = 0.0003)
                if d <20.0:
                    print("STOOOP!")
                    # car_controller.send_command(arduino, "S")
                    car_controller.send_command(arduino, 20 * 'B')
                    break
            else:
                car_controller.send_command(arduino, 4 * 'F')
        # for _ in range(3):
            # car_controller.send_command(arduino, "F")

def get_camera():
    global picam2
    global camera_command
    global camera_ready
    count = 0
    while True:
        count +=1
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
        #height, width, _ = result.shape
        vision = 250
        """
        right_quarter = np.sum(result[:vision, :width//4 + 50])
        left_quarter = np.sum(result[:vision, 3*width//4 -50:])
        buffer = 70
        
        left_half = result[:vision, :-buffer+ width // 2]
        right_half = result[:vision,buffer+ width // 2:]
        left_sum = np.sum(left_half)
        right_sum = np.sum(right_half)
        #cv2.imwrite(f'./res2{count}.jpg',result)
        if (right_sum > (left_sum+6000)*4):
            camera_ready = 1
            camera_command = max(-80,-27-4*right_quarter/right_sum)
            cv2.imwrite(f'./result_lllll_{count}.jpg', result[:vision,:])
            #print('L', camera_command)
        elif(left_sum  > (right_sum+6000)*4):
            camera_ready = 1
            camera_command = min(80,27+4*left_quarter/left_sum)
            cv2.imwrite(f'./result_rrrrr_{count}.jpg', result[:vision,:])
            #print('R', camera_command)
        else:
            camera_ready = 1
            camera_command = 0
        """
        
        for y in range(480):
            for x in range(640):
                count += 1
                if x > 200 and x < 400:
                    continue
                if mask[y][x] > 0:
                    sum += (x-320)
        camera_command = 120*sum/count
        camera_ready = 1

if __name__ == "__main__":
    #picam2 = Picamera2()
    time.sleep(1) 
    #picam2.configure(picam2.create_preview_configuration()) 
    time.sleep(2)
    #picam2.start()
    time.sleep(3)
    print('Camera initialized')
    #thread_one = threading.Thread(target=main)
    #thread_two = threading.Thread(target=get_camera)
    main()
    #thread_one.start()
    #thread_two.start()
