import numpy as np

from .. import Simulation
from ..constants import G, MASS_SUN

"""
Simple motion and energy functions
"""
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


class EulerSimulation(Simulation):
    fieldnames = [
        'time',
        'x',
        'y',
        'radius',
        'v_x',
        'v_y',
        'a_x',
        'a_y',
        'total_energy'
    ]

    def __init__(self, x0, y0, vx0, vy0, dt, end_time):
        self.pos = np.array([x0, y0])
        self.velocity = np.array([vx0, vy0])
        self.dt = dt
        self.end_time = end_time

        self.time = 0
        self.radius = radius(self.pos)
        self.acceleration = acceleration(self.pos, self.radius)
        self.total_energy = total_energy(self.velocity, self.radius)

    def run(self, outfile):
        self.prepare_file(outfile)
        self.write_row(outfile)
        while self.time < self.end_time:
            self.time += self.dt

            self.radius = radius(self.pos)
            self.acceleration = acceleration(self.pos, self.radius)
            self.velocity = velocity(self.velocity, self.acceleration, self.dt)
            self.pos = position(self.pos, self.velocity, self.acceleration, self.dt)

            self.total_energy = total_energy(self.velocity, self.radius)
            self.write_row(outfile)

    def write_row(self, outfile):
        with open(outfile, 'a') as csvfile:
            writer = self.get_csv_writer(csvfile)
            writer.writerow({
                'time': self.time,
                'x': self.pos[0],
                'y': self.pos[1],
                'radius': self.radius,
                'v_x': self.velocity[0],
                'v_y': self.velocity[1],
                'a_x': self.acceleration[0],
                'a_y': self.acceleration[1],
                'total_energy': self.total_energy
            })
