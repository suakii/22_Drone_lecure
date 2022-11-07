from djitellopy import Tello
import time

tello = Tello()
tello.connect()

battery_level = tello.get_battery()
print(f"Battery Life Percentage: {battery_level}")

tello.takeoff()
time.sleep(2)

tello.flip_left()
time.sleep(2)

tello.flip_right()

tello.land()
