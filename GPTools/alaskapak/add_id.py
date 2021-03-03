# -*- coding: utf-8 -*-
"""
AddID.py
Created: 2011-01-25

Title:
Add Unique ID to a dataset

Tags:
unique, identification, calculate, attribute, column, field

Summary:
This tool will add and populate an ID field to a list of feature classes.

Usage:
This tool will add a user controllable id field

Parameter 1:
Data_set
A semicolon separated list of data sets. If it has a field called idFieldName it will be overwritten, and it must be of type long.

Parameter 2:
Field_Name
The name of the field to hold the unique id. If the field does not exist, it will be added. If the field exists, it must be an editable number or text field. The field name must be a valid for the features workspace i.e. no spaces, no reserved words, and less than 10 characters for shapefiles.
This field is optional.  Default value is "UniqueID"

Parameter 3:
Starting_Value
The starting value for the ids.  Each feature class starts over with this value.
This field is optional.  Default value is 1

Parameter 4:
Increment
Consecutive ids will be incremented by this value.
This field is optional.  Default value is 1

Parameter 5:
Sort_Field
The name of an existing field in all feature classes.  Data will be sorted in ascending order before the id is added.
This field is optional.  Default value is None (i.e. no sorting)

Scripting Syntax:
AddID_AlaskaPak (Data_set, Field_Name, Starting_Value, Increment, Sort_Field)

Example1:
Scripting Example
The following example shows how this script can be used in another python script, or directly in the ArcGIS Python Window.  It assumes that the script has been loaded into a toolbox, and the toolbox has been loaded into the active session of ArcGIS.
 # Give all roads an even id number starting with the shortest
 features = r"C:\tmp\roads.shp"
 AddID_AlaskaPak(features, "EvenIDs", 2, 2, length)

Example2:
Command Line Example
The following example shows how the script can be used from the operating system command line.  It assumes that the current directory is the location of the script, and that the python interpreter is the path.
 C:\tmp> python AddMiles.py "C:\tmp\roads.shp;C:\tmp\test.gdb\fences" newID 1 1

Credits:
Regan Sarwas, Alaska Region GIS Team, National Park Service

Limitations:
Public Domain

Requirements
arcpy module - requires ArcGIS v10+ and a valid license

Disclaimer:
This software is provide "as is" and the National Park Service gives
no warranty, expressed or implied, as to the accuracy, reliability,
or completeness of this software. Although this software has been
processed successfully on a computer system at the National Park
Service, no warranty expressed or implied is made regarding the
functioning of the software on another system or for general or
scientific purposes, nor shall the act of distribution constitute any
such warranty. This disclaimer applies both to individual use of the
software and aggregate use with other software.
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
    id = start

    # WARNING: shapefiles do not support ORDER BY
    if sortFieldName:
        order_by = "ORDER BY {0}".format(sortFieldName)
    else:
        order_by = None
    with arcpy.da.UpdateCursor(
        feature, [idFieldName], sql_clause=(None, order_by)
    ) as cursor:
        for row in cursor:
            row[0] = id
            id += increment
            cursor.updateRow(row)
