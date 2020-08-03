# -*- coding: utf-8 -*-
"""
Air properties
==============

Sound propagates through the air, and many of its properties affects its propagation.
This module provides an abstraction of the air to obtain its properties and absorption.

Created on Thu Jul 30 22:52:15 2020

author: João Vitor Gutkoski Paes
"""


import numpy as _np


class Air(object):
    """Air acoustical properties object interface."""

    @staticmethod
    def get_absorption(temp: float, hum: float, atm: float, freq: _np.ndarray):
        """Calculates the air aborption coefficient in [m^-1]."""
        T0 = 293.15                # Reference temperature [k]
        T01 = 273.16               # 0 [C] in [k]
        T = temp + 273.15   # Input temp in [k]
        ps0 = 1.01325e5  # 1 atm in Pascals

        # Saturation pressure
        Csat = -6.8346 * _np.power(T01 / T, 1.261) + 4.6151
        rhosat = _np.power(10, Csat)
        h = rhosat * hum  * ps0 / atm

        # Nytrogen gas molecule (N2) relaxation frequency
        FrN2 = (atm/ps0) * _np.power(T0 / T, 0.5) * (
            9 + 280*h * _np.exp(-4.17 * (_np.power(T0 / T, 1/3) - 1)))

        # Oxygen gas molecule (O2) relaxation frequency
        FrO2 = (atm/ps0) * (24. + 4.04e4 * h * (0.02 + h) / (0.391 + h))

        # Air absorption in [dB/m]
        alpha = freq*freq * (
            1.84e-11 / (_np.power(T0 / T, 0.5) * atm / ps0)
            + _np.power(T / T0, -2.5)
            * (
                0.10680 * _np.exp(-3352 / T) * FrN2 / (freq*freq + FrN2*FrN2)
                + 0.01278 * _np.exp(-2293.1 / T) * FrO2 / (freq*freq + FrO2*FrO2)
              )
            )

        absorp_dBm = 20 * alpha / _np.log(10)
        absorp_m = absorp_dBm / (20*_np.log10(_np.exp(1)))
        return _np.float32(absorp_m), _np.float32(absorp_dBm)

    @staticmethod
    def get_properties(temp: float, hum: float, atm: float):
        """Calculate air properties acoustically relevant."""
        thermCond = 0.026  # W/(mK)
        temp += 273.16  # K
        airConst = 287.031  # J/K/kg
        h2oConst = 461.521  # J/K/kg
        Pierce = 0.0658 * temp**3 - 53.7558 * temp**2 \
                 + 14703.8127 * temp - 1345485.0465
        viscos = 7.72488e-8 * temp - 5.95238e-11 * temp**2 \
                 + 2.71368e-14 * temp**3
        constPress=4168.8 * (0.249679 - 7.55179e-5 * temp \
                             + 1.69194e-7 * temp**2 - 6.46128e-11 * temp**3);
        constVol=constPress - airConst  # (J/kg/K) for 260 K < T < 600 K
        Prandtl=viscos*constPress/thermCond;
        expans = constPress/constVol
        dens = atm/(airConst*temp) - (1/airConst - 1/h2oConst) * hum/100 * Pierce/temp
        velSom = (expans * atm / dens)**0.5
        return {"soundSpeed": velSom, "density": dens, "viscosity": viscos,
                "thermalConduct": thermCond, "specHeatRatio": expans, "prandtl": Prandtl,
                "specHeatCP": constPress, "specHeatCV": constVol, "impedance": velSom*dens}

    def __init__(self,
                 temp: float or int = 20,
                 hum: float or int = 50,
                 atm: float or int = 101325,
                 freqs: _np.ndarray = _np.array([63., 125., 250., 500.,
                                                 1000, 2000, 4000, 8000, 16000],
                                                dtype='float32')):
        """
        Air properties for acoustical parameters.

        Parameters
        ----------
        temp : float or int, optional
            Environment temperature, in Celsius degrees [°C]. The default is 20.
        hum : float or int, optional
            Relative humidity, as percentage [%]. The default is 50.
        atm : float or int, optional
            Atmospheric pressure, in Pascals [Pa]. The default is 101325.

        Returns
        -------
        None.

        """
        self.temperature = temp
        self.humidity = hum
        self.atmPressure = atm
        self.calc_properties()
        self.calc_absorption(freqs)
        return

    @property
    def temperature(self):
        """Air temperature in degree Celsius [°C]."""
        return self._temp

    @temperature.setter
    def temperature(self, temp: float or int):
        if type(temp) not in [float, int]:
            raise TypeError("Temperature must be a number.")
        elif temp < 0 or temp > 50:
            raise ValueError("Temperature must be between 0 and 50 °C.")
        self._temp = temp
        return

    @property
    def humidity(self):
        """Air relative humidity in percentage [%]."""
        return self._hum

    @humidity.setter
    def humidity(self, hum):
        if type(hum) not in [float, int]:
            raise TypeError("Humidity must be a number.")
        elif hum < 0 or hum > 100:
            raise ValueError("Humidity must be between 0 and 100 %.")
        self._hum = hum
        return

    @property
    def atmPressure(self):
        """Atmospherical pressure in Pascals [Pa]."""
        return self._atm

    @atmPressure.setter
    def atmPressure(self, atm):
        if type(atm) not in [float, int]:
            raise TypeError("Atmospheric pressure must be a number.")
        elif atm < 90e3 or atm > 115e3:
            raise ValueError("Atmospheric pressure must be between 90 and 115 kPa.")
        self._atm = atm
        return

    @property
    def soundSpeed(self):
        """Sound speed in meters per second [m/s]."""
        return self._props["soundSpeed"]

    @property
    def density(self):
        """Specific, or volumetric, density in kilograms per cubic meter [kg/m³]."""
        return self._props["density"]

    @property
    def impedance(self):
        """Characteristic impedance in rayls per square meter [rayl/m²]."""
        return self._props["impedance"]

    @property
    def specHeatCP(self):
        """Specific heat at Constant Pressure [J/kg·K]."""
        return self._props["specHeatCP"]

    @property
    def specHeatCV(self):
        """Specific heat at Constant Volume [J/kg·K]."""
        return self._props["specHeatCV"]

    @property
    def specHeatRatio(self):
        """
        Ratio between specific heat at constant pressure
        and specific heat at constant volume [-].
        """
        return self._props["specHeatRatio"]

    @property
    def viscosity(self):
        """Dynamic viscosity [Ns/m²]."""
        return self._props["viscosity"]

    @property
    def prandtl(self):
        """Prandtl number [-]."""
        return self._props["prandtl"]

    @property
    def thermalConduct(self):
        """Thermal conductivity [W/m·K]."""
        return self._props["thermalConduct"]

    @property
    def frequencies(self):
        """Frequencies for which the air absorption was calculated, in Hertz [Hz]."""
        return self._freqs

    def absorption(self, unit: str):
        """Air absorption [1/m]."""
        if unit == '1/m':
            return self._props["absorb"]
        elif unit == 'dB/m':
            return self._props["absorb_dB"]
        else:
            raise ValueError(f"Unit must be '1/m' or 'dB/m', found: {unit}.")

    def calc_properties(self):
        """
        Calculate the air acoustically relevant properties.

        The `AirProperties` basic values, `temperature`, `humidity` and
        `atmPressure` can be set at will, but this method must be explicitly
        called to update the properties values.

        Returns
        -------
        None.

        """
        self._props = Air.get_properties(self.temperature,
                                         self.humidity,
                                         self.atmPressure)
        return

    def calc_absorption(self, freqs: _np.ndarray):
        """
        Calculate the air absorption as an inverse of meter factor.

        Also hold the frequency array used as base for the calculations.

        Parameters
        ----------
        freqs : _np.ndarray
            Array of frequencies to evaluate the air absorption.

        Returns
        -------
        None.

        """
        self._freqs = freqs
        self._props["absorb"], self._props["absorb_dB"] = \
            Air.get_absorption(self.temperature, self.humidity,
                               self.atmPressure, self.frequencies)
        return

