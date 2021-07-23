# -*- coding: utf-8 -*-
"""
Create rectangular building polygons from a single edge.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

import arcpy

if __name__ == "__main__":
    # for use as a command line script and with old style ArcGIS toolboxes (*.tbx)
    import utils
    import line_to_rectangle
else:
    # for use as a module and Python toolboxes (*.pyt)
    from . import utils
    from . import line_to_rectangle


def square_buildings(edges, buildings):
    """Create rectangular building polygons from a single edge.

    Args:
        edges (text): An ArcGIS data source path to a existing polyline feature
            class. Must have fields `Width_Ft` (Double) and `Right_Left` (text).
        buildings (text): An ArcGIS data source path to the polygon feature
            class that will be created.
    """

    # Local variables:
    temp_edges = "in_memory/edges"
    # TODO: make sure temp_field is unique, make it so if not.
    temp_field = "zz_offset"
    expression_type = "PYTHON3"
    if sys.version_info[0] < 3:
        expression_type = "PYTHON_9.3"

    # Create an in memory copy of edges and prep it for line_to_rectangles
    arcpy.CopyFeatures_management(edges, temp_edges, "", "0", "0", "0")
    arcpy.AddField_management(temp_edges, temp_field, "DOUBLE")
    arcpy.CalculateField_management(
        temp_edges,
        temp_field,
        # FIXME: Will crash with Right_Left null or empty
        "!Width_Ft! * 0.3048 * (1 if !Right_Left!.lower()[0] == 'r' else -1)",
        expression_type,
    )
    # Process: Line to Rectangle
    line_to_rectangle.line_to_rectangle(temp_edges, temp_field, buildings)
    arcpy.DeleteField_management(buildings, temp_field)
    arcpy.Delete(temp_edges)


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
    if not arg_count == 2:
        usage = "Usage: {0} edge_features building_features"
        utils.die(usage.format(sys.argv[0]))

    # TODO: check that args[0] is an existing line feature class
    # with fields `Width_Ft` (Double) and `Right_Left` (string).

    return args


if __name__ == "__main__":
    # Set command line or simple testing
    # sys.argv[1:] = ["C:/tmp/test.gdb/bldg_edge", "C:/tmp/test.gdb/bldg_footprint"]
    utils.execute(square_buildings, parameter_fixer)
