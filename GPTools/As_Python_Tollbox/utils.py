"""
Utility functions for use with AlaskaPak Scripts

:Created: 2013-10-24

:Credits:
  Regan Sarwas, Alaska Region GIS Team, National Park Service

:License:
  Public Domain

:Disclaimer:
  This software is provide "as is" and the National Park Service gives
  no warranty, expressed or implied, as to the accuracy, reliability,
  or completeness of this software. Although this software has been
  processed successfully on a computer system at the National Park
  Service, no warranty expressed or implied is made regarding the
  functioning of the software on another system or for general or
  scientific purposes, nor shall the act of distribution constitute any
  such warranty. This disclaimer applies both to individual use of the
  software and aggregate use with other software.

Requirements:
  * Python 2.7+ or 3.x
  * ArcGIS arcpy module v10.1+ basic (or better) license
"""

import sys

import arcpy
import arcpy.da


def die(msg):
        arcpy.AddError(msg)
        print("ERROR: " + str(msg))
        sys.exit()


def warn(msg):
        arcpy.AddWarning(msg)
        print("Warning: " + str(msg))


def info(msg):
        arcpy.AddMessage(msg)
        print("Info: " + str(msg))


def is_float(something):
    """Returns True if *something* is a float,
    or something convertible to a float like '4.2'
    """
    try:
        float(something)
    except (ValueError, TypeError):
        return False
    return True


def is_int(something):
    """Returns True if *something* is an int,
    or something convertible to an int like '42'
    """
    try:
        int(something)
    except (ValueError, TypeError):
        return False
    return True


def frange(x, y, jump):
    """Return a range of numbers from x to y by jump increments.
    It is intended to be a floating point version of range().
    """

    if jump == 0:
        raise ValueError("jump must be non-zero")
    if jump > 0:
        while x < y:
            yield x
            x += jump
    else:
        while x > y:
            yield x
            x += jump


def get_points(points_feature, sr=None):
    """Returns a python list of (x,y) pairs"""
    with arcpy.da.SearchCursor(points_feature, 'SHAPE@XY',
                               spatial_reference=sr) as searchCursor:
        points = [row[0] for row in searchCursor]
    return points
