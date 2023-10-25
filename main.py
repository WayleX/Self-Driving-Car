import serial
import time

import dist_sensor
import car_controller

def main():
    dist_sensor.init_sensor()

    with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
        time.sleep(1)
        
        if arduino.isOpen():
            time.sleep(3)
            print("{} connected!".format(arduino.port))

        
        # car_controller.send_command(arduino, "R" * 3)
        car_controller.send_command(arduino, "R" * 5)
        # car_controller.send_command(arduino, "R" * 3)
        car_controller.send_command(arduino, "R" * 5)


        car_controller.send_command(arduino, "L" * 3)
        car_controller.send_command(arduino, "L" * 3)

        # return 
        while True:
            d = dist_sensor.get_distance(timeout = 0.0001)
            print(d)
            if d < 50.0:

                print("STOOOP!")
                # car_controller.send_command(arduino, "S")
                car_controller.send_command(arduino, 2 * "B")
                break
            else:
                car_controller.send_command(arduino, "F")
        # for _ in range(3):
            # car_controller.send_command(arduino, "F")
            
if __name__ == "__main__":
    main()
