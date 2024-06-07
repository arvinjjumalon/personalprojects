import numpy as np

def sattelite_orbit(state_vec, time, planet_mass, sattelite_mass):
    Grav = 6.67259e-20
    mu = Grav*(planet_mass + sattelite_mass)

    state_vec = np.array(state_vec)

    rx, ry, rz = state_vec[:3]
    vx, vy, vz = state_vec[3:]

    r_norm = (rx**2 + ry**2 + rz**2)**0.5
    r_vec = [rx, ry, rz]

    ax, ay, az = [-1 * n * mu / r_norm**3 for n in r_vec]

    return [vx, vy, vz, ax, ay, az]

if __name__ == "__main__":
    print(sattelite_orbit([8000, 0, 6000, 0, 5, 5],0,5.974*10**24,1000))