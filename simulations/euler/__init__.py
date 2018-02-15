from csv import DictWriter
import numpy as np

from ..simple_motion import acceleration, velocity, position, radius, total_energy


class Simulation:
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
                'x': self.pos[0],
                'y': self.pos[1],
                'radius': self.radius,
                'v_x': self.velocity[0],
                'v_y': self.velocity[1],
                'a_x': self.acceleration[0],
                'a_y': self.acceleration[1],
                'total_energy': self.total_energy
            })
