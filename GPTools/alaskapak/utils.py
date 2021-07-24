# -*- coding: utf-8 -*-
"""
Utility functions for use with ArcGIS 10.1
Created: 2013-10-24
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

import arcpy


def die(msg):
    """Print error message to console and ArcGIS and exit."""
    arcpy.AddError(msg)
    sys.exit()


def warn(msg):
    """Print warning message to console and ArcGIS."""
    arcpy.AddWarning(msg)


def info(msg):
    """Print info message to console and ArcGIS."""
    arcpy.AddMessage(msg)


def is_float(something):
    """Return True is something is convertible to a floating point number."""
    try:
        float(something)
    except (ValueError, TypeError):
        return False
    return True


def is_int(something):
    """Return True is something is convertible to a integer number."""
    try:
        int(something)
    except (ValueError, TypeError):
        return False
    return True


def float_range(start, stop, step=1.0):
    """Return a range of numbers from x to y by jump increments.
    It is intended to be a floating point version of range()."""

    if step == 0:
        raise ValueError("jump must be non-zero")
    if step > 0:
        while start < stop:
            yield start
            start += step
    else:
        while start > stop:
            yield start
            start += step


def get_points(point_feature, spatial_reference=None):
    """returns a python list of (x,y) pairs"""
    with arcpy.da.SearchCursor(
        point_feature, "SHAPE@XY", spatial_reference=spatial_reference
    ) as cursor:
        points = [row[0] for row in cursor]
    return points


# Maps the string returned by Describe.Field.type and ListFields().type
# to the string required by arcpy.AddField()
# Field.type = SmallInteger, Integer, Single, Double, String, Date, OID, Geometry, BLOB.
# AddField() types: TEXT, FLOAT, DOUBLE, SHORT, LONG, DATE, BLOB, RASTER, GUID
type_map = {
    "SmallInteger": "SHORT",
    "Integer": "LONG",
    "Single": "FLOAT",
    "Double": "DOUBLE",
    "String": "TEXT",
    "Date": "DATE",
    "OID": "LONG",  # Not creatable with AddField() - use caution
    "Geometry": "BLOB",  # Not creatable with AddField() - use caution
    "BLOB": "BLOB",
}


def get_database(data_set):
    r"""Returns the database even if data_set is in a feature dataset.

    Examples:
      C:\data\access.mdb\table => C:\data\access.mdb
      C:\data\db.gdb\network\junctions => C:\data\db.gdb
      C:\data\conn.sde\roads  => C:\data\conn.sde
      C:\data\lines.shp  => C:\data

    Args:
        data_set (text): A catalog path to a table or feature class

    Returns:
        text: the path to the database
    """
    workspace = os.path.dirname(arcpy.Describe(data_set).catalogPath)
    desc = arcpy.Describe(workspace)
    if hasattr(desc, "datasetType") and desc.datasetType == "FeatureDataset":
        workspace = os.path.dirname(workspace)
    return workspace


def valid_field_name(field_name, data_set):
    """Returns field_name or a slight modification suitable for the data_set.

    Args:
        field_name (text): The desired field name.
        data_set (text): An ArcGIS dataset, i.e feature class or table.

    Returns:
        text: The new acceptable field name.
    """
    workspace = get_database(data_set)
    new_field_name = arcpy.ValidateFieldName(field_name, workspace)
    return new_field_name


def execute(task, transformer=None):
    """Execute a task with transformed toolbox parameters (or command line arguments).

    Args:
       task (callable): The function to execute
       transformer (callable): an optional function to transform and/or validate
       the toolbox parameters to match the task arguments
    """
    args = []
    try:
        # Collect arcpy parameters until empty or they throw an exception
        i = 0
        # Toolbox may send an empty string for an optional parameter
        while True:
            args.append(arcpy.GetParameterAsText(i))
            i += 1
            # Modifying the sys.argv for testing seems to add an infinite
            # number of empty parameters
            if i == 20:
                raise ValueError("Too many parameters")
    except (RuntimeError, ValueError):
        pass
    if transformer is not None:
        args = transformer(args)
    task(*args)
