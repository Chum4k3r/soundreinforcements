#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Sources
=======

This module provide an abstraction for sound reinforcement systems sources


Created on Thu Jul 30 23:31:02 2020

@author: joaovitor
"""


from .space import Object3D
from .levelmaths import power_from_wave, swl_from_power
from typing import List
import numpy as _np


class Audio(object):
    """Audio data abstraction."""

    def __init__(self, data: _np.ndarray, fs: int):
        self.data = _np.float32(data)
        self.fs = _np.int32(fs)
        return


class Source(Object3D):
    """Sound source abstraction."""

    def __init__(self, pos: List[float], ori: List[float],
                 power: _np.ndarray, directivity: int = 2):
        Object3D.__init__(self, pos, ori)
        self.power = _np.float32(power)
        self.directivity = directivity
        return

    @property
    def swl(self):
        return swl_from_power(self.power)


class SourceChain(object):
    """Class abstraction for signal output chain."""

    def __init__(self, dacvout: float = 3.1, amppow: float = 100,
                 ampknob: float = 0.5, spkohm: float = 4):
        self.audios = {}
        self.dacVout = _np.float32(dacvout)
        self.ampKnob = _np.float32(ampknob)
        self.ampPower = _np.float32(amppow)
        self.spkImpedance = _np.float32(spkohm)
        return

    def add_audio(self, id: int or str, audio: Audio):
        self.audios[id] = audio
        return

    def output_power(self, id: int or str):
        amp = self.dacVout * self.ampKnob * (self.ampPower / self.spkImpedance)**0.5
        aud = self.audios[id].data * amp
        return power_from_wave(aud)

    def audio_source(self, id: int or str, pos: List[float],
                     ori: List[float], directivity: int = None):
        return Source(pos, ori, self.output_power(id), directivity)
