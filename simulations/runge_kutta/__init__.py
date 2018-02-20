import numpy as np

from .. import Simulation
from ..constants import MASS_SUN, G
from ..utils import radius, total_energy


def calc_k(pos, vel, dt, M=MASS_SUN):
    """
    Returns
    :param pos:
    :param vel:
    :param dt:
    :param M: gravitational mass
    :return:
    """

    ssq = np.sum(pos ** 2)
    sqrt_ssq = np.sqrt(ssq)

    k_pos = vel * dt
    k_vel = pos * (-G * M * dt) / (ssq * sqrt_ssq)
    return k_pos, k_vel


class RKSimulation(Simulation):
    fieldnames = [
        'time',
        'x',
        'y',
        'v_x',
        'v_y',
        'total_energy',
    ]

    def __init__(self, x0, y0, vx0, vy0, dt, end_time, order=2):
        self.position = np.array([x0, y0])
        self.velocity = np.array([vx0, vy0])
        self.dt = dt
        self.end_time = end_time
        self.order = order
        self.time = 0
        self.total_energy = total_energy(self.velocity, self.position)

        # Hardcode order weights for now
        # will do n-th order sometime maybe
        if order == 2:
            self.sum_weights = np.array([1, 1])[:, np.newaxis]
            self.sum_coeff = 1 / 2
        elif order == 4:
            self.sum_weights = np.array([1, 2, 2, 1])[:, np.newaxis]
            self.sum_coeff = 1 / 6

    def run(self, outfile):
        self.prepare_file(outfile)
        self.write_row(outfile)
        while self.time < self.end_time:
            self.time += self.dt

            k_vel_arr = np.ndarray(shape=(self.order, 2))  # x and y direction
            k_pos_arr = np.ndarray(shape=(self.order, 2))  # x and y direction
            k_pos, k_vel = self.position, self.velocity

            for i in range(self.order):
                k_pos_next, k_vel_next = calc_k(k_pos, k_vel, self.dt)
                k_pos_arr[i] = k_pos_next
                k_vel_arr[i] = k_vel_next

                k_pos += (k_pos_next / self.sum_weights[i])
                k_vel += (k_vel_next / self.sum_weights[i])

            # Update the variables to new values
            self.position += self.sum_coeff * ((k_pos_arr * self.sum_weights).sum(axis=0))
            self.velocity += self.sum_coeff * ((k_vel_arr * self.sum_weights).sum(axis=0))

            # For sanity checks
            self.total_energy = total_energy(self.velocity, self.position)

            # Record the iteration
            self.write_row(outfile)

    def write_row(self, outfile):
        with open(outfile, 'a') as csvfile:
            writer = self.get_csv_writer(csvfile)
            writer.writerow({
                'time': self.time,
                'x': self.position[0],
                'y': self.position[1],
                'v_x': self.velocity[0],
                'v_y': self.velocity[1],
                'total_energy': self.total_energy,
            })
