# http://richard.cgpublisher.com/product/pub.84/prod.11
# INTIALISATION
import pygame, math, sys
from pygame.locals import *

import cruiser
import utils

L_wheel = ("left", (-12, 0))
R_wheel = ("right", (12, 0))

board = cruiser.TwoWheelBoard(position=[350, 500], theta=0, l_board=80, w_board=24,
                              max_speed_mi_ph=10, wheel_diameter_cm=5.5, zero_to_max_vel_time_s=20, dt=0.01,
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
car = gradient_surface((10, 20), (255, 0, 255, 255), (0, 255, 255, 255))

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

        # if up:
        #     if event.key == K_UP or event.key == K_DOWN:
        #         board.move_target_ang_vel_to_zero()
        #         print("move target ang vel to zero")
        #     if event.key == K_LEFT or event.key == K_RIGHT:
        #         board.move_target_diff_ang_vel_to_zero()
        #         print("move target diff vel to zero")

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
    delta_x, delta_y, delta_theta = board.change_in_position()

    # board.position[0] += delta_x * math.cos(board.theta)
    # board.position[1] += delta_y * math.sin(board.theta)
    # board.theta += delta_theta

    board.position[0] += delta_x
    board.position[1] += delta_y
    board.theta += delta_theta

    # print(f"Board position x diff: {delta_x * math.cos(board.theta)}")
    # print(f"Board position y diff: {delta_y * math.sin(board.theta)}")
    # print(f"Board position theta diff: {delta_theta}")

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

# import utils
# import cruiser

# # Constants in human readable units
# # max_speed_mi_ph = 20 # miles per hour (boosted board max speed)
# # wheel_diameter_cm = 5.5 # cm
# # 0_to_max_vel_time_s = 4 # s

# # # Converted units better for computer and metric system
# # max_speed_me_ph = utils.mi_ph_to_me_ps(max_speed_mi_ph) # meters per sec
# # max_angular_velocity_rad_ps = utils.wheel_diam_cm_to_rad_ps(wheel_diameter_cm, max_speed_me_ph) # rad / s
# # ang_accel_rad_ps2 = max_angular_velocity / 0_to_max_vel_time_s # rad / s^2

# # # Initial wheel angular velocities
# # L_ang_vel, R_ang_vel = 0, 0
# # Max forward: max(w) = max_angular_velocity_rad_ps
# # Max backward: min(w) = -max_angular_velocity_rad_ps
# # left: max_angular_velocity_rad_ps, right: -max_angular_velocity_rad_ps
# # Max right turn: max(d) = 2 * max_angular_velocity_rad_ps
# # left: -max_angular_velocity_rad_ps, right: max_angular_velocity_rad_ps
# # Max left turn: min(d) = -2 * max_angular_velocity_rad_ps
# # w, d = 0, 0
# L_wheel = ("left", (-12, 0))
# R_wheel = ("right", (12, 0))

# board = cruiser.TwoWheelBoard(l_board=80, w_board=24,
#                       max_speed_mi_ph=20, wheel_diameter_cm=5.5, zero_to_max_vel_time_s=4,
#                       wheel_tuples=[L_wheel, R_wheel])

# if down:
#     if event.key == K_UP:
#         cruiser.increase_target_ang_vel()
#     if event.key == K_DOWN:
#         cruiser.decrease_target_ang_vel()
#     if event.key == K_LEFT:
#         cruiser.increase_target_diff_ang_vel()
#     if event.key == K_RIGHT:
#         cruiser.decrease_target_diff_ang_vel()

# while play:
#     clock.tick(30)
#     for event in pygame.event.get():

#         if not hasattr(event, 'key'):
#             continue

#         # Quit game
#         if event.key == K_ESCAPE:
#             play = False

#         down = event.type == KEYDOWN
#         up = event.type == KEYUP

#         # Release key
#         # All up
#             # move max wheel in terms of vel. magnitude toward min wheel vel.
#             # Move both wheels towards 0 together
#         # S up + E down
#         # S up + W down
#         # N up + E down
#         # N up + W down
#         # S down + E up
#         # S down + W up
#         # N down + E up
#         # N down + W up
#             # move min wheel in terms of vel. magnitude toward max wheel vel.
#         if down:

#         if up:
#             L_ang_accel *= -1
#             R_ang_accel *= -1

#         # Determine angular accelerations to speed up and/or turn
#         if event.key == K_UP:
#             L_ang_accel, R_ang_accel = ang_accel_rad_ps2, ang_accel_rad_ps2
#         if event.key == K_DOWN:
#             L_ang_accel, R_ang_accel = -ang_accel_rad_ps2, -ang_accel_rad_ps2
#         if event.key == K_LEFT:
#             L_ang_accel, R_ang_accel = -ang_accel_rad_ps2, ang_accel_rad_ps2
#         if event.key == K_RIGHT:
#             L_ang_accel, R_ang_accel = ang_accel_rad_ps2, -ang_accel_rad_ps2
    
#     # Limit wheels to max angular velocities
#     if abs(L_ang_vel) < max_angular_velocity_rad_ps:
#         L_ang_vel += L_ang_accel
#     else:
#         if L_ang_vel <= -max_angular_velocity_rad_ps:
#             L_ang_vel = -max_angular_velocity_rad_ps:
#         if L_ang_vel >= max_angular_velocity_rad_ps:
#             L_ang_vel = max_angular_velocity_rad_ps:

#     if abs(R_ang_vel) < max_angular_velocity_rad_ps:
#         R_ang_vel += R_ang_accel
#     else:
#         if R_ang_vel <= -max_angular_velocity_rad_ps:
#             R_ang_vel = -max_angular_velocity_rad_ps:
#         if R_ang_vel >= max_angular_velocity_rad_ps:
#             R_ang_vel = max_angular_velocity_rad_ps: