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
from typing import List
import numpy as _np



class Source(Object3D):
    """Sound source abstraction."""

    def __init__(self, pos: List[float], ori: List[float],
                 swl: _np.ndarray, directivity: int = 1):
        Object3D.__init__(self, pos, ori)
        self.swl = _np.float32(swl)
        self.directivity = directivity
        return


