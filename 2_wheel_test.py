import cruiser
import environment

if __name__ == "__main__":
    board = cruiser.TwoWheelBoard(position=[350, 500], theta=0, l_board=80, w_board=24,
                                  max_speed_mi_ph=20, wheel_diameter_cm=5.5, zero_to_max_vel_time_dt=20, dt=0.01,
                                  wheel_tuples=[("left", (-12, 0)), ("right", (12, 0))])

    env = environment.Environment(board)

    env.start()