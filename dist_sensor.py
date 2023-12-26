#!/usr/bin/python
import time
import RPi.GPIO as GPIO


def init_all_sensors(sensor_pins: dict[str, tuple[int, int]]):
    for key, value in sensor_pins.items():
        init_sensor(value[0], value[1])
        print(f"Sensor {key} initialized")

    print("All sensors initialized")

def get_all_sensors_data(timeout, sensor_pins: dict[str, tuple[int, int]]) -> dict[str, float]:
    res = {}
    for key, value in sensor_pins.items():
        res[key] = get_distance(timeout, value[0], value[1])

    return res

def init_sensor(trigger, echo):
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(trigger, GPIO.OUT)
    GPIO.setup(echo, GPIO.IN)

    GPIO.output(trigger, GPIO.LOW)


def get_distance(timeout, trigger, echo):
    time.sleep(timeout)

    GPIO.output(trigger, GPIO.HIGH)
    GPIO.output(trigger, GPIO.LOW)

    while GPIO.input(echo) == 0:
        pulse_start_time = time.time()
        
    while GPIO.input(echo) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)

    return distance

def cleanup():
    GPIO.cleanup()

