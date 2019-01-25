import time

class PID:
    """ Simple PID control.

        This class implements a simplistic PID control algorithm. When first
        instantiated all the gain variables are set to zero, so calling
        the method GenOut will just return zero.
    """
    def __init__(self, p=0., i=0., d=0.):
        # Constants
        self.Kp = p
        self.Kd = i
        self.Ki = d

        self.t_curr = time.time()
        self.t_prev = self.t_curr

        self.prev_err = 0.

        # term result variables
        self.Cp = 0.
        self.Ci = 0.
        self.Cd = 0.

    def output(self, error):
        """ Performs a PID computation and returns a control value based on
            the elapsed time (dt) and the error signal from a summing junction
            (the error parameter).
        """
        self.t_curr = time.time()               # get t
        dt = self.t_curr - self.t_prev          # get delta t
        de = error - self.prev_err              # get delta error

        self.Cp = self.Kp * error               # proportional term
        self.Ci += error * dt                   # integral term

        self.Cd = 0
        if dt > 0:                              # no div by zero
            self.Cd = de/dt                     # derivative term

        self.t_prev = self.t_curr               # save t for next pass
        self.prev_err = error                   # save t-1 error

        # sum the terms and return the result
        return self.Cp + (self.Ki * self.Ci) + (self.Kd * self.Cd)

    def set_kp(self, p):
        self.Kp = p

    def set_ki(self, i):
        self.Ki = i

    def set_kd(self, d):
        self.Kd = d

    def set_prev_err(self, e):
        self.prev_err = e