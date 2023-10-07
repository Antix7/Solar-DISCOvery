import numpy as np
import datetime as dt
import math


def compute_dipole_tilt_angle(target_date):
    """
    Compute the dipole tilt angle for a target date.
    """

    vernal_equinox = dt.date(2015, 3, 20)  # Vernal equinox
    days_in_year = 365.25  # Average number of days in a year

    # Compute the tilt for the target date
    days_since_equinox_target = (target_date - vernal_equinox).days
    tilt = 23.5 * math.sin(2 * math.pi * days_since_equinox_target / days_in_year)

    return tilt


def gse_to_gsm(vector_gse, date):

    """
    - vector_gse (tuple or list): Vector in GSE coordinates (Bx, By, Bz)
    - date (date)
    """
    dipole_tilt_angle = compute_dipole_tilt_angle(date)

    rotation_matrix = np.array([
        [1, 0, 0],
        [0, np.cos(dipole_tilt_angle), -np.sin(dipole_tilt_angle)],
        [0, np.sin(dipole_tilt_angle), np.cos(dipole_tilt_angle)]
    ])

    return tuple(np.matmul(rotation_matrix, vector_gse))

