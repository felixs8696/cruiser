# http://richard.cgpublisher.com/product/pub.84/prod.11
# INTIALISATION
import pygame, math, sys
from pygame.locals import *

import cruiser
import utils

L_wheel = ("left", (-12, 0))
R_wheel = ("right", (12, 0))

board = cruiser.TwoWheelBoard(position=[350, 500], theta=0, l_board=80, w_board=24,
                              max_speed_mi_ph=20, wheel_diameter_cm=5.5, zero_to_max_vel_time_dt=20, dt=0.01,
                              wheel_tuples=[L_wheel, R_wheel])

BG= (0,0,0)
MAX_Y = 768
MAX_X = 1024

def gradient_surface(size, startcolor, endcolor):
    """
    Draws a vertical linear gradient filling the entire surface. Returns a
    surface filled with the gradient (numeric is only 2-3 times faster).
    """
    height = size[1]
    bigSurf = pygame.Surface((1,height), pygame.SRCALPHA).convert_alpha()
    dd = 1.0/height
    sr, sg, sb, sa = startcolor
    er, eg, eb, ea = endcolor
    rm = (er-sr)*dd
    gm = (eg-sg)*dd
    bm = (eb-sb)*dd
    am = (ea-sa)*dd
    for y in range(height):
        bigSurf.set_at((0,y),
                        (int(sr + rm*y),
                         int(sg + gm*y),
                         int(sb + bm*y),
                         int(sa + am*y))
                      )
    return pygame.transform.scale(bigSurf, size)

screen = pygame.display.set_mode((MAX_X, MAX_Y))
car = gradient_surface((10, 33), (255, 0, 255, 255), (0, 255, 255, 255))

clock = pygame.time.Clock() # load clock
k_up = k_down = k_left = k_right = 0 # init key values
speed = direction = 0 # start speed & direction
position = (350, 500) # start position

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

    screen.fill(BG)

    print(f"x: {x}")
    print(f"d: {d}")
    # if accelerate:
    if x == 0:
        board.move_target_ang_vel_to_zero()
    if x == 1:
        board.increase_target_ang_vel()
    if x == -1:
        board.decrease_target_ang_vel()

    if d == 0:
        board.move_target_diff_ang_vel_to_zero()
    if d == 1:
        board.increase_target_diff_ang_vel()
    if d == -1:
        board.decrease_target_diff_ang_vel()

    board.move_wheels_towards_targets()
    dx, dy, dtheta = board.change_in_position()

    board.position[0] += dx
    board.position[1] += dy
    board.theta += dtheta

    # print(f"Board position x diff: {dx * math.cos(board.theta)}")
    # print(f"Board position y diff: {dy * math.sin(board.theta)}")
    # print(f"Board position theta diff: {dtheta}")

    # make sure the car doesn't exit the screen
    if board.position[1] < 0:
        board.position[1] = 0 # TODO is there another way to treat this?
    elif board.position[1] > MAX_Y:
        board.position[1] = MAX_Y
    if board.position[0] < 0:
        board.position[0] = 0
    elif board.position[0] > MAX_X:
        board.position[0] = MAX_X

    rotated = pygame.transform.rotate(car, utils.rad_to_deg(board.theta))
    
    rect = rotated.get_rect()
    rect.center = board.position
    print(board.position)
    print(board.theta)
    
    screen.blit(rotated, rect)
    pygame.display.flip()

sys.exit(0) # quit the game
