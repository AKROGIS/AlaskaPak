# -*- coding: utf-8 -*-
"""
Create polygons from an ordered set of points.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import arcpy


def points_to_polygons(
    point_feature_class, polygon_feature_class, polygon_id_fieldname, sort_field_name
):
    """Create polygons from an ordered set of points."""
    # TODO Document parameters in the doc string

    lines = "in_memory\\lines"
    # Points To Lines
    arcpy.PointsToLine_management(
        point_feature_class, lines, polygon_id_fieldname, sort_field_name, "CLOSE"
    )
    # Lines To Polygon
    arcpy.FeatureToPolygon_management(
        lines, polygon_feature_class, "", "ATTRIBUTES", ""
    )


if __name__ == "__main__":
    points = arcpy.GetParameterAsText(0)
    polygons = arcpy.GetParameterAsText(1)
    id_fieldname = arcpy.GetParameterAsText(2)
    sort_fieldname = arcpy.GetParameterAsText(3)
    points_to_polygons(points, polygons, id_fieldname, sort_fieldname)
