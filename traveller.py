import serial
import time
import threading
import dist_sensor
import car_controller

sensors_pins = {
    "F": (0, 1),
    "R": (0, 1),
    "L": (0, 1),
    "B": (0, 1)
}

timeout = 0.0001

def decide(arduino, sensors_data, state):
    if state == "F":
        if sensors_data["F"] > 100:
            pass
        elif sensors_data["R"] > sensors_data["L"]:
            car_controller.send_command(arduino, 'L'*60)
            state = "R"
        elif sensors_data["R"] < sensors_data["L"]:
            car_controller.send_command(arduino, 'R'*60)
            state = "L"
    if state == "R":
        if sensors_data["F"] > 100:
            car_controller.send_command(arduino, 'R'*60)
            state = "F"
        else:
            pass
    if state == "L":
        if sensors_data["F"] > 100:
            car_controller.send_command(arduino, 'L'*60)
            state = "F"
        else:
            pass

def main():
    dist_sensor.init_all_sensors()

    with serial.Serial("/dev/ttyUSB0", 9600, timeout=1) as arduino:
        time.sleep(1)
        
        # Adjust wheels
        if arduino.isOpen():
            time.sleep(3)
            print("{} connected!".format(arduino.port))

        car_controller.send_command(arduino, 'R'*400)
        car_controller.send_command(arduino, 'L'*72)

        state = "F"

        while True:
            sensors_data = dist_sensor.get_all_sensors_data(timeout, sensors_pins)
            
            decide(arduino,sensors_data, state)
            time.sleep(0.005)
            if state == "F":
                car_controller.send_command(arduino, 'F'*10)
            else:
                car_controller.send_command(arduino, 'B'*10)
        

                    



