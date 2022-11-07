from djitellopy import Tello

tello = Tello()
tello.connect()

battery_level = tello.get_battery()
print(f"Battery Life Percentage: {battery_level}")

tello.takeoff()
tello.move_up(40)   # Fly x cm up.
tello.move_down(40) # Fly x cm down.
tello.land()

