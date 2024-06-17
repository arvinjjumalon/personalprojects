# Written by ArvinJay Jumalon

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import matplotlib.pyplot as plt
import numpy as np
import matplotlib.animation as anim
import tools.rk4 as rk4
import tools.celestial_bodies as cb
import earth_sattelite_orbit.src.eom as eom

y0 = [8000, 0, 6000, 0, 5, 5] #Sattelite rx, ry, rz, vx, vy, vz

earth_mass = cb.earth.mass
earth_radius = cb.earth.radius
sattelite_mass = 1000 #kg
t0 = 0
tf = 4*60*60
dt = 0.5

func = lambda y,t: eom.sattelite_orbit(y,t,earth_mass,sattelite_mass)
time_vec, y_solution = rk4.integration2(func, y0, tf, t0, dt)

sx, sy, sz = y_solution[0,:], y_solution[1,:], y_solution[2,:]

fig = plt.figure()
inertialframe = fig.add_subplot(111, projection='3d')

inertialframe.plot(sx, sy, sz, label='Body 1', color="r")

# Plotting Earth
u, v = np.mgrid[0:2*np.pi:20j, 0:np.pi:10j]
x = earth_radius*np.cos(u)*np.sin(v)
y = earth_radius*np.sin(u)*np.sin(v)
z = earth_radius*np.cos(v)
inertialframe.plot_surface(x, y, z, color="b", alpha=0.6)

inertialframe.set_xlabel('X')
inertialframe.set_ylabel('Y')
inertialframe.set_zlabel('Z')
inertialframe.legend()
inertialframe.set_aspect('equal')

# Animation Portion: Body Frame Relative to Body 1
point, = inertialframe.plot([sx[0]], [sy[0]], [sz[0]], 'bo')
time_text2 = inertialframe.text2D(0.05, 0.95, '', transform=inertialframe.transAxes)

# Update function for the animation
def update_bodyframe(frame):
    point.set_data([sx[frame]], [sy[frame]])
    point.set_3d_properties([sz[frame]])
    # Update time text
    time_text2.set_text('Time Elapsed: {:.1f} seconds'.format(time_vec[frame]))

    return point, time_text2

# Create the animation
ani_bodyframe = anim.FuncAnimation(fig, update_bodyframe, frames=len(time_vec), interval=20, blit=True, repeat=False)

plt.show()