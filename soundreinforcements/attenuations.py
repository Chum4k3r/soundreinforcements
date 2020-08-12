# -*- codging: utf-8 -*-
"""
Attenuations
============

This is a brief explanation of all the sound attenuation effects that the ISO 9613-2: 1996 proposes
as part of the outdoor sound propagation modelling.


Parameters:
    - r: distance between source and receiver in m
    - a: atmosphere absorption in dB/m
    - h: height
    - d: distance between source and receiver projected on the ground plane in m


Divergence attenuation (Adiv):
    Depends only on the distance

    Adiv = 20 * log10(r) + 11


Atmosphere attenuation (Aatm):
    Depends on distance and atmospherical conditions such as temperature, air relative humidity
    and atmospherical pressure

    Aatm = a * r


Ground effect (Agr):
    Depends on the height of, and the ground type surrounding, the source (s) and receiver (r).
    If the surrounding areas of source and receiver do not intersect, there is a consideration
    about the ground between them as mean (m) ground.

    The ground factor G is as follows:

    G = 0 for hard ground

    G = 1 for porous ground

    0 < G < 1 for mixed ground

    May be expressed as a ratio of hard to porous ground.

    These equations can be used only if the ground is flat between source and receiver, or the distance between
    them is short. Each term have specific equations that describe the attenuation.

    dp = 1 - exp(-d / 50)

    c125 = 1.5 + 3 * exp(-0.12 * (h - 5)**2) * dp + 5.7 * exp(-0.09 * h**2) * (1 - exp(-2.8e-6 * d**2))

    c250 = 1.5 + 8.6 * exp(-0.09 * h**2) * dp)

    c500 = 1.5 + 14 * exp(-0.46 * h**2) * dp)

    c1000 = 1.5 + 5 * exp(-0.9 * h**2) * dp)

    For h can be hs for the source and hr for the receiver, G can be Gs and Gr, respectively

    As and Ar can be calculated, for each frequency band, as follows:

    63      -1.5
    125     -1.5 + G * c125
    250     -1.5 + G * c250
    500     -1.5 + G * c500
    1000    -1.5 + G * c1000
    2000    -1.5 * (1 - G)
    4000    -1.5 * (1 - G)
    8000    -1.5 * (1 - G)

    The mean ground attenuation depends on the factor q which is 0 if d <= 30 * (hr + hs), else:

    q = 1 - 30 * (hr + hs) / d

    Then, the Am attenuation:

    63              -3 * q
    125 to 8000     -3 * q * (1 - Gm)

    with Gm being the ground factor of the mean ground

    Finally,

    Agr = As + Ar + Am


Barriers:




"""


import numpy as np
from .space import projected_distance_from_plane


def divergence(r: float):
    return 20. * np.log10(r) + 11.


def atmosphere(a: np.ndarray, r: float):
    return a * r


def ground(srcpos, srcG, recpos, recG, meanG):
    def dp(d: float):
        return 1. - np.exp(-d / 50.)

    def c125(h, d):
        return 1.5 + 3 * np.exp(-0.12 * (h - 5)**2) * dp(d) + 5.7 * np.exp(-0.09 * h**2) * (1 - np.exp(-2.8e-6 * d**2))

    def c250(h, d):
        return 1.5 + 8.6 * np.exp(-0.09 * h**2) * dp(d)

    def c500(h, d):
        return 1.5 + 14 * np.exp(-0.46 * h**2) * dp(d)

    def c1000(h, d):
        return 1.5 + 5 * np.exp(-0.9 * h**2) * dp(d)

    def q(hr, hs, d):
        m = 30. * (hr + hs)
        return 1. - m / d if d > m else 0.

    projDist = projected_distance_from_plane('xy', srcpos, recpos)
    recHeight = recpos.z
    srcHeight = srcpos.z

    Ar = np.array([-1.5, -1.5 + recG*c125(recHeight, projDist), -1.5 + recG*c250(recHeight, projDist),
        -1.5 + recG*c500(recHeight, projDist), -1.5 + recG*c1000(recHeight, projDist), -1.5*(1-recG),
        -1.5*(1-recG), -1.5*(1-recG)])

    As = np.array([-1.5, -1.5 + srcG*c125(srcHeight, projDist), -1.5 + srcG*c250(srcHeight, projDist),
        -1.5 + srcG*c500(srcHeight, projDist), -1.5 + srcG*c1000(srcHeight, projDist), -1.5*(1-srcG),
        -1.5*(1-srcG), -1.5*(1-srcG)])

    Am = -3 * q(recHeight, srcHeight, projDist) * np.array([1] + 7 * [1 - meanG])

    return Ar + As + Am



