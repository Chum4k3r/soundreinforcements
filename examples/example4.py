#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Aug 12 19:46:47 2020

@author: joaovitor
"""

import soundreinforcements as srs
import matplotlib.pyplot as plt

# Two sources with 200 W each
src1 = srs.Source([0., 20., 0.], [0., 1., 0.], 200)
src2 = srs.Source([0., -20., 0.], [0., 1., 0.], 200)

# A venue space
rg = srs.ReceiversGrid(0., 301., 1, -100., 101., 1, 1.8, srs.Air())

# SPL for each sound source
p1 = rg.eval_pressure(src1)
p2 = rg.eval_pressure(src2)

# Sum the pressures and calculate the sound pressure level
spl = srs.level.spl_from_pressure(p1 + p2)


# View the SPL field
fig, ax = plt.subplots()
h = ax.pcolormesh(rg.xs, rg.ys, spl[:, :, 4], cmap='jet', vmin=55., vmax=135., shading='auto')
cb = fig.colorbar(h, ax=ax, extend='both')
fig.show()

