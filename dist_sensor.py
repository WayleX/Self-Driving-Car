#!/usr/bin/python
import time
import RPi.GPIO as GPIO


PIN_TRIGGER = 7
PIN_ECHO = 11

def init_sensor():
    GPIO.setmode(GPIO.BOARD)

    GPIO.setup(PIN_TRIGGER, GPIO.OUT)
    GPIO.setup(PIN_ECHO, GPIO.IN)

    GPIO.output(PIN_TRIGGER, GPIO.LOW)
    
    print("Sensor initialized.")


def get_distance(timeout):
    time.sleep(timeout)

    GPIO.output(PIN_TRIGGER, GPIO.HIGH)
    GPIO.output(PIN_TRIGGER, GPIO.LOW)

    while GPIO.input(PIN_ECHO) == 0:
        pulse_start_time = time.time()
        
    while GPIO.input(PIN_ECHO) == 1:
        pulse_end_time = time.time()

    pulse_duration = pulse_end_time - pulse_start_time
    distance = round(pulse_duration * 17150, 2)

    return distance

def cleanup():
    GPIO.cleanup()

