#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 00:51:13 2020

@author: joaovitor
"""

import numpy as np
from functools import wraps


def dB_round(func: callable):
    @wraps(func)
    def dB_round_wrapper(*args, **kwargs):
        dBvalue = func(*args, **kwargs)
        return np.round(dBvalue, 1)
    return dB_round_wrapper


@dB_round
def spl_from_pressure(pressure: np.ndarray):
    """Sound pressure level from effective sound pressure given in Pa."""
    return 20*np.log10(pressure/2e-5)


def pressure_from_spl(spl: np.ndarray):
    """Effective sound pressure, in Pa, from given sound pressure level."""
    return 2e-5 * 10**(spl/20)


@dB_round
def swl_from_power(power: np.ndarray):
    """Sound power level from sound power given in W."""
    return 10*np.log10(power/1e-12)


def power_from_swl(swl: np.ndarray):
    """Sound power, in W, from given sound power level."""
    return 1e-12 * (10**(swl/10))


def power_from_wave(wave: np.ndarray):
    return np.mean(wave**2)


@dB_round
def sil_from_intensity(intensity: np.ndarray):
    """Sound intensity level from sound intensity given in W/m²."""
    return 10*np.log10(intensity/1e-12)


def intensity_from_sil(sil: np.ndarray):
    """Sound intensity, in W/m², from given sound intensity level."""
    return 1e-12 * 10**(sil/10)


@dB_round
def spl_from_swl(swl: np.ndarray, Q: int, distance: float):
    """
    Sound pressure level at `distance` m away from sound source
    with `swl` sound power level and `Q` directivity factor.
    """
    diff = np.abs(10*np.log10(Q/(4*np.pi*distance**2)))
    return swl - diff


def intensity_from_power(power: np.ndarray, distance: float):
    """Sound intensity at `distance` m away from sound source with `power` sound power."""
    return power/(4*np.pi*distance**2)

