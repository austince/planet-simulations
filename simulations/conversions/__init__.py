import numpy as np

KM_PER_AU = 1.496 * (10 ** 8)


def au_to_m(au):
    return au_to_km(au) * 1000


def au_to_km(au):
    return au * KM_PER_AU


def km_to_au(km):
    return km / KM_PER_AU


def day_to_sec(day):
    return day * 86400


# From: https://stackoverflow.com/questions/20924085/python-conversion-between-coordinates
def cart_to_pol(x, y):
    rho = np.sqrt(x ** 2 + y ** 2)
    phi = np.arctan2(y, x)
    return rho, phi


def pol_to_cart(rho, phi):
    x = rho * np.cos(phi)
    y = rho * np.sin(phi)
    return x, y
