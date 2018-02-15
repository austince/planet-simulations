import numpy as np

from ..constants import MASS_SUN, G


def calc_k(pos, vel, dt, M=MASS_SUN):
    """
    Returns
    :param vel:
    :param dt:
    :return:
    """

    def calc_k_vel(numer):
        ssq = np.sum(pos ** 2)
        return (-G * M) * numer * dt / (ssq * np.sqrt(ssq))

    k_pos = vel * dt
    # Do the same calculations for x and y position in velocity
    k_vel  = np.array([calc_k_vel(pos[0]), calc_k_vel(pos[1])])
    return k_pos, k_vel


class KSimulation:
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

            ks = np.ndarray(shape=(self.k,), dtype=object)
            k_pos, k_vel = self.position, self.velocity
            for i in range(self.k):
                k_pos, k_vel = calc_k(k_pos, k_vel, self.dt)
                ks[i] = k_pos, k_vel

            # Update the variables to new values

            self.write_row(outfile)


    @staticmethod
    def get_csv_writer(csvfile):
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
        return DictWriter(csvfile, fieldnames=fieldnames)

    def prepare_file(self, outfile):
        with open(outfile, 'w') as csvfile:
            writer = self.get_csv_writer(csvfile)
            writer.writeheader()

    def write_row(self, outfile):
        with open(outfile, 'a') as csvfile:
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