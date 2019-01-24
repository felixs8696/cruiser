import math
import numpy as np

def lb_to_kg(x):
	return .45 * x

def kg_to_lb(x):
	return x / .45

def force(m, a):
	return m * a

def rad_to_deg(rad):
	return rad * 180. / np.pi

def deg_to_rad(deg):
	return deg * np.pi / 180.

#rotate x,y around xo,yo by theta (rad)
def rotate(x,y,xo,yo,theta):
    xr=math.cos(theta)*(x-xo)-math.sin(theta)*(y-yo)   + xo
    yr=math.sin(theta)*(x-xo)+math.cos(theta)*(y-yo)  + yo
    return [xr,yr]