import numpy as np

from .constants import MASS_SUN, G


def radius(position):
    return np.sqrt(np.sum(np.square(position)))


def total_energy(velocity, position, M=MASS_SUN):
    return 0.5 * (np.sqrt(velocity.dot(velocity)) ** 2) - (G * M / radius(position))

