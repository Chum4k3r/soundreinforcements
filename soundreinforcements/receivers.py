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
from .space import Object3D, distance, distance_over_plane
from .sources import Source
from .air import Air
from .level import spl_from_swl, pressure_from_spl, spl_from_pressure, pressure_from_power
                   #, power_from_swl, intensity_from_power, sil_from_intensity


class Receiver(Object3D):
    """Receiver abstraction."""

    def __init__(self, pos: List[float], ori: List[float]):
        Object3D.__init__(self, pos, ori)
        return

    def distance_from_source(self, source: Source):
        """3D distance from source to receiver."""
        return distance(self.position, source.position)

    def ground_distance_from_source(self, source: Source):
        """Distance from source to receiver projected to the ground plane."""
        return distance_over_plane('xy', self.position, source.position)

    def spl_from_source(self, source: Source, air: Air):
        dist = self.distance_from_source(source)
        distgr = self.ground_distance_from_source(source)
        spl = spl_from_swl(source.swl, dist, distgr,
                           source.position.z, 0.6,
                           self.position.z, 0.8,
                           0.5,
                           air.absorption('dB/m'))
        return spl

    def pressure_from_source(self, source, air: Air):
        k = 2 * _np.pi * air.frequencies / air.soundSpeed
        dist = distance(self.position, source.position)
        p = pressure_from_power(source.power, dist, air.impedance)
        return p * _np.exp(-1j * k * dist)

    # def intensity_from_source(self, source: Source, air: Air):
    #     dist = self.distance_from_source(source)
    #     power = power_from_swl(source.swl)
    #     intensity = intensity_from_power(power, dist)
    #     intensity *= _np.exp(-air.absorption('1/m')*dist)
    #     return intensity

    # def sil_from_source(self, source: Source, air: Air):
    #     intensity = self.intensity_from_source(source, air)
    #     return sil_from_intensity(intensity)


class ReceiversGrid(object):
    """Space distributed receivers grid."""

    def __init__(self, minx, maxx, dx, miny, maxy, dy, z, air):
        self.rect = _np.array([minx, miny, maxx, maxy], dtype='float16')
        self.xs = _np.arange(minx, maxx, dx, dtype='float16')
        self.ys = _np.arange(miny, maxy, dy, dtype='float16')
        self.z = z
        self.air = air
        self.generate_grid()
        return

    def generate_grid(self):
        self.recsgrids = []
        for y in self.ys:
            rs = []
            for x in self.xs:
                rs.append(Receiver([x, y, self.z], [x, y, self.z]))
            self.recsgrids.append(rs)
        return

    def eval_spl(self, src: Source):
        spls = [[rec.spl_from_source(src, self.air)
                 for rec in recgrid]
                for recgrid in self.recsgrids]
        return _np.array(spls)

    def eval_pressure(self, src: Source):
        pressures = [[rec.pressure_from_source(src, self.air)
                      for rec in recgrid]
                     for recgrid in self.recsgrids]
        return _np.array(pressures)


