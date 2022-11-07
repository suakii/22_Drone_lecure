from djitellopy import Tello

tello = Tello()
tello.connect()

battery_level = tello.get_battery()
print(f"Battery Life Percentage: {battery_level}")

tello.takeoff()

tello.rotate_clockwise(90)
tello.rotate_counter_clockwise(90)

tello.land()
