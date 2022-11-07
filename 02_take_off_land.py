from djitellopy import Tello
import time

tello = Tello()
tello.connect()

battery = tello.get_battery()
print(f"Battery Life Percentage: {battery}")

tello.takeoff()
time.sleep(5)
tello.land()
