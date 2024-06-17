import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import rk4
import src.eom as eom
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as anim


# Example 2.2
y0 = [-9000, 2000, 4000, -8000, 2000, 6000, 20, -29, 0, 70, 0, -5]

Grav = 6.67259e-20
m1 = 1.e26
m2 = 1.e26
t0 = 0
tf = 480
dt = 0.5

func_2body = lambda y,t: eom.twobody_ode2(y,t,m1,m2)
time_vec, y_solution = rk4.integration2(func_2body, y0, tf, t0, dt)

body1_x, body1_y, body1_z = y_solution[0, :], y_solution[1, :], y_solution[2, :]
body2_x, body2_y, body2_z = y_solution[3, :], y_solution[4, :], y_solution[5, :]

body2_x_rel, body2_y_rel, body2_z_rel = body2_x - body1_x, body2_y - body1_y, body2_z - body1_z

# Might need to put all of this into src or tools or smth
# Plotting Portion: Inertial Frame
fig1 = plt.figure(1)
inertialframe = fig1.add_subplot(111, projection='3d')

inertialframe.plot(body1_x, body1_y, body1_z, label='Body 1')
inertialframe.plot(body2_x, body2_y, body2_z, label='Body 2')

inertialframe.set_xlabel('X')
inertialframe.set_ylabel('Y')
inertialframe.set_zlabel('Z')
inertialframe.legend()
inertialframe.set_aspect('equal')

# Animation portion: inertial frame
point_if_body1, = inertialframe.plot([body1_x[0]], [body1_y[0]], [body1_z[0]], 'bo')
point_if_body2, = inertialframe.plot([body2_x[0]], [body2_y[0]], [body2_z[0]], 'ro')
time_text1 = inertialframe.text2D(0.05, 0.95, '', transform=inertialframe.transAxes)

def update_inertialframe(frame):
    point_if_body1.set_data([body1_x[frame]], [body1_y[frame]])
    point_if_body1.set_3d_properties([body1_z[frame]])

    point_if_body2.set_data([body2_x[frame]], [body2_y[frame]])
    point_if_body2.set_3d_properties([body2_z[frame]])
    # Update time text
    time_text1.set_text('Time Elapsed: {:.1f} seconds'.format(time_vec[frame]))

    return point_if_body1, point_if_body2, time_text1

ani_inertialframe = anim.FuncAnimation(fig1, update_inertialframe, frames=len(time_vec), interval=20, blit=True, repeat=False)

# Plotting Portion: Body Frame relative to Body 1
fig2 = plt.figure(2)
bodyframe_body1 = fig2.add_subplot(111, projection='3d')

bodyframe_body1.plot(0, 0, 'ro', label='Body 1')
bodyframe_body1.plot(body2_x_rel, body2_y_rel, body2_z_rel, label='Body 2')

bodyframe_body1.set_xlabel('X')
bodyframe_body1.set_ylabel('Y')
bodyframe_body1.set_zlabel('Z')
bodyframe_body1.legend()
bodyframe_body1.set_aspect('equal')

# Animation Portion: Body Frame Relative to Body 1
point_bf_body2, = bodyframe_body1.plot([body2_x_rel[0]], [body2_y_rel[0]], [body2_z_rel[0]], 'bo')
time_text2 = bodyframe_body1.text2D(0.05, 0.95, '', transform=bodyframe_body1.transAxes)

# Update function for the animation
def update_bodyframe(frame2):
    point_bf_body2.set_data([body2_x_rel[frame2]], [body2_y_rel[frame2]])
    point_bf_body2.set_3d_properties([body2_z_rel[frame2]])
    # Update time text
    time_text2.set_text('Time Elapsed: {:.1f} seconds'.format(time_vec[frame2]))

    return point_bf_body2, time_text2

# Create the animation
ani_bodyframe = anim.FuncAnimation(fig2, update_bodyframe, frames=len(time_vec), interval=20, blit=True, repeat=False)

# Display the plots
plt.show()
