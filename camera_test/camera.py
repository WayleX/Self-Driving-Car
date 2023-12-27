from picamera2 import Picamera2
import time
import cv2

picam2 = Picamera2()
config = picam2.create_still_configuration(main= {"size": (1920, 1080)}, lores = {"size": (480, 320)}, display = "lores", buffer_count = 3, queue = False)
picam2.configure(config)

picam2.set_controls({"ExposureTime": 100, "AnalogueGain": 5}) #Shutter time and analogue signal boost
picam2.start(show_preview=True)

time.sleep(5)  #enjoy the preview

t_0 = time.monotonic()
img = picam2.capture_array("lores") #this takes a picture. img can be used with cv2
t_1 = time.monotonic()
picam2.close() #when you're done taking photos, this closes the camera connection

print("taking the photo took %s seconds", round(t_1-t_0, 3))
print("width height\t:", *img.shape[0:2][::-1])

img.