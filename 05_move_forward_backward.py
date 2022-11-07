from djitellopy import Tello

tello = Tello()
tello.connect()

battery_level = tello.get_battery()
print(f"Battery Life Percentage: {battery_level}")

tello.takeoff()

tello.move_forward(40)
tello.move_back(40)

tello.land()
