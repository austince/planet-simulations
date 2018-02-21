#!/usr/bin/env python

import os
import subprocess
from string import Template
from itertools import product
from termcolor import cprint

dir_path = os.path.dirname(os.path.realpath(__file__))

example_dir = os.path.join(dir_path, 'examples')
cli_path = os.path.join(dir_path, 'cli.py')

name_format = Template('${method}_dt=${dt}_end=${end_time}.csv')
cmd_args_format = Template('--method ${method} -dt ${dt} --end-time ${end_time} -o ${output} --save-plot')

if __name__ == "__main__":
    if not os.path.isdir(example_dir):
        os.mkdir(example_dir)

    cprint('Generating examples.', 'white')

    methods = ['euler', 'rk2', 'rk4']
    dts = [0.1, 0.5, 1, 2.5, 5]
    ends = [1825]

    combos = product(methods, dts, ends)

    for combo in combos:
        name = name_format.substitute(method=combo[0], dt=combo[1], end_time=combo[2])
        output = os.path.join(example_dir, name)
        args = cmd_args_format.substitute(method=combo[0], dt=combo[1], end_time=combo[2], output=output)
        subprocess.run(['python',  cli_path] + args.split(" "))

    cprint('Done. All examples in ' + os.path.dirname(example_dir), 'green')
