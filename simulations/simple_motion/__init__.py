import numpy as np

from ..constants import G, MASS_SUN

def acceleration(pos_i, r_i):
    return pos_i * (-G * MASS_SUN / (r_i ** 3))


def velocity(v_i, a_i, dt):
    return v_i + (a_i * dt)


def position(pos_i, v_i, a_i, dt):
    return pos_i + (v_i * dt) + (0.5 * a_i * (dt ** 2))


def radius(pos_i):
    return np.sqrt(np.sum(np.square(pos_i)))


def total_energy(v_i, r_i):
    return 0.5 * (np.sqrt(v_i.dot(v_i)) ** 2) - (G * MASS_SUN / r_i)