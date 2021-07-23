# -*- coding: utf-8 -*-
"""
Create polygons from an ordered set of points.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

import arcpy

if __name__ == "__main__":
    # for use as a command line script and with old style ArcGIS toolboxes (*.tbx)
    import utils
else:
    # for use as a module and Python toolboxes (*.pyt)
    from . import utils


def points_to_polygons(
    point_feature_class, polygon_feature_class, polygon_id_fieldname, sort_field_name
):
    """Create polygons from an ordered set of points."""
    # TODO Document parameters in the doc string

    lines = "in_memory\\lines"
    # Points To Lines (Basic License)
    arcpy.PointsToLine_management(
        point_feature_class, lines, polygon_id_fieldname, sort_field_name, "CLOSE"
    )
    # Lines To Polygon (Advanced License)
    arcpy.FeatureToPolygon_management(
        lines, polygon_feature_class, "", "ATTRIBUTES", ""
    )


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

    arg_count = len(args)
    if not arg_count == 4:
        usage = "Usage: {0} points polygons id_fieldname sort_fieldname"
        utils.die(usage.format(sys.argv[0]))

    # TODO: Check for Advanced (ArcInfo) license
    # TODO: check args, allow optional fields, provide defaults, check in points

    return args


if __name__ == "__main__":
    # Set command line or simple testing
    # sys.argv[1:] = ["C:/tmp/test.gdb/pts", "C:/tmp/test.gdb/polys", "name", "objectid"]
    utils.execute(points_to_polygons, parameter_fixer)
