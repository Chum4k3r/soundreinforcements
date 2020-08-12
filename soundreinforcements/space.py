#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 30 23:33:49 2020

@author: joaovitor
"""

import numpy as _np


class Coordinate(object):
    """Coordinate abstraction."""

    def __init__(self, x: float = 0., y: float = 0., z: float = 0.):
        """
        Coordinate representing a point in a three dimensional space.

        Parameters
        ----------
        x : float
            Value in the "x" axis.
        y : float
            Value in the "y" axis.
        z : float
            Value in the "z" axis.

        Returns
        -------
        None.

        """
        self._values = _np.array([x, y, z], dtype='float32')
        return

    def __repr__(self):
        return f"Coordinate({self.x}, {self.y}, {self.z})"

    def __call__(self):
        return self._values

    def __abs__(self):
        return (self.x**2 + self.y**2 + self.z**2)**0.5

    def __add__(self, other):
        obj = self._type_check(other)
        vals = self._values + obj()
        return type(self)(*vals)

    def __sub__(self, other):
        obj = self._type_check(other)
        vals = self._values - obj()
        return type(self)(*vals)

    def __dadd__(self, other):
        return type(self).__add__(self, other)

    def __dsub__(self, other):
        return type(self).__sub__(self, other)

    def __iadd__(self, other):
        obj = self._type_check(other)
        self._values += obj()
        return

    def __isub__(self, other):
        obj = self._type_check(other)
        self._values -= obj()
        return

    def _type_check(self, other):
        if type(other) in [list, tuple]:
            if len(other) != 3:
                raise ValueError("Operands must have len == 3 form.")
            obj = type(self)(*other)
        elif not isinstance(other, type(self)):
            raise ValueError(f"This operation is not valid between {type(self)} and {type(obj)}.")
        else:
            obj = other
        return obj

    @property
    def x(self):
        return self._values[0]

    @x.setter
    def x(self, nx):
        self._values[0] = nx
        return

    @property
    def y(self):
        return self._values[1]

    @y.setter
    def y(self, ny):
        self._values[1] = ny
        return

    @property
    def z(self):
        return self._values[2]

    @z.setter
    def z(self, nz):
        self._values[2] = nz
        return


class Orientation(Coordinate):
    """Orientation abstraction."""

    def __init__(self, x: float = 1., y: float = 0., z: float = 0.):
        """Orientation limits its values between -1.0 and 1.0. See `Coordinate`."""
        div = self._get_div([x, y, z])
        Coordinate.__init__(self, x/div, y/div, z/div)
        return

    def __repr__(self):
        return f"Orientation({self.x}, {self.y}, {self.z})"

    def __iadd__(self, other):
        obj = self._type_check(other)
        vals = self._values + obj()
        div = self._get_div(vals)
        self._values = vals/div
        return

    def __isub__(self, other):
        obj = self._type_check(other)
        vals = self._values - obj()
        div = self._get_div(vals)
        self._values = vals/div
        return

    def _get_div(self, vals):
        div = _np.sum(_np.array(vals, dtype='float32')**2)**0.5
        return div


class Object3D(object):
    """Abstraction of a three dimensional object with a position and orientation."""

    def __init__(self, pos: Coordinate, ori: Orientation):
        self.position = Coordinate()._type_check(pos)
        self.orientation = Orientation()._type_check(ori)
        return

    @property
    def position(self):
        return self._pos

    @position.setter
    def position(self, pos: Coordinate):
        if type(pos) != Coordinate:
            raise TypeError("Position must be a soundforce.Coordinate.")
        self._pos = pos
        return

    @property
    def orientation(self):
        return self._ori

    @orientation.setter
    def orientation(self, ori: Orientation):
        if type(ori) == Coordinate:
            self._ori = Orientation(*ori())
        elif type(ori) == Orientation:
            self._ori = ori
        else:
            raise TypeError("Orientation must be a soundforce.Orientation.")
        return



def distance(p1: Coordinate, p2: Coordinate) -> float:
    """
    Distance between two coordinates.

    Parameters
    ----------
    p1 : Coordinate
        Reference, or origin point.
    p2 : Coordinate
        Destiny point.

    Returns
    -------
    float
        The absolute distance between the two points..

    """
    return abs(p2 - p1)


def distance_over_plane(plane: str, p1: Coordinate, p2: Coordinate):
    """Projects both coordinates over a `plane`, to compute the 2D distance of the projection."""
    p1coord = p1()[:]
    p2coord = p2()[:]

    if plane == 'xy':
        p1coord[2] = p2coord[2] = 0.
    elif plane == 'xz':
        p1coord[1] = p2coord[1] = 0.
    elif plane == 'yz':
        p1coord[0] = p2coord[0] = 0.

    p1c = Coordinate(*p1coord)
    p2c = Coordinate(*p2coord)
    return distance(p1c, p2c)

