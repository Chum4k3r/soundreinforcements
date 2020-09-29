# -*- coding: utf-8 -*-
"""
Outdoor sound propagation
=========================

Created on Tue Aug 11 14:22:44 2020

@author: joaovitor
"""


import numpy as np
from .air import Air
from .sources import SourceChain
# from receivers import ReceiverGrid
from .attenuations import divergence, ground, atmosphere


class Environment(object):
    """Main program object."""

    def __init__(self, temp, hum, atm, rect=[50., 0., 0., 50.]):
        self.air = Air(temp, hum, atm)
        self.rect = np.array(rect, dtype='float32')
        self._srcChains = []
        self._recGrids = None
        return

    @property
    def base(self):
        return np.sum(self.rect[:2]**2)**0.5

    @property
    def height(self):
        return np.sum(self.rect[2:]**2)**0.5

    @property
    def area(self):
        b = np.sum(self.base**2)**0.5
        h = np.sum(self.height**2)**0.5
        return b * h

    def setup_source_chain(self, dacvout, amppow, ampknob, spkohm):
        self._srcChains.append(SourceChain(dacvout, amppow, ampknob, spkohm))
        return

    # def grid_space(self, dx: float = None):

