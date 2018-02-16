import numpy as np

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

    ssq = np.sum(pos ** 2)
    sqrt_ssq = np.sqrt(ssq)

    def calc_k_vel(numer):
        """
        Todo: make into lambda function and use np to apply to each
        :param numer:
        :return:
        """
        return (-G * M * numer * dt) / (ssq * sqrt_ssq)

    k_pos = vel * dt
    # Do the same calculations for x and y position in velocity
    k_vel = np.array([calc_k_vel(pos[0]), calc_k_vel(pos[1])])
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
        # Hardcode order weights for now
        # will do n-th order sometime maybe
        if k == 2:
            self.sum_weights = [1, 1]
            self.sum_coeff = 1 / 2
        elif k == 4:
            self.sum_weights = [1, 2, 2, 1]
            self.sum_coeff = 1 / 6

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

                k_pos += (k_pos_next / self.sum_weights[i])
                k_vel += (k_vel_next / self.sum_weights[i])

            # Update the variables to new values
            self.position += self.sum_coeff * ((k_pos_arr * self.sum_weights).sum(axis=0))
            self.velocity += self.sum_coeff * ((k_vel_arr * self.sum_weights).sum(axis=0))

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
