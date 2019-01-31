# http://richard.cgpublisher.com/product/pub.84/prod.11
# INTIALISATION
import pygame, math, sys
from pygame.locals import *

import utils
import pygame_utils as putils

class Environment(object):
    def __init__(self, board):
        self.BG= (0,0,0)
        self.MAX_Y = 768
        self.MAX_X = 1024
        self.board = board

    def start(self):
        screen = pygame.display.set_mode((self.MAX_X, self.MAX_Y))
        car = putils.gradient_surface((10, 33), (255, 0, 255, 255), (0, 255, 255, 255))
        clock = pygame.time.Clock() # load clock
        
        play = True
        x, d = 0, 0

        while play:

            clock.tick(30)

            for event in pygame.event.get():

                if not hasattr(event, 'key'):
                    continue

                if event.key == K_ESCAPE:
                    play = False

                down = event.type == KEYDOWN
                up = event.type == KEYUP

                if down:

                    if event.key == K_UP:
                        x = 1
                    if event.key == K_DOWN:
                        x = -1
                    if event.key == K_RIGHT:
                        d = 1
                    if event.key == K_LEFT:
                        d = -1

                if up:
                    if event.key == K_UP:
                        x = 0
                    if event.key == K_DOWN:
                        x = 0
                    if event.key == K_LEFT:
                        d = 0
                    if event.key == K_RIGHT:
                        d = 0

            screen.fill(self.BG)

            print(f"x: {x}")
            print(f"d: {d}")
            # if accelerate:
            if x == 0:
                self.board.move_target_ang_vel_to_zero()
            if x == 1:
                self.board.increase_target_ang_vel()
            if x == -1:
                self.board.decrease_target_ang_vel()

            if d == 0:
                self.board.move_target_diff_ang_vel_to_zero()
            if d == 1:
                self.board.increase_target_diff_ang_vel()
            if d == -1:
                self.board.decrease_target_diff_ang_vel()

            self.board.move_wheels_towards_targets()
            dx, dy, dtheta = self.board.change_in_position()

            self.board.position[0] += dx
            self.board.position[1] += dy
            self.board.theta += dtheta

            # print(f"Board position x diff: {dx * math.cos(self.board.theta)}")
            # print(f"Board position y diff: {dy * math.sin(self.board.theta)}")
            # print(f"Board position theta diff: {dtheta}")

            # make sure the car doesn't exit the screen
            if self.board.position[1] < 0:
                self.board.position[1] = 0 # TODO is there another way to treat this?
            elif self.board.position[1] > self.MAX_Y:
                self.board.position[1] = self.MAX_Y
            if self.board.position[0] < 0:
                self.board.position[0] = 0
            elif self.board.position[0] > self.MAX_X:
                self.board.position[0] = self.MAX_X

            rotated = pygame.transform.rotate(car, utils.rad_to_deg(self.board.theta))
            
            rect = rotated.get_rect()
            rect.center = self.board.position
            print(self.board.position)
            print(self.board.theta)
            
            screen.blit(rotated, rect)
            pygame.display.flip()

        sys.exit(0) # quit the game
