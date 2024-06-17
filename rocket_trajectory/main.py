# Written by ArvinJay Jumalon

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from tools import rk4
import pandas as pd
import numpy as np
import rocket_trajectory.src.eom as eom
import matplotlib.pyplot as plt

# Initial state vector: [u, v, w, p, q, r, phi, theta, psi, x, y, z]
y0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
mass = 0.9  # kg
i_matrix = np.identity(3)

t0 = 0      #seconds
tf = 10
dt = 0.1

# Path to the thrust data CSV file
thrust_curve_file_path_1 = '.venv/Sims/rocket_trajectory/src/booster_info/Estes_F15.csv'

func_2body = lambda y, t: eom.eqofmotion(y, t, i_matrix, mass, thrust_curve_file_path_1)
time_vec, y_solution = rk4.integration2(func_2body, y0, tf, t0, dt)

z = y_solution[11, :]
vz = y_solution[2,:]

# Plot the results
fig1 = plt.figure(1)
inertialframe = fig1.add_subplot(111)

inertialframe.plot(time_vec, z, label='Altitude')
inertialframe.plot(time_vec, vz, label='Altitude')

inertialframe.set_xlabel('time (s)')
inertialframe.set_ylabel('altitude (m), acceleration(m/s^2)')
inertialframe.legend()
plt.show()

# To do:
# Make it a two stage thing cause its supposed to be a lander, damn!
# Somehoe add in pertubations based on altitude (csv files!)