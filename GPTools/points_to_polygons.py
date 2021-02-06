# -*- coding: utf-8 -*-
"""
# Point2Poly.py
# Created on: 2011-01-26 16:13:49.00000
#   (generated by ArcGIS/ModelBuilder)
# Usage: Point2Poly <Point_Features> <Polygon_Features> <Polygon_Id_Field> <Sort_Field>
# Description:
# Takes an ordered set of points and converts them to a set of polygons
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import arcpy

# Script arguments
Point_Features = arcpy.GetParameterAsText(0)
Polygon_Features = arcpy.GetParameterAsText(1)
Polygon_Id_Field = arcpy.GetParameterAsText(2)
Sort_Field = arcpy.GetParameterAsText(3)

lines = "in_memory\\lines"

# Points To Lines
arcpy.PointsToLine_management(
    Point_Features, lines, Polygon_Id_Field, Sort_Field, "CLOSE"
)
# Lines To Polygon
arcpy.FeatureToPolygon_management(lines, Polygon_Features, "", "ATTRIBUTES", "")