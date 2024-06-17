# Written by ArvinJay Jumalon

import numpy as np

def twobody_ode2(state_vec, time, m_1, m_2):
    G = 6.67259e-20
    
    state_vec = np.array(state_vec) #Just to make sure

    rx1, ry1, rz1, rx2, ry2, rz2 = state_vec[:6]
    vx1, vy1, vz1, vx2, vy2, vz2 = state_vec[6:]

    r_norm = ((rx1-rx2)**2+(ry1-ry2)**2+(rz1-rz2)**2)**0.5
    r_vec1 = [rx2-rx1, ry2-ry1, rz2-rz1]
    r_vec2 = [-n for n in r_vec1]

    ax1, ay1, az1 = [n * m_2 * G / r_norm**3 for n in r_vec1]
    ax2, ay2, az2 = [n * m_1 * G / r_norm**3 for n in r_vec2]

    return [vx1, vy1, vz1, vx2, vy2, vz2, ax1, ay1, az1, ax2, ay2, az2]