import utils

# Constants in human readable units
max_speed_mi_ph = 20 # miles per hour (boosted board max speed)
wheel_diameter_cm = 5.5 # cm
0_to_max_vel_time_s = 4 # s

# Converted units better for computer and metric system
max_speed_me_ph = utils.mi_ph_to_me_ps(max_speed_mi_ph) # meters per sec
max_angular_velocity_rad_ps = utils.wheel_diam_cm_to_rad_ps(wheel_diameter_cm, max_speed_me_ph) # rad / s
ang_accel_rad_ps2 = max_angular_velocity / 0_to_max_vel_time_s # rad / s^2

# Initial wheel angular velocities
L_ang_vel, R_ang_vel = 0, 0

while play:
    clock.tick(30)
    for event in pygame.event.get():

        if not hasattr(event, 'key'):
            continue

        # Quit game
        if event.key == K_ESCAPE:
            play = False

        down = event.type == KEYDOWN
        up = event.type == KEYUP

        # Release key
        # All up
            # move max wheel in terms of vel. magnitude toward min wheel vel.
            # Move both wheels towards 0 together
        # S up + E down
        # S up + W down
        # N up + E down
        # N up + W down
        # S down + E up
        # S down + W up
        # N down + E up
        # N down + W up
            # move min wheel in terms of vel. magnitude toward max wheel vel.
        if down:

        if up:
            L_ang_accel *= -1
            R_ang_accel *= -1

        # Determine angular accelerations to speed up and/or turn
        if event.key == K_UP:
            L_ang_accel, R_ang_accel = ang_accel_rad_ps2, ang_accel_rad_ps2
        if event.key == K_DOWN:
            L_ang_accel, R_ang_accel = -ang_accel_rad_ps2, -ang_accel_rad_ps2
        if event.key == K_LEFT:
            L_ang_accel, R_ang_accel = -ang_accel_rad_ps2, ang_accel_rad_ps2
        if event.key == K_RIGHT:
            L_ang_accel, R_ang_accel = ang_accel_rad_ps2, -ang_accel_rad_ps2
    
    # Limit wheels to max angular velocities
    if abs(L_ang_vel) < max_angular_velocity_rad_ps:
        L_ang_vel += L_ang_accel
    else:
        if L_ang_vel <= -max_angular_velocity_rad_ps:
            L_ang_vel = -max_angular_velocity_rad_ps:
        if L_ang_vel >= max_angular_velocity_rad_ps:
            L_ang_vel = max_angular_velocity_rad_ps:

    if abs(R_ang_vel) < max_angular_velocity_rad_ps:
        R_ang_vel += R_ang_accel
    else:
        if R_ang_vel <= -max_angular_velocity_rad_ps:
            R_ang_vel = -max_angular_velocity_rad_ps:
        if R_ang_vel >= max_angular_velocity_rad_ps:
            R_ang_vel = max_angular_velocity_rad_ps: