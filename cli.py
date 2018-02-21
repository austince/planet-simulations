"""
The command line interface
"""
import argparse
from termcolor import cprint

from simulations.euler import EulerSimulation
from simulations.runge_kutta import RKSimulation
from simulations.conversions import au_to_m, day_to_sec
from simulations.plotting import plot_results

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

    plot_group = parser.add_argument_group('Plotting')
    plot_group.add_argument('-p', '--plot',
                            help='Plot the results?',
                            action='store_true',
                            default=False,
                            )

    plot_group.add_argument('-sp', '--save_plot',
                            help='Save the plotted results?',
                            action='store_true',
                            default=False,
                            )

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
            order=2,
        )
    elif args.method == 'rk4':
        sim = RKSimulation(
            au_to_m(args.x0),
            au_to_m(args.y0),
            args.vx0 * 1000,
            args.vy0 * 1000,
            day_to_sec(args.dt),
            day_to_sec(args.end_time),
            order=4,
        )

    sim.run(args.output)
    cprint('Simulation done.', 'green')

    if args.plot or args.save_plot:
        cprint('Plotting results...', 'yellow')
        title = '%s for %.1f days. dt = %.2f days' % (args.method, args.end_time, args.dt)
        poly, cart = plot_results(sim, title, args.output)
        # poly.show()
        # cart.show()
        if args.plot:
            import matplotlib.pyplot as plt
            plt.show()
        if args.save_plot:
            cprint('Saving plots...', 'yellow')
            poly.savefig(args.output + 'polyplot.png')
            cart.savefig(args.output + 'cartplot.png')


if __name__ == '__main__':
    main()
