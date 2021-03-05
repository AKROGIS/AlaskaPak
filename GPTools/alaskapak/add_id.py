# -*- coding: utf-8 -*-
"""
Add a unique integer id to one or more feature classes.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import arcpy


def add_id_commandline():
    """Parse and validate command line arguments then add id to features."""
    # get input
    features = arcpy.GetParameterAsText(0)
    id_field_name = arcpy.GetParameterAsText(1)
    start = arcpy.GetParameterAsText(2)
    increment = arcpy.GetParameterAsText(3)
    sort_field_name = arcpy.GetParameterAsText(4)

    # validate input
    if id_field_name in ["", "#"]:
        id_field_name = "UniqueID"
    try:
        start = int(start)
    except ValueError:
        start = 1

    try:
        increment = int(increment)
    except ValueError:
        increment = 1
    add_id_multiple(features, id_field_name, start, increment, sort_field_name)


# process features
def add_id_multiple(
    features, field_name="UniqueID", start=1, increment=1, sort_field_name=None
):
    """Add id to multiple feature classes."""

    for feature in features.split(";"):
        add_id(feature, field_name, start, increment, sort_field_name)


def add_id(
    feature_class, field_name="UniqueID", start=1, increment=1, sort_field_name=None
):
    """Add id to a feature class."""

    if feature_class[0] == "'" and feature_class[-1] == "'":
        feature_class = feature_class[1:-1]
    arcpy.AddMessage("Adding Id to " + feature_class)
    if field_name not in arcpy.ListFields(feature_class):
        arcpy.AddField_management(
            feature_class,
            field_name,
            "Long",
            "",
            "",
            "",
            "",
            "NULLABLE",
            "NON_REQUIRED",
            "",
        )
    feature_id = start

    # WARNING: shapefiles do not support ORDER BY
    if sort_field_name:
        order_by = "ORDER BY {0}".format(sort_field_name)
    else:
        order_by = None
    with arcpy.da.UpdateCursor(
        feature_class, [field_name], sql_clause=(None, order_by)
    ) as cursor:
        for row in cursor:
            row[0] = feature_id
            feature_id += increment
            cursor.updateRow(row)
