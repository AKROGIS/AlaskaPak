# -*- coding: utf-8 -*-
"""
Add a unique integer id to one or more feature classes.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import arcpy

# get input
featureList = arcpy.GetParameterAsText(0)
idFieldName = arcpy.GetParameterAsText(1)
start = arcpy.GetParameterAsText(2)
increment = arcpy.GetParameterAsText(3)
sortFieldName = arcpy.GetParameterAsText(4)

# validate input
if idFieldName in ["", "#"]:
    idFieldName = "UniqueID"
try:
    start = int(start)
except ValueError:
    start = 1

try:
    increment = int(increment)
except ValueError:
    increment = 1

# process features
for feature in featureList.split(";"):
    if feature[0] == "'" and feature[-1] == "'":
        feature = feature[1:-1]
    arcpy.AddMessage("Adding Id to " + feature)
    if idFieldName not in arcpy.ListFields(feature):
        arcpy.AddField_management(
            feature, idFieldName, "Long", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""
        )
    feature_id = start

    # WARNING: shapefiles do not support ORDER BY
    if sortFieldName:
        order_by = "ORDER BY {0}".format(sortFieldName)
    else:
        order_by = None
    with arcpy.da.UpdateCursor(
        feature, [idFieldName], sql_clause=(None, order_by)
    ) as cursor:
        for row in cursor:
            row[0] = feature_id
            feature_id += increment
            cursor.updateRow(row)
