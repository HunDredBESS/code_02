import sys
from time import sleep
from picamera import PiCamera


file_name_path = sys.argv[1]
print(file_name_path)
camera = PiCamera()
camera.resolution = (240, 240)
camera.start_preview()
# Camera warm-up time
sleep(2)
camera.capture(file_name_path)
