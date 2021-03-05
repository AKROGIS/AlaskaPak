# -*- coding: utf-8 -*-
"""
Create rectangular building polygons from a single edge.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import arcpy

# Load required toolboxes
arcpy.ImportToolbox("X:/GIS/Toolboxes/10.0/Alaska Pak Development.tbx")

# Script arguments
Building_Edges = arcpy.GetParameterAsText(0)

Building_Polygons = arcpy.GetParameterAsText(1)

# Local variables:
edges = Building_Edges
edges__2_ = edges
edges__3_ = edges__2_
Building_Polygons__2_ = Building_Polygons

# Process: Copy Features
arcpy.CopyFeatures_management(Building_Edges, edges, "", "0", "0", "0")

# Process: Add Field
arcpy.AddField_management(
    edges, "zz_offset", "DOUBLE", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""
)

# Process: Calculate Field
arcpy.CalculateField_management(
    edges__2_,
    "zz_offset",
    "!Width_Ft! * 0.3048 * (1 if !Right_Left!.lower()[0] == 'r' else -1)",
    "PYTHON",
    "",
)

# Process: Line to Rectangle
arcpy.Line2Rect_AlaskaPak(edges__3_, "zz_offset", Building_Polygons)

# Process: Delete Field
arcpy.DeleteField_management(Building_Polygons, "zz_offset")
