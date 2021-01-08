# ------------------------------------------------------------------------------
# Utils101.py
# Created: 2013-10-24
#
# Utility functions for use with ArcGIS 10.1
# ------------------------------------------------------------------------------

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
    """Returns True if *something* is a float, or something convertible to a float like '4.2'"""
    try:
        float(something)
    except (ValueError, TypeError):
        return False
    return True


def is_int(something):
    """Returns True if *something* is an int, or something convertible to an int like '42'"""
    try:
        int(something)
    except (ValueError, TypeError):
        return False
    return True


def frange(x, y, jump):
    """Return a range of numbers from x to y by jump increments.
    It is intended to be a floating point version of range()."""

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
    """returns a python list of (x,y) pairs"""
    with arcpy.da.SearchCursor(points_feature, 'SHAPE@XY', spatial_reference=sr) as searchCursor:
        points = [row[0] for row in searchCursor]
    return points
