import utils
import math

class Wheel(object):
    def __init__(self, id, max_angular_velocity_rad_ps, ang_accel_rad_ps2, wheel_diameter_cm):
        self.id = id
        self.curr_ang_vel = 0 # rad / s
        self.wheel_diameter_cm = wheel_diameter_cm # cm
        self.max_angular_velocity_rad_ps = max_angular_velocity_rad_ps # rad / s
        self.ang_accel_rad_ps2  = ang_accel_rad_ps2# rad / s^2

    def accelerate_towards_limit(self, vel_limit):
        if vel_limit is None:
            vel_limit = self.max_angular_velocity_rad_ps
        if vel_limit > self.max_angular_velocity_rad_ps:
            vel_limit = self.max_angular_velocity_rad_ps
        if vel_limit < -self.max_angular_velocity_rad_ps:
            vel_limit = -self.max_angular_velocity_rad_ps

        if self.curr_ang_vel != vel_limit:
            if self.curr_ang_vel < vel_limit:
                if self.curr_ang_vel + self.ang_accel_rad_ps2 >= vel_limit:
                    self.curr_ang_vel = vel_limit
                else:
                    self.curr_ang_vel += self.ang_accel_rad_ps2
            if self.curr_ang_vel > vel_limit:
                if self.curr_ang_vel - self.ang_accel_rad_ps2 <= vel_limit:
                    self.curr_ang_vel = vel_limit
                else:
                    self.curr_ang_vel -= self.ang_accel_rad_ps2

        assert self.curr_ang_vel <= self.max_angular_velocity_rad_ps and self.curr_ang_vel >= -self.max_angular_velocity_rad_ps

    def decelerate_towards_zero(self):
        if self.curr_ang_vel != 0:
            if self.curr_ang_vel > 0:
                if self.curr_ang_vel - self.ang_accel_rad_ps2 <= 0:
                    self.curr_ang_vel = 0
                else:
                    self.curr_ang_vel -= self.ang_accel_rad_ps2
            if self.curr_ang_vel < 0:
                if self.curr_ang_vel + self.ang_accel_rad_ps2 >= 0:
                    self.curr_ang_vel = 0
                else:
                    self.curr_ang_vel += self.ang_accel_rad_ps2

        assert self.curr_ang_vel <= self.max_angular_velocity_rad_ps and self.curr_ang_vel >= -self.max_angular_velocity_rad_ps

