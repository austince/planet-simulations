import matplotlib.pyplot as plt
from simulations.conversions import cart_to_pol
import numpy as np


def plot_results(sim, title, output_file_name):
    data = np.loadtxt(open(output_file_name, 'rb'), delimiter=',', skiprows=1)
    x = data[:, sim.get_key_index('x')]
    y = data[:, sim.get_key_index('y')]

    # Convert to polar
    r, theta = cart_to_pol(x, y)

    # polar plot
    polar_plot = plt.figure('Polar Plot')
    polar_ax = plt.subplot(111, projection='polar')
    polar_ax.plot(theta, r)
    polar_ax.set_rmin(np.min(r))
    # polar_ax.set_rmin(0)
    polar_ax.set_rmax(np.max(r))
    polar_ax.grid(True)
    polar_ax.set_title(title)

    # cartesian plot
    cart_plot = plt.figure('Cart Plot')
    cart_ax = plt.subplot(111, polar=False)
    cart_ax.plot(x, y)
    cart_ax.set_title(title)
    cart_ax.set_xlabel('X position')
    cart_ax.set_ylabel('Y position')
    cart_ax.grid(True)
    cart_ax.axis([np.min(x), np.max(x), np.min(y), np.max(y)])
    return polar_plot, cart_plot