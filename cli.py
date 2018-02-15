"""
The command line interface
"""
import argparse
from termcolor import cprint

from simulations.euler import Simulation
from simulations.conversions import au_to_km, day_to_sec

__version__ = '1.0.0'


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
                        )

    parser.add_argument('-et', '--end-time',
                        help='End time for the simulation. (days)',
                        type=float,
                        default=1825,
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
                        choices=['euler', 'e', 'rk2', 'rk4'],
                        default='euler',
                        type=str
                        )

    args = parser.parse_args()

    cprint('Starting simulation.', 'white')
    sim = Simulation(
        au_to_km(args.x0) * 1000,
        au_to_km(args.y0) * 1000,
        args.vx0 * 1000,
        args.vy0 * 1000,
        day_to_sec(args.dt),
        day_to_sec(args.end_time),
    )
    sim.run(args.output)
    cprint('Simulation done.', 'green')


if __name__ == '__main__':
    main()