class Board(object):
    def __init__(self, position=[350, 500], theta=0, l_board=80, w_board=24, max_speed_mi_ph=20, wheel_diameter_cm=5.5, zero_to_max_vel_time_s=10, dt=.01, wheel_tuples=[]):

        self.position = position
        self.theta = theta
        self.dt = dt

        self.l_board = l_board # cm
        self.w_board = w_board # cm

        self.l_plate = l_board/2 # cm
        self.w_plate = w_board # cm

        # Constants in human readable units
        self.max_speed_mi_ph = max_speed_mi_ph # miles per hour (boosted board max speed)
        self.wheel_diameter_cm = wheel_diameter_cm # cm
        self.zero_to_max_vel_time_s = zero_to_max_vel_time_s # s

        # Converted units better for computer and metric system
        self.max_speed_me_ph = utils.mi_ph_to_me_ps(max_speed_mi_ph) # meters per sec
        self.max_angular_velocity_rad_ps = utils.wheel_diam_cm_to_rad_ps(self.wheel_diameter_cm, self.max_speed_me_ph) # rad / s
        self.ang_accel_rad_ps2 = self.max_angular_velocity_rad_ps / self.zero_to_max_vel_time_s # rad / s^2

        self.wheels = {}
        
        for w_id, w_loc in wheel_tuples:
            self.wheels[str(w_id)] = {"obj": Wheel(w_id, self.max_angular_velocity_rad_ps, self.ang_accel_rad_ps2, self.wheel_diameter_cm), "loc": w_loc}

        # Max forward: max(w) = max_angular_velocity_rad_ps
        # Max backward: min(w) = -max_angular_velocity_rad_ps
        # left: max_angular_velocity_rad_ps, right: -max_angular_velocity_rad_ps
        # Max right turn: max(d) = 2 * max_angular_velocity_rad_ps
        # left: -max_angular_velocity_rad_ps, right: max_angular_velocity_rad_ps
        # Max left turn: min(d) = -2 * max_angular_velocity_rad_ps
        self.target_ang_vel = 0
        self.target_diff_ang_vel = 0

        print(f"max_angular_velocity_rad_ps: {self.max_angular_velocity_rad_ps}")
        print(f"ang_accel_rad_ps2: {self.ang_accel_rad_ps2}")

    def increase_target_ang_vel(self):
        if self.target_ang_vel + self.ang_accel_rad_ps2  >= self.max_angular_velocity_rad_ps:
            self.target_ang_vel = self.max_angular_velocity_rad_ps 
        else:
            self.target_ang_vel += self.ang_accel_rad_ps2 

        assert self.target_ang_vel <= self.max_angular_velocity_rad_ps and self.target_ang_vel >= -self.max_angular_velocity_rad_ps

    def decrease_target_ang_vel(self):
        if self.target_ang_vel - self.ang_accel_rad_ps2  <= -self.max_angular_velocity_rad_ps :
            self.target_ang_vel = -self.max_angular_velocity_rad_ps 
        else:
            self.target_ang_vel -= self.ang_accel_rad_ps2
        assert self.target_ang_vel <= self.max_angular_velocity_rad_ps and self.target_ang_vel >= -self.max_angular_velocity_rad_ps

    def move_target_ang_vel_to_zero(self):
        if self.target_ang_vel != 0:
            if self.target_ang_vel > 0:
                if self.target_ang_vel - self.ang_accel_rad_ps2 <= 0:
                    self.target_ang_vel = 0
                else:
                    self.target_ang_vel -= self.ang_accel_rad_ps2
            if self.target_ang_vel < 0:
                if self.target_ang_vel + self.ang_accel_rad_ps2 >= 0:
                    self.target_ang_vel = 0
                else:
                    self.target_ang_vel += self.ang_accel_rad_ps2
        assert self.target_ang_vel <= self.max_angular_velocity_rad_ps and self.target_ang_vel >= -self.max_angular_velocity_rad_ps

    # 2 * because both wheels accelerate to achieve d
    def increase_target_diff_ang_vel(self):
        if self.target_diff_ang_vel + self.ang_accel_rad_ps2  >= 2 * self.max_angular_velocity_rad_ps :
            self.target_diff_ang_vel = 2 * self.max_angular_velocity_rad_ps 
        else:
            self.target_diff_ang_vel += self.ang_accel_rad_ps2

        assert self.target_diff_ang_vel <= 2 * self.max_angular_velocity_rad_ps and self.target_diff_ang_vel >= -2 * self.max_angular_velocity_rad_ps

    def decrease_target_diff_ang_vel(self):
        if self.target_diff_ang_vel - self.ang_accel_rad_ps2  <= -2 * self.max_angular_velocity_rad_ps :
            self.target_diff_ang_vel = -2 * self.max_angular_velocity_rad_ps 
        else:
            self.target_diff_ang_vel -= self.ang_accel_rad_ps2

        assert self.target_diff_ang_vel <= 2 * self.max_angular_velocity_rad_ps and self.target_diff_ang_vel >= -2 * self.max_angular_velocity_rad_ps

    def move_target_diff_ang_vel_to_zero(self):
        if self.target_diff_ang_vel != 0:
            if self.target_diff_ang_vel > 0:
                if self.target_diff_ang_vel - self.ang_accel_rad_ps2 <= 0:
                    self.target_diff_ang_vel = 0
                else:
                    self.target_diff_ang_vel -= self.ang_accel_rad_ps2
            if self.target_diff_ang_vel < 0:
                if self.target_diff_ang_vel + self.ang_accel_rad_ps2 >= 0:
                    self.target_diff_ang_vel = 0
                else:
                    self.target_diff_ang_vel += self.ang_accel_rad_ps2

        assert self.target_diff_ang_vel <= 2 * self.max_angular_velocity_rad_ps and self.target_diff_ang_vel >= -2 * self.max_angular_velocity_rad_ps

    def get_wheel_objects():
        pass

    def get_wheel_locs():
        pass

    def move_wheels_towards_targets():
        pass

    def get_diff_ang_vel():
        pass

    def change_in_position():
        pass

