"""
The command line interface
"""
import argparse
from termcolor import cprint

from simulations.euler import EulerSimulation
from simulations.rk2 import RKSimulation
from simulations.conversions import au_to_m, day_to_sec, cart_to_pol

__version__ = '2.0.0'


class DaysToSecsAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


class AUToMAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        setattr(namespace, self.dest, values)


def main():
    """The exported main function
        :return: 
        """
    parser = argparse.ArgumentParser(description='Project 1 Simulation for PEP 336')
    parser.add_argument('-v', '--version', action='version', version=__version__)

    parser.add_argument('-dt',
                        help='Time delta. (days)',
                        type=float,
                        default=1,
                        action=DaysToSecsAction,
                        )

    parser.add_argument('-et', '--end-time',
                        help='End time for the simulation. (days)',
                        type=float,
                        default=1825,
                        action=DaysToSecsAction,
                        )

    parser.add_argument('-y0',
                        help='Initial y position. (AU)',
                        type=float,
                        default=0,
                        )

    parser.add_argument('-x0',
                        help='Initial x position. (AU)',
                        type=float,
                        default=1,
                        )

    parser.add_argument('-vy0',
                        help='Initial velocity in y direction. (km/s)',
                        type=float,
                        default=29.8,
                        )

    parser.add_argument('-vx0',
                        help='Initial velocity in x direction. (km/s)',
                        type=float,
                        default=0,
                        )

    parser.add_argument('-o', '--output',
                        help='CSV file to write results to.',
                        type=str,
                        required=True,
                        )

    parser.add_argument('-m', '--method',
                        help='Method for the simulation.',
                        choices=['euler', 'rk2', 'rk4'],
                        default='euler',
                        type=str
                        )

    parser.add_argument('-p', '--plot',
                        help='Plot the results?',
                        action='store_true',
                        default=False,
                        # type=bool
                        )

    # rk_args_group = parser.add_argument_group('RK Method')
    # rk_args_group.add_argument('-n', '-num-divisions',
    #                            help='Number of subdivisions.',
    #                            choices=[2, 4],
    #                            default=2,
    #                            type=int
    #                            )

    args = parser.parse_args()

    cprint('Starting simulation.', 'white')

    sim = None
    if args.method == 'euler':
        sim = EulerSimulation(
            au_to_m(args.x0),
            au_to_m(args.y0),
            args.vx0 * 1000,
            args.vy0 * 1000,
            day_to_sec(args.dt),
            day_to_sec(args.end_time),
        )
    elif args.method == 'rk2':
        sim = RKSimulation(
            au_to_m(args.x0),
            au_to_m(args.y0),
            args.vx0 * 1000,
            args.vy0 * 1000,
            day_to_sec(args.dt),
            day_to_sec(args.end_time),
            k=2,
        )
    elif args.method == 'rk4':
        sim = RKSimulation(
            au_to_m(args.x0),
            au_to_m(args.y0),
            args.vx0 * 1000,
            args.vy0 * 1000,
            day_to_sec(args.dt),
            day_to_sec(args.end_time),
            k=4,
        )

    sim.run(args.output)
    cprint('Simulation done.', 'green')

    if args.plot:
        # Could be made into it's own module / function
        cprint('Plotting results...', 'yellow')
        import matplotlib.pyplot as plt
        import numpy as np

        title = '%s for %.1f days. dt = %.2f days' % (args.method, args.end_time, args.dt)

        data = np.loadtxt(open(args.output, 'rb'), delimiter=',', skiprows=1)
        x = data[:, sim.get_key_index('x')]
        y = data[:, sim.get_key_index('y')]

        # Convert to polar
        r, theta = cart_to_pol(x, y)

        # polar plot
        polar_ax = plt.subplot(111, projection='polar')
        polar_ax.plot(theta, r)
        polar_ax.set_rmin(np.min(r))
        polar_ax.set_rmax(np.max(r))
        polar_ax.grid(True)
        polar_ax.set_title(title)

        # cartesian plot
        # cart_ax = plt.subplot(111)
        # cart_ax.plot(x, y)
        # cart_ax.set_title(title)
        # cart_ax.set_xlabel('X position')
        # cart_ax.set_ylabel('Y position')
        # cart_ax.grid(True)
        # cart_ax.axis([np.min(x), np.max(x), np.min(y), np.max(y)])

        plt.show()


if __name__ == '__main__':
    main()
