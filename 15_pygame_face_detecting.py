from djitellopy import Tello
import cv2
import pygame
import numpy as np
import time
import sys
from pyimagesearch.objcenter import ObjCenter
from pyimagesearch.pid import  PID
import imutils
from datetime import datetime


# Speed of the drone
S = 60
# Frames per second of the pygame window display
# A low number also results in input lag, as input information is processed once per frame.
FPS = 120


class FrontEnd(object):
    """ Maintains the Tello display and moves it through the keyboard keys.
        Press escape key to quit.
        The controls are:
            - T: Takeoff
            - L: Land
            - Arrow keys: Forward, backward, left and right.
            - A and D: Counter clockwise and clockwise rotations (yaw)
            - W and S: Up and down.
    """

    def __init__(self):
        # Init pygame
        pygame.init()

        # Creat pygame window
        pygame.display.set_caption("Tello video stream")
        self.screen = pygame.display.set_mode([640*2, 480]) #왼쪽은 원래 이미지, 오른쪽은 detect

        # Init Tello object that interacts with the Tello drone
        self.tello = Tello()

        # Drone velocities between -100~100
        self.for_back_velocity = 0
        self.left_right_velocity = 0
        self.up_down_velocity = 0
        self.yaw_velocity = 0
        self.speed = 10

        self.send_rc_control = False

        #face tracking
        self.face_center = ObjCenter("./haarcascade_frontalface_default.xml")


        # create update timer
        pygame.time.set_timer(pygame.USEREVENT + 1, 1000 // FPS)

    def run(self):
        self.tello.connect()
        self.tello.set_speed(self.speed)
        # In case streaming is on. This happens when we quit this program without the escape key.
        self.tello.streamoff()
        self.tello.streamon()

        frame_read = self.tello.get_frame_read()
        time.sleep(5)
        should_stop = False
        while not should_stop:
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT + 1:
                    self.update()
                elif event.type == pygame.QUIT:
                    should_stop = True
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        should_stop = True
                    else:
                        self.keydown(event.key)
                elif event.type == pygame.KEYUP:
                    self.keyup(event.key)

            if frame_read.stopped:
                break

            self.screen.fill([0, 0, 0])
            frame = frame_read.frame
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = imutils.resize(frame, width=640)

            if frame is not None:
                frame_copy = frame.copy()

                # text = "Battery: {}%".format(self.tello.get_battery())
                # cv2.putText(frame, text, (5, 200 - 5),
                #             cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2)

                detect_face_frame = self.find_face(frame_copy) #face detect

                frame = frame.swapaxes(0, 1)
                detect_face_frame = detect_face_frame.swapaxes(0, 1)

                self.screen.blit(pygame.surfarray.make_surface(frame), [0, 0])
                self.screen.blit(pygame.surfarray.make_surface(detect_face_frame), [640, 0])

            pygame.display.update()
            time.sleep(1 / FPS)


        # Call it always before finishing. To deallocate resources.
        self.tello.end()

    # find face
    def find_face(self, frame):
        # frame = imutils.resize(frame, width=400)
        H, W, _ = frame.shape
        frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)  # opencv is bgr
        # calculate the center of the frame as this is (ideally) where
        # we will we wish to keep the object
        centerX = W // 2
        centerY = H // 2

        cv2.circle(frame, center=(centerX, centerY), radius=5, color=(0, 0, 255), thickness=-1)

        # find the object's location
        frame_center = (centerX, centerY)
        objectLoc = self.face_center.update(frame, frameCenter=None)
        ((objX, objY), rect, d) = objectLoc
        if rect is not None:
            (x, y, w, h) = rect
            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            cv2.circle(frame, center=(objX, objY), radius=5, color=(255, 0, 0), thickness=-1)
            cv2.arrowedLine(frame, frame_center, (objX, objY), color=(0, 255, 0), thickness=2)

        return cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    def keydown(self, key):
        """ Update velocities based on key pressed
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP:  # set forward velocity
            self.for_back_velocity = S
        elif key == pygame.K_DOWN:  # set backward velocity
            self.for_back_velocity = -S
        elif key == pygame.K_LEFT:  # set left velocity
            self.left_right_velocity = -S
        elif key == pygame.K_RIGHT:  # set right velocity
            self.left_right_velocity = S
        elif key == pygame.K_w:  # set up velocity
            self.up_down_velocity = S
        elif key == pygame.K_s:  # set down velocity
            self.up_down_velocity = -S
        elif key == pygame.K_a:  # set yaw counter clockwise velocity
            self.yaw_velocity = -S
        elif key == pygame.K_d:  # set yaw clockwise velocity
            self.yaw_velocity = S

    def keyup(self, key):
        """ Update velocities based on key released
        Arguments:
            key: pygame key
        """
        if key == pygame.K_UP or key == pygame.K_DOWN:  # set zero forward/backward velocity
            self.for_back_velocity = 0
        elif key == pygame.K_LEFT or key == pygame.K_RIGHT:  # set zero left/right velocity
            self.left_right_velocity = 0
        elif key == pygame.K_w or key == pygame.K_s:  # set zero up/down velocity
            self.up_down_velocity = 0
        elif key == pygame.K_a or key == pygame.K_d:  # set zero yaw velocity
            self.yaw_velocity = 0
        elif key == pygame.K_t:  # takeoff
            self.tello.takeoff()
            self.send_rc_control = True
        elif key == pygame.K_l:  # land
            not self.tello.land()
            self.send_rc_control = False

    def update(self):
        """ Update routine. Send velocities to Tello."""
        if self.send_rc_control:
            self.tello.send_rc_control(self.left_right_velocity, self.for_back_velocity,
                self.up_down_velocity, self.yaw_velocity)


def main():
    frontend = FrontEnd()

    # run frontend
    frontend.run()


if __name__ == '__main__':
    main()