class TwoWheelBoard(Board):
    def __init__(self, position=[350, 500], theta=0, l_board=80, w_board=24, max_speed_mi_ph=20, wheel_diameter_cm=5.5, zero_to_max_vel_time_s=4, dt=.01, wheel_tuples=[]):
        assert len(wheel_tuples) == 2, "There must be exactly 2 wheels on a TwoWheelBoard()"
        assert wheel_tuples[0][0] == "left", "id for left wheel must be 'left'"
        assert wheel_tuples[1][0] == "right", "id for right wheel must be 'right'"
        super().__init__(position, theta, l_board, w_board, max_speed_mi_ph, wheel_diameter_cm, zero_to_max_vel_time_s, dt, wheel_tuples)

    def get_wheel_objects(self):
        return self.wheels["left"]["obj"], self.wheels["right"]["obj"]

    def get_wheel_locs(self):
        return self.wheels["left"]["loc"], self.wheels["right"]["loc"]
    
    def get_diff_ang_vel(self):
        L_wheel, R_wheel = self.get_wheel_objects()
        assert L_wheel.curr_ang_vel <= self.max_angular_velocity_rad_ps and L_wheel.curr_ang_vel >= -self.max_angular_velocity_rad_ps
        assert R_wheel.curr_ang_vel <= self.max_angular_velocity_rad_ps and R_wheel.curr_ang_vel >= -self.max_angular_velocity_rad_ps
        return L_wheel.curr_ang_vel - R_wheel.curr_ang_vel

    def move_wheels_towards_targets(self):
        L_wheel, R_wheel = self.get_wheel_objects()
        curr_diff_ang_vel = self.get_diff_ang_vel()

        move_wheel_vels_apart = abs(curr_diff_ang_vel) < abs(self.target_diff_ang_vel)
        move_wheel_vels_close = abs(curr_diff_ang_vel) > abs(self.target_diff_ang_vel)
        move_wheel_vels_together = curr_diff_ang_vel == self.target_diff_ang_vel

        print(f"target_ang_vel: {self.target_ang_vel}")
        print(f"target_diff_ang_vel: {self.target_diff_ang_vel}")
        print(f"curr_diff_ang_vel: {curr_diff_ang_vel}")

        if move_wheel_vels_together:
            print(f"move_wheel_vels_together")
            L_wheel.accelerate_towards_limit(vel_limit=self.target_ang_vel)
            R_wheel.accelerate_towards_limit(vel_limit=self.target_ang_vel)

        if move_wheel_vels_close:
            print(f"move_wheel_vels_close")
            assert L_wheel.curr_ang_vel != R_wheel.curr_ang_vel, "L and R wheels should have different velocities here. If they have the same velocity, curr_diff_ang_vel == 0"
            L_wheel.accelerate_towards_limit(vel_limit=R_wheel.curr_ang_vel - (self.target_diff_ang_vel/2))
            R_wheel.accelerate_towards_limit(vel_limit=L_wheel.curr_ang_vel - (self.target_diff_ang_vel/2))

        if move_wheel_vels_apart:
            print(f"move_wheel_vels_apart")
            if self.target_diff_ang_vel >= 0:
                L_wheel.accelerate_towards_limit(vel_limit=self.target_ang_vel)
                R_wheel.accelerate_towards_limit(vel_limit=L_wheel.curr_ang_vel - self.target_diff_ang_vel)
            else:
                L_wheel.accelerate_towards_limit(vel_limit=-self.target_ang_vel)
                R_wheel.accelerate_towards_limit(vel_limit=L_wheel.curr_ang_vel - self.target_diff_ang_vel)

            print(f"L_wheel.curr_ang_vel: {L_wheel.curr_ang_vel}")
            print(f"R_wheel.curr_ang_vel: {R_wheel.curr_ang_vel}")

    def change_in_position(self):
        L_wheel, R_wheel = self.get_wheel_objects()
        L_wheel_loc, R_wheel_loc = self.get_wheel_locs()
        x, y = R_wheel_loc[0] - L_wheel_loc[0], R_wheel_loc[1] - L_wheel_loc[1]
        d = utils.hypotenuse(x, y) # distance_betwee_wheels

        dtheta = -(L_wheel.curr_ang_vel - R_wheel.curr_ang_vel) / d
        dtheta_dt = dtheta * self.dt
        
        dx = ((L_wheel.curr_ang_vel + R_wheel.curr_ang_vel) / 2) * math.sin(self.theta + (dtheta_dt / 2))
        dy = ((L_wheel.curr_ang_vel + R_wheel.curr_ang_vel) / 2) * math.cos(self.theta + (dtheta_dt / 2))

        dx_dt = dx * self.dt
        dy_dt = dy * self.dt

        return dx_dt, dy_dt, dtheta_dt
