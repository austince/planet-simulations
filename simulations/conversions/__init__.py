KM_PER_AU = 1.496 * (10 ** 8)


def au_to_m(au):
    return au_to_km(au) * 1000


def au_to_km(au):
    return au * KM_PER_AU


def km_to_au(km):
    return km / KM_PER_AU


def day_to_sec(day):
    return day * 86400
