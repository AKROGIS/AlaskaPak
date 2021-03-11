# -*- coding: utf-8 -*-
"""
Create rectangular building polygons from a single edge.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

import arcpy

from . import line_to_rectangle


def square_buildings(edges, buildings):
    """Create rectangular building polygons from a single edge.

    Args:
        edges (text): An ArcGIS data source path to a existing polyline feature
            class. Must have fields `Width_Ft` (Double) and `Right_Left`
            ("R{ight}"|"L{eft}").
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
        "!Width_Ft! * 0.3048 * (1 if !Right_Left!.lower()[0] == 'r' else -1)",
        expression_type,
    )
    # Process: Line to Rectangle
    line_to_rectangle.line_to_rectangle(temp_edges, temp_field, buildings)
    arcpy.DeleteField_management(buildings, temp_field)
    arcpy.Delete(temp_edges)
