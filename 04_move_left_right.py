from djitellopy import Tello

tello = Tello()
tello.connect()

battery_level = tello.get_battery()
print(f"Battery Life Percentage: {battery_level}")

tello.takeoff()

tello.move_left(40) # Fly x cm left.
tello.move_right(40) # Fly x cm right.

tello.land()
