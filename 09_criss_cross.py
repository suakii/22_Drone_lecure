from djitellopy import Tello
import time

tello = Tello()
tello.connect()

battery_level = tello.get_battery()
print(f"Battery Life Percentage: {battery_level}")

tello.takeoff()
time.sleep(1)

"""
Flight Patter
    2     4
    |\   /|
    | \ / |
    |  \  |
    | / \ |
   1 5   3

"""

travel_distance_cm = 50
#tello.go_xyz_speed(x,y,z, speed)

# x - (+)foward/(-)backwards
# y - (+)left/(-)right
# z - (+)up/(-)down
tello.go_xyz_speed(0, 0, travel_distance_cm, 20)
time.sleep(0.5)
tello.go_xyz_speed(0, travel_distance_cm, -travel_distance_cm, 20)
time.sleep(0.5)
tello.go_xyz_speed(0, 0, travel_distance_cm, 20)
time.sleep(0.5)

# x - (+)foward/(-)backwards
# y - (+)left/(-)right
# z - (+)up/(-)down
tello.go_xyz_speed(0, -travel_distance_cm, -travel_distance_cm, 20)
time.sleep(0.5)

tello.land()

