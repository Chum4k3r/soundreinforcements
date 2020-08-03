#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug  2 00:51:13 2020

@author: joaovitor
"""

import numpy as np


def spl_from_pressure(pressure: np.ndarray):
    return np.round(20*np.log10(pressure/2e-5), 1)


def pressure_from_spl(spl: np.ndarray):
    return 2e-5 * 10**(spl/20)


def swl_from_power(power: np.ndarray):
    return np.round(10*np.log10(power/1e-12), 1)


def power_from_swl(swl: np.ndarray):
    return 1e-12 * (10**(swl/10))


def sil_from_intensity(intensity: np.ndarray):
    return np.round(10*np.log10(intensity/1e-12), 1)


def intensity_from_sil(sil: np.ndarray):
    return 1e-12 * 10**(sil/10)


def spl_from_swl(swl: np.ndarray, directivity: int, distance: float):
    spl = swl - np.abs(10*np.log10(directivity/(4*np.pi*distance**2)))
    return np.round(spl, 1)


def intensity_from_power(power: np.ndarray, distance: float):
    return power/(4*np.pi*distance**2)


# def pressure_from_intensity(intensity: np.ndarray, directivity: int):
#     return

