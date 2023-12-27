from dist_sensor import *
import time

cleanup()

pins = {"F": (13, 15), "R": (16, 33), "L": (18, 35), "B": (22, 37)}

init_all_sensors(pins)
time.sleep(6)

print("start")

while True:
	#print(get_distance(0.5, 22, 37))
	for key, value in pins.items():
		print(get_all_sensors_data(0.2, pins))
