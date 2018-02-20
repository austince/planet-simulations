import numpy as np

from .. import Simulation
from ..constants import G, MASS_SUN
from ..utils import radius, total_energy

"""
Simple motion and energy functions
"""


def acceleration(pos_i, r_i):
    return pos_i * (-G * MASS_SUN / (r_i ** 3))


def velocity(v_i, a_i, dt):
    return v_i + (a_i * dt)


def position(pos_i, v_i, a_i, dt):
    return pos_i + (v_i * dt) + (0.5 * a_i * (dt ** 2))


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
        self.position = np.array([x0, y0])
        self.velocity = np.array([vx0, vy0])
        self.dt = dt
        self.end_time = end_time

        self.time = 0
        self.radius = radius(self.position)
        self.acceleration = acceleration(self.position, self.radius)
        self.total_energy = total_energy(self.velocity, self.position)

    def run(self, outfile_path):
        self.prepare_file(outfile_path)
        self.write_row(outfile_path)
        while self.time < self.end_time:
            self.time += self.dt

            self.position = position(self.position, self.velocity, self.acceleration, self.dt)
            self.radius = radius(self.position)
            self.velocity = velocity(self.velocity, self.acceleration, self.dt)

            self.acceleration = acceleration(self.position, self.radius)

            self.total_energy = total_energy(self.velocity, self.radius)
            self.write_row(outfile_path)

    def write_row(self, outfile_path):
        with open(outfile_path, 'a') as csvfile:
            writer = self.get_csv_writer(csvfile)
            writer.writerow({
                'time': self.time,
                'x': self.position[0],
                'y': self.position[1],
                'radius': self.radius,
                'v_x': self.velocity[0],
                'v_y': self.velocity[1],
                'a_x': self.acceleration[0],
                'a_y': self.acceleration[1],
                'total_energy': self.total_energy
            })
