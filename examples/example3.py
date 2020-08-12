#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Aug 11 18:23:29 2020

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
spl1 = rg.eval_spl(src1)
spl2 = rg.eval_spl(src2)

# Sum the pressures and calculate the sound pressure level
spl = srs.levelmaths.spl_from_pressure(
    srs.levelmaths.pressure_from_spl(spl1)
    + srs.levelmaths.pressure_from_spl(spl2)
    )

# View the SPL field
fig, ax = plt.subplots()
h = ax.pcolormesh(rg.xs, rg.ys, spl[:, :, 8], cmap='jet', vmin=55., vmax=135.)
cb = fig.colorbar(h, ax=ax, extend='both')
