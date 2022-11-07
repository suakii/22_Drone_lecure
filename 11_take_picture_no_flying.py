from djitellopy import Tello
import cv2
import time

tello = Tello()

tello.connect()

battery_level = tello.get_battery()
print(f"Battery Life Percentage: {battery_level}")

time.sleep(2)

print("Turn Video Stream On")
tello.streamon()

frame_read = tello.get_frame_read()

# print("Takeoff!")
# tello.takeoff()

time.sleep(2)

# read a single image from the Tello video feed
print("Read Tello Image")
tello_video_image = frame_read.frame

print("Write tello-picture.png")
# use opencv to write image
if tello_video_image is not None:
    cv2.imwrite("tello-picture.png", tello_video_image)

# tello.land()

tello.streamoff()
