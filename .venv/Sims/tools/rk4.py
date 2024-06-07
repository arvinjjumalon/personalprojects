import numpy as np

def singlestep(func, h, t0, y0):
    k1 = np.array(func(y0, t0)) #Turn k's into an array to make dealing with everything else easier
    k2 = np.array(func(y0 + k1 * (h/2), t0 + h/2))
    k3 = np.array(func(y0 + k2 * (h/2), t0 + h/2))
    k4 = np.array(func(y0 + k3 * h, t0 + h))
    y_next = y0 + h * (k1 + 2*k2 + 2*k3 + k4) / 6
    return y_next

def integration2(func, y0, final_time, initial_time, dt):
    time_pts = int((final_time - initial_time) / dt) + 1
    time_vec = np.linspace(initial_time, final_time, time_pts)

    y_solve = np.zeros((len(y0), time_pts))
    y_solve[:, 0] = y0
    for i in range(time_pts - 1):
        y_out = singlestep(func, dt, time_vec[i], y_solve[:, i])
        y_solve[:, i + 1] = y_out
    
    return time_vec, y_solve

