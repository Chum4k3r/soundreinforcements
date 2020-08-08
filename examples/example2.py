#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Aug  8 02:36:00 2020

@author: joaovitor
"""

import numpy as np
import soundreinforcements as srs


SAMPLERATE = 48000

# Frequencies of analysis.
freqs = np.array([125, 250, 500, 1000, 2000, 4000], dtype='float32')  # Hz


# Random noise sound, single channel, with normalized amplitude and 2 seconds of duration
rnd = np.random.randn(2 * SAMPLERATE)
rnd /= np.max(np.abs(rnd))

# Audio abstraction of the random noise
rndAud = srs.Audio(rnd, SAMPLERATE)


# Air properties abstraction, for sound attenuation by air absorption.
air = srs.Air(temp=23.2,  # °C
              hum=66.5,   # %
              atm=101310, # Pa
              freqs=freqs)


# Absraction of audio output chain of gains.
audOutput = srs.SourceChain(dacvout=5.0,   # Digital to analog converter output voltage

                            amppow=200.0,  # Power amplification of power amplifier (...)
                            ampknob = 0.6, # Input knob: 0 for turned to minimum,
                                           # and 1 for turned to maximum

                            spkohm=8.0)    # Speaker input impedance

# Include audio of random noise as simulation signal
audOutput.add_audio('noise', rndAud)


# Generate a source with power provided from audio signal and source chain
src = audOutput.audio_source('noise', pos=[1.5, 1., 2.8],
                             ori=[0., 1., 0.], directivity=0.5)


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
