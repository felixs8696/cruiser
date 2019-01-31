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

def mi_to_m(mi):
	return mi / 1609.34

def cm_to_m(m):
	return m / 100.

def radius_to_circum(r):
	return np.pi * (r**2.)

def hours_to_sec(h):
	return h * 3600.

def rev_to_rad(rev):
	return 2. * np.pi * rev

def rad_to_rev(rad):
	return rad / (2. * np.pi)

def mi_ph_to_me_ps(mi_ph):
	me_ph = mi_to_m(mi_ph)
	me_ps = me_ph * hours_to_sec(1.)
	return me_ps

def ang_vel_rad_ps_to_lin_vel_me_ps(ang_vel, wheel_diam):
	wheel_radius = wheel_diam / 2. # cm
	cm_ps = rad_to_rev(ang_vel) * radius_to_circum(wheel_radius)
	return cm_ps / 100.

def hypotenuse(x, y):
	return math.sqrt(x**2. + y**2)

def circum_ratio_to_angle_rad(ratio):
	return ratio * 2. * np.pi

def circum_ratio_to_angle_deg(ratio):
	return ratio * 360.

def arc_cm_angle_rad_to_radius_cm(arc, theta):
	return arc / theta

def chord_from_radius_cm_and_angle_rad(r, theta):
	return 2. * r * math.sin(theta/2.)

def vec_2D_to_components(vec, theta):
	return vec * math.cos(theta), vec * math.sin(theta)

def base_angles_of_isosceles_triangle_rad(theta):
	return (np.pi - theta)/2.

# target_ang_vel = me_ps
def wheel_diam_cm_to_rad_ps(d, target_ang_vel):
	me_per_rev = cm_to_m(radius_to_circum(d/2))
	rev_ps = target_ang_vel / me_per_rev
	return rev_to_rad(rev_ps)

#rotate x,y around xo,yo by theta (rad)
def rotate(x,y,xo,yo,theta):
	xr=math.cos(theta)*(x-xo)-math.sin(theta)*(y-yo)   + xo
	yr=math.sin(theta)*(x-xo)+math.cos(theta)*(y-yo)  + yo
	return [xr,yr]
