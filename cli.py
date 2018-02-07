"""
The command line interface
"""
import argparse
import os
import sys
from termcolor import cprint

from euler import Simulation

__version__ = '1.0.0'


def main():
    """The exported main function
        :return: 
        """
    parser = argparse.ArgumentParser(description='Project 1 Simulation for PEP 336')
    parser.add_argument('-v', '--version', action='version', version=__version__)

    parser.add_argument('-b', '--bandwidth', help='Bandwidth for the mean shift clustering.', type=int)

    # Optional to provide input images instead of default set
    parser.add_argument('-o', '--output',
                        help='CSV file to write results to.',
                        type=str,
                        required=True,
                        )

    cprint('Starting simulation', 'white')
    sim = Simulation()
    sim.run()
    cprint('Simulation done.', 'green')


if __name__ == '__main__':
    main()
