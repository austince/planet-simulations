# Earth Orbit Simulations for PEP 336

## Requirements
**Only runs with Python 3**  

3rd party packages can be install either with [Anaconda](https://www.anaconda.com/) 
by `conda env create -f env.yml` or with [pip](https://packaging.python.org/tutorials/installing-packages/)
by `pip install -r requirements.txt`.

## Running

The `cli.py` script runs the simulations and writes the 
data to a csv file. All the running options are explained
by running `python cli.py --help` but here are a few good ones
to remember:
- `--plot` will plot the results in a polar projection.
- `--output <filename>` will save the results to `filename`. (Required!)
- `--method {euler,rk2,rk4}` will run one of those three simulations.
- `-dt <days>` will set the time delta to `days`.

Here's a full example that runs a *RK4* simulation for *5 years* with a 
time delta of *0.5 days* and plots it. 

`python cli.py -dt 0.5 --end-time 1825 --method rk4 --output rk4_dt=0.5_end=1825.csv --plot`