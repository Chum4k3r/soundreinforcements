#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Aug  3 15:56:59 2020

@author: joaovitor
"""

import numpy as np
import soundreinforcements as srs

# Frequencies of analysis.
freqs = np.array([125, 250, 500, 1000, 2000, 4000], dtype='float32')

# Source power level for each frequency
powerlevel = np.array(freqs.size * [100])

# Air properties abstraction, for sound attenuation by air absorption.
air = srs.Air(temp=23.2, hum=66.5, atm=101310, freqs=freqs)

# A line source placed at (x=1.5, y=1.0, z=2.8) m and oriented to (nx=0, ny=1, nz=0)
src = srs.Source(pos=[1.5, 1., 2.8], ori=[0., 1., 0.], swl=powerlevel, directivity=0.5)

# Receivers, placed a few meters away from source, oriented towards the source, immersed in air
recs = []
recs.append(srs.Receiver(pos=[2.3, 9.4, 1.67], ori=[0., -1., 0.], air=air))
recs.append(srs.Receiver(pos=[4.2, 8.7, 1.87], ori=[0., -1., 0.], air=air))
recs.append(srs.Receiver(pos=[0.2, 12.5, 1.7], ori=[0., -1., 0.], air=air))

for num, rec in enumerate(recs):
    print(f"Receiver {num} at {rec.position()}, {rec.distance_from_source(src):2.2f} m away:")
    print(f"Frequencies: {freqs} Hz")
    print(f"SPL: {rec.spl_from_source(src)} dB ref 2e-5 Pa")
    print()
