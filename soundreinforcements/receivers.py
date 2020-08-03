#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Receivers
=========

This module provide abstraction for sound receivers, such as microphones.


Created on Thu Jul 30 23:50:01 2020

@author: joaovitor
"""


import numpy as _np
from typing import List
from .space import Object3D, distance
from .sources import Source
from .air import Air
from .levelmaths import spl_from_swl, pressure_from_spl, power_from_swl, \
                        intensity_from_power, sil_from_intensity


class Receiver(Object3D):
    """Receiver abstraction."""

    def __init__(self, pos: List[float], ori: List[float], air: Air):
        Object3D.__init__(self, pos, ori)
        self.air = air
        return

    def distance_from_source(self, source: Source):
        return distance(self.position, source.position)

    def spl_from_source(self, source: Source):
        dist = self.distance_from_source(source)
        spl = spl_from_swl(source.swl, source.directivity, dist)
        spl -= self.air.absorption('dB/m') * dist
        return spl

    def pressure_from_source(self, source):
        spl = self.spl_from_source(source)
        return pressure_from_spl(spl)

    def intensity_from_source(self, source: Source):
        dist = self.distance_from_source(source)
        power = power_from_swl(source.swl)
        intensity = intensity_from_power(power, dist)
        intensity *= _np.exp(-self.air.absorption('1/m')*dist)
        return intensity

    def sil_from_source(self, source: Source):
        intensity = self.intensity_from_source(source)
        return sil_from_intensity(intensity)


