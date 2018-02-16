import numpy as np
from csv import DictWriter

from .. import Simulation
from ..constants import MASS_SUN, G


def calc_k(pos, vel, dt, M=MASS_SUN):
    """
    Returns
    :param pos:
    :param vel:
    :param dt:
    :param M: gravitational mass
    :return:
    """

    def calc_k_vel(numer):
        ssq = np.sum(pos ** 2)
        return (-G * M) * numer * dt / (ssq * np.sqrt(ssq))

    k_pos = vel * dt
    # Do the same calculations for x and y position in velocity
    k_vel  = np.array([calc_k_vel(pos[0]), calc_k_vel(pos[1])])
    return k_pos, k_vel


class RKSimulation(Simulation):
    fieldnames = [
        'time',
        'x',
        'y',
        'v_x',
        'v_y',
    ]

    def __init__(self, x0, y0, vx0, vy0, dt, end_time, k=2):
        self.position = np.array([x0, y0])
        self.velocity = np.array([vx0, vy0])
        self.dt = dt
        self.end_time = end_time
        self.k = k
        self.time = 0

    def run(self, outfile):
        self.prepare_file(outfile)
        self.write_row(outfile)
        while self.time < self.end_time:
            self.time += self.dt

            k_vel_arr = np.ndarray(shape=(self.k, 2))  # x and y direction
            k_pos_arr = np.ndarray(shape=(self.k, 2))  # x and y direction
            k_pos, k_vel = self.position, self.velocity

            for i in range(self.k):
                k_pos_next, k_vel_next = calc_k(k_pos, k_vel, self.dt)
                k_pos_arr[i] = k_pos_next
                k_vel_arr[i] = k_vel_next

                k_pos += k_pos_next
                k_vel += k_vel_next

            # Update the variables to new values
            self.position += (1 / self.k) * (np.sum(k_pos_arr))  # Todo: calculate real 1/(c * k) function
            self.velocity += (1 / self.k) * (np.sum(k_vel_arr))

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
            })

