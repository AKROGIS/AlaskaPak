# -*- coding: utf-8 -*-
"""
Calculates the length of the longest axis on a polygon

Created by Regan Sarwas on 2010-08-30
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import os
import sys

import arcpy

if __name__ == "__main__":
    # for use as a command line script and with old style ArcGIS toolboxes (*.tbx)
    import utils
else:
    # for use as a module and Python toolboxes (*.pyt)
    from . import utils


def longest_axis(in_features, out_features, name="MaxAxis"):
    """out_features is a copy of in_features with a new double field called name
    with the value of the larger of the width or height of the bounding box"""

    make_feature_class(in_features, out_features, name)
    add_max_axis(out_features, name)


def make_feature_class(in_features, out_features, name):
    """Copy the in_features to out_features and add double column `name`"""
    arcpy.CopyFeatures_management(in_features, out_features)
    arcpy.AddField_management(
        out_features, name, "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""
    )


def add_max_axis(feature_class, name):
    """Add the the max axis value to the column `name` in feature_class"""
    with arcpy.da.UpdateCursor(feature_class, ["Shape@", name]) as cursor:
        for row in cursor:
            row[1] = max_axis(row[0])
            cursor.updateRow(row)


def max_axis(geom):
    """Return the max width or height of the geom extents"""
    return max(geom.extent.width, geom.extent.height)


# New Brute Force Algorithm:
#
# for poly in polygons:
#  n = number of vertices
#  max = 0;
#  for v1 = range(0 to n-4):
#   for v2 = range(v1+2 to n-1):
#    line = create line from v1 to v2
#    dist = length of line
#    if max < dist:
#     if line is completely within poly:
#      max = dist
#  store max as attribute in poly

# Checking for line within poly for every line is probably very very expensive,
# and cannot be done effectively in python.  Use arcobjects


def parameter_fixer(args):
    """Validates and transforms the command line arguments for the task.

    1) Converts text values from old style toolbox (*.tbx) parameters (or the
       command line) to the python object arguments expected by the primary task
       of the script, and as provided by the new style toolbox (*.pyt).
    2) Validates the correct number of arguments.
    3) Provides default values for command line options provided as "#"
       or missing from the end of the command line.
    4) Provides additional validation for command line parameters to match the
       validation done by the toolbox interface.  This isn't required when
       called by an old style toolbox, but it isn't possible to tell it is
       called by the toolbox or by the command line.

    Args:
        args (list[text]): A list of commands arguments, Usually obtained
        from the sys.argv or arcpy.GetParameterAsText().  Provide "#" as
        placeholder for an unspecified intermediate argument.

    Returns:
        A list of validated arguments expected by the task being called.
        Exits with an error message if the args cannot be transformed.
    """

    # TODO: Allow optional argument
    arg_count = len(args)
    if arg_count < 2 or arg_count > 3:
        usage = "Usage: {0} in_features, out_features, [name]"
        utils.die(usage.format(sys.argv[0]))

    # TODO: check parameters and provide default values

    # make sure output workspace exists
    # ArcGIS (toolbox or command line) does not do any validation on the output workspace
    path, _ = os.path.split(args[1])
    if not arcpy.Exists(path):
        utils.die("Error: The output workspace does not exist.")

    return args


if __name__ == "__main__":
    # Set command line or simple testing
    # sys.argv[1:] = ["TODO Make test case"]
    utils.execute(longest_axis, parameter_fixer)
