import time

import numpy as np

import matplotlib as mpl
mpl.use('TkAgg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches

import utils
from pid import PID

ALLOWABLE_ERROR = 1e-6

m_human = utils.lb_to_kg(150) # kg
m_board = utils.lb_to_kg(25) # kg
v_max = 8 # m/s
v_min = 0
g_a = 9.81 # m/s^2

l_board = 80 # cm
w_board = 24 # cm
l_plate = l_board/2 # cm
w_plate = w_board
plt_pad = 5 # cm

front_wheel_origin = [0], [l_plate/2]
board_origin = [0], [0]
back_wheel_origin = [0], [-l_plate/2]

def weights_to_forces(weights):
	return weights * g_a

# Vector magnitude along the positive (L to R) front wheel X-axis
def front_vec(forces):
	x = forces[0][1] - forces[0][0]
	y = 0.
	return x, y

# Vector magnitude along the positive (L to R) back wheel X-axis
def back_vec(forces):
	x = forces[1][1] - forces[1][0]
	y = 0.
	return x, y

# Vector magnitude along the X axis and Y axis from the center of the board
def center_vec(forces):
	x = forces[0][1] + forces[1][1] - (forces[0][0] + forces[1][0])
	y = forces[0][0] + forces[0][1] - (forces[1][0] + forces[1][1])
	return x, y

# [[front_L, front_R], [back_L, back_R]]
forces = np.array([[0., 0.], [0., 0.]])
weights = np.array([[m_human/4., m_human/4.], [m_human/4., m_human/4.]])

print(f'Human force: {m_human * g_a}')

fig, ax = plt.subplots(1)

pid_ctrl = PID(p=1.2, i=0, d=0)

for i in range(20):
	ax.plot(0,0,'ok') #<-- plot a black point at the origin
	ax.axis('equal')  #<-- set the axes to the same scale
	plt.xlim([-w_plate/2 - plt_pad, w_plate/2 + plt_pad]) #<-- set the x axis limits
	plt.ylim([-l_plate/2 - plt_pad, l_plate/2 + plt_pad]) #<-- set the y axis limits
	ax.grid(b=True, which='major')

	weights = np.random.random(size=4).reshape((2,2))
	weights /= np.sum(weights)
	weights *= m_human
	assert np.sum(weights) - m_human <= ALLOWABLE_ERROR
	print(f'weights: {weights}')

	forces = weights_to_forces(weights)
	print(f'forces: {forces}')

	vec_front = front_vec(forces)
	print(f'vec_front: {vec_front}')
	vec_center = center_vec(forces)
	print(f'vec_center: {vec_center}')
	vec_back = back_vec(forces)
	print(f'vec_back: {vec_back}')
	
	vec_scale = (m_human*g_a)/(min(w_plate, l_plate)/2)

	# Draw central vectors
	# Black = Intended direction (human applied force)
	# Blue = Vectors along each major axis
	ax.quiver(*board_origin, vec_center[0], 0, color='b', angles='xy', scale_units='xy', scale=vec_scale)
	ax.quiver(*board_origin, 0, vec_center[1], color='b', angles='xy', scale_units='xy', scale=vec_scale)
	ax.quiver(*board_origin, vec_center[0], vec_center[1], color='k', angles='xy', scale_units='xy', scale=vec_scale)

	# Draw front and back vectors
	ax.quiver(*front_wheel_origin, vec_front[0], vec_front[1], color='r', angles='xy', scale_units='xy', scale=vec_scale)
	ax.quiver(*back_wheel_origin, vec_back[0], vec_back[1], color='r', angles='xy', scale_units='xy', scale=vec_scale)

	force_plate = patches.Rectangle((-w_plate/2,-l_plate/2), w_plate, l_plate,linewidth=1,edgecolor='r',facecolor='none')
	ax.add_patch(force_plate)

	# Transform board to rotate to vector
	theta_rad = np.arctan2(vec_center[1], vec_center[0]) + np.pi/2
	theta_deg = utils.rad_to_deg(theta_rad)
	ts = ax.transData
	print(f'board_origin: {board_origin}')
	coords = ts.transform([board_origin[0][0], board_origin[1][0]])
	print(f'coords: {coords}')
	tr = mpl.transforms.Affine2D().rotate_deg_around(coords[0], coords[1], theta_deg)
	t= ts + tr

	# new_front_wheel_origin = utils.rotate(front_wheel_origin[0][0], front_wheel_origin[1][0], 0, 0, theta_rad)
	# new_back_wheel_origin = utils.rotate(back_wheel_origin[0][0], back_wheel_origin[1][0], 0, 0, theta_rad)
	# new_vec_front = utils.rotate(vec_front[0], vec_front[1], 0, 0, theta_rad)
	# new_vec_back = utils.rotate(vec_back[0], vec_back[1], 0, 0, theta_rad)

	# ax.quiver(*new_front_wheel_origin, new_vec_front[0], new_vec_front[1], color='y', angles='xy', scale_units='xy', scale=vec_scale)
	# ax.quiver(*new_back_wheel_origin, new_vec_back[0], new_vec_back[1], color='y', angles='xy', scale_units='xy', scale=vec_scale)

	new_force_plate = patches.Rectangle((-w_plate/2,-l_plate/2), w_plate, l_plate,transform=t,linewidth=1,edgecolor='y',facecolor='none')
	ax.add_patch(new_force_plate)

	fig.canvas.draw()
	plt.pause(0.0001)
	ax.clear()
	fig.canvas.flush_events()
	# plt.show()

	time.sleep(3)
