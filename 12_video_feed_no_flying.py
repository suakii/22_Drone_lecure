from djitellopy import Tello
import cv2
import time

tello = Tello()
tello.connect()

battery_level = tello.get_battery()
print(f"Battery Life Percentage: {battery_level}")

time.sleep(2)
tello.streamon()

# read a single image from the Tello video feed
print("Read Tello Image")
frame_read = tello.get_frame_read()

time.sleep(2)
while True:
    tello_video_image = frame_read.frame
    # use opencv to write image
    if tello_video_image is not None:
        cv2.imshow("TelloVideo", tello_video_image)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

tello.streamoff()
cv2.destroyWindow('TelloVideo')
cv2.destroyAllWindows()
cv2.waitKey(1)


