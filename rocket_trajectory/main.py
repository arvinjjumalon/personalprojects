from Sims.tools import rk4
import pandas as pd
import numpy as np
import Sims.rocket_trajectory.src.eom as eom
import matplotlib.pyplot as plt

# Initial state vector: [u, v, w, p, q, r, phi, theta, psi, x, y, z]
y0 = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
mass = 0.9  # kg
i_matrix = np.identity(3)

t0 = 0  # start time in seconds
tf = 10  # end time in seconds
dt = 0.1  # time step in seconds

# Path to the thrust data CSV file
thrust_curve_file_path_1 = '.venv/Sims/rocket_trajectory/src/booster_info/Estes_F15.csv'

# Define the function to be used in the integrator
func_2body = lambda y, t: eom.eqofmotion(y, t, i_matrix, mass, thrust_curve_file_path_1)

# Perform the integration using the Runge-Kutta method
time_vec, y_solution = rk4.integration2(func_2body, y0, tf, t0, dt)

# Extract the altitude (z) from the solution
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
