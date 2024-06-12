import numpy as np
import pandas as pd

# Rotation Matrices
def rot3(psi):  # z-axis rotation, psi must be in radians
    c, s = np.cos(psi), np.sin(psi)
    R = np.array([[c, -s, 0], [s, c, 0], [0, 0, 1]])
    return R

def rot2(theta):  # y-axis rotation, theta must be in radians
    c, s = np.cos(theta), np.sin(theta)
    R = np.array([[c, 0, s], [0, 1, 0], [-s, 0, c]])
    return R

def rot1(phi):  # x-axis rotation, phi must be in radians
    c, s = np.cos(phi), np.sin(phi)
    R = np.array([[1, 0, 0], [0, c, -s], [0, s, c]])
    return R

def euler_rate_matrix(phi, theta):
    cosp, sinp = np.cos(phi), np.sin(phi)
    tant, sect = np.tan(theta), 1/np.cos(theta)
    R = np.array([[1, sinp*tant, cosp*tant], [0, cosp, -sinp], [0, sinp*sect, cosp*sect]])
    return R

def load_thrust_data(file_path):
    thrust_data = pd.read_csv(file_path)
    return thrust_data

def linear_interpolate(thrust_data, time):
    times = thrust_data['time'].values
    thrusts = thrust_data['thrust'].values
    
    if time <= times[0]:
        return thrusts[0]
    if time >= times[-1]:
        return thrusts[-1]
    
    for i in range(len(times) - 1):
        if time >= times[i] and time <= times[i + 1]:
            t1, t2 = times[i], times[i + 1]
            f1, f2 = thrusts[i], thrusts[i + 1]
            return f1 + (f2 - f1) * (time - t1) / (t2 - t1)
    
    return 0  # Default case, should not happen if the data is correct

def eqofmotion(state_vec, time, i_matrix, mass, thrust_path):

    thrust_data = load_thrust_data(thrust_path)

    i_inverse = np.linalg.inv(i_matrix)
    grav_constant = -9.8  # m/s^2 (positive for calculations, direction handled in force vector)
    weight = grav_constant * mass

    # Variable Mapping
    u, v, w = state_vec[:3]
    p, q, r = state_vec[3:6]
    phi, theta, psi = state_vec[6:9]
    x, y, z = state_vec[9:12]

    vel_vector = np.array([u, v, w]).reshape(3, 1)
    ang_vel_vector = np.array([p, q, r]).reshape(3, 1)
    euler_vector = np.array([phi, theta, psi]).reshape(3, 1)
    pos_vector = np.array([x, y, z]).reshape(3, 1)

    # Forces:
    # Gravitational Forces in the Earth Frame
    grav_force_inertial = np.array([[0], [0], [weight]]).reshape(3, 1)

    # Transform gravitational force to the body frame
    grav_force_body = rot3(psi).dot(rot2(theta)).dot(rot1(phi)).dot(grav_force_inertial)

    # Aero Forces
    # Add Aero force calculations if available

    # Thrust Forces
    thrust_magnitude = linear_interpolate(thrust_data, time)
    thrust = np.array([[0], [0], [thrust_magnitude]])  # Assuming thrust is in the body frame along the z-axis

    force = thrust + grav_force_body

    vel_dot_vector = (force / mass) - np.cross(ang_vel_vector.flatten(), vel_vector.flatten()).reshape(3, 1)
    ang_vel_dot_vector = i_inverse.dot(-np.cross(ang_vel_vector.flatten(), (i_matrix.dot(ang_vel_vector).flatten())).reshape(3, 1))
    euler_dot_vector = euler_rate_matrix(phi, theta).dot(ang_vel_vector)
    pos_dot_vector = rot3(psi).dot(rot2(theta).dot(rot1(phi).dot(vel_vector)))

    return np.concatenate((vel_dot_vector, ang_vel_dot_vector, euler_dot_vector, pos_dot_vector), axis=0).flatten()

if __name__ == '__main__':
    y0 = [0,0,0,0,0,0,0,0,0,0,0,0]
    # state_vec = [u v w p q r phi theta psi x y z]
    mass = 9                        #kg
    grav_constant = -9.81            #m/s^2
    weight = mass * grav_constant   #N
    i_matrix = np.identity(3)
    t = 2

    thrust_curve_file_path_1 = '.venv/Sims/rocket_trajectory/src/booster_info/Estes_F15.csv'

    test = eqofmotion(y0,t,i_matrix,mass,thrust_curve_file_path_1)

    print(test)