# -*- coding: utf-8 -*-
"""
Line2Rect.py
Created: 2011-01-14

Title:
Lines to Rectangles

Tags:
Building, Offset, Width, Height, Square, Polygon

Summary:
This tool will derive rectangles from lines and associated offsets.

Usage:
Use this tool to build a polygon feature class containing rectangles derived from a line feature class.  The line feature class must contain an attribute for each feature which provides the perpendicular distance from the line to the far side of the rectangle.

Parameter 1:
Line_Features
The full name of a polyline feature class.  Each line defines the base or first side of a generated rectangle. Each line can have 1 or more parts (i.e. it may be a multi-line), and there may be two or more vertices in each part, however only the first and last vertex of each part are used in the output rectangle.  If the line is a multi-part shape, then the rectangle is also a multi-part shape.  If any line (or part) is degenerate (i.e. a single vertex, or first vertex and last vertex are the same) then that line (or line part) is skipped. If all parts in the line are degenerate then no output is created for that line.

Parameter 2:
Rectangle_Width_Field
This is the name of an attribute (column/field) in the line feature class which specifies the width of the rectangle. Width may also be known as offset or height.  Specifically It is the distance perpendicular to the line at which the far side of the rectangle is drawn. If the width is positive, the rectangle is drawn on the right side of the line.  If it is negative it is drawn on the left side.  Right and left are from the perspective of the line looking from the first vertex to the last. The width must be a numeric (integer or real) field, and it must be in the same units/coordinate system as the line feature class. The field name can be either an actual field name, or the alias for the field name.  Actual field names are given priority in case of ambiguity.

Parameter 3:
Rectangle_Features
The full name of a polygon feature class to create.  Any existing feature class at that path will not be overwritten, and the script will issue an error if the feature class exists (unless the geoprocessing options are set to overwrite output). The output feature class will have the same spatial reference system as the input. If the input feature class has Z or M values then the output will as well, however no Z or M values will be written to the output. All attributes of the line feature class are copied to the output feature class, except Shape, OID, and any non-editable fields (i.e. Shape_Length).

Scripting Syntax:
Line2Rect(Line_Features, Rectangle_Width_Field, Rectangle_Features)

Example1:
Scripting Example
The following example shows how this script can be used in another python script, or directly in the ArcGIS Python Window.  It assumes that the script has been loaded into a toolbox, and the toolbox has been loaded into the active session of ArcGIS.
 lineFC = r"C:\tmp\gps_lines.shp"
 rectFC = r"C:\tmp\test.gdb\park\bldg"
 Line2Rect(lineFC, "width", rectFC)

Example2:
Command Line Example
The following example shows how the script can be used from the operating system command line.  It assumes that the current directory is the location of the script, and that the python interpreter is the path.
 C:\tmp> python Line2Rect.py "c:\tmp\gps_lines.shp" "width" "c:\tmp\test.gdb\park\bldg"

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

import math
import os
import sys

import arcpy


def MakeRect(pt1, pt2, width):
    """Assumes pt1 and pt2 are arcpy.Points, and width is numeric.
    Returns a tuple of the next two points in the rectangle.
    Points proceed clockwise for a positive width and
    counterclockwise for a negative width."""
    # Find the angle of the line between the points
    dx = pt2.X - pt1.X
    dy = pt2.Y - pt1.Y
    angle = math.atan2(dy, dx)
    # find the endpoint of a line width long and
    # rotated 90 degrees to the right
    angle = angle - math.pi / 2.0
    y = width * math.sin(angle)
    x = width * math.cos(angle)
    # add that end point to the two points given
    pt3 = arcpy.Point(pt2.X + x, pt2.Y + y)
    pt4 = arcpy.Point(pt1.X + x, pt1.Y + y)
    return (pt3, pt4)


def MakeRectFromLine(line, width):
    """Assumes an arcpy.Polyline for input, and returns an
    arcpy.Polygon or None.  If the input is multipart, so is output.
    Any degenerate parts (single vertex, or first == last) are
    ignored.  If all parts are degenerate, None is returned."""
    # skip bad shapes
    if line.partCount == 0:
        return None
    # skip bad width
    if width == None or width == 0:
        return None
    if line.isMultipart:
        parray = arcpy.Array()
        parts = line.getPart()
        for part in parts:
            # part is an array of points
            if len(part) == 0:
                continue  # bad part
            pt1 = part[0]
            pt2 = part[len(part) - 1]
            if pt1.equals(pt2):
                continue  # baseline for rect cannot be a point
            pt3, pt4 = MakeRect(pt1, pt2, width)
            parray.add(arcpy.Array([pt1, pt2, pt3, pt4, pt1]))
        if len(parray) == 0:
            return None
        return arcpy.Polygon(parray)
    else:
        pt1 = line.firstPoint
        pt2 = line.lastPoint
        if pt1.equals(pt2):  # this equals is an arcpy method
            return None
        pt3, pt4 = MakeRect(pt1, pt2, width)
        return arcpy.Polygon(arcpy.Array([pt1, pt2, pt3, pt4, pt1]))


# Get and check input
if len(sys.argv) != 4:
    arcpy.AddError("This tool requires exactly 3 parameters.")
    usage = "Usage: {0} path_to_lineFC Offset_Field_Name path_to_outputFC"
    print(usage.format(sys.argv[0]))
    sys.exit(1)

lineFC = arcpy.GetParameterAsText(0)
offsetFN = arcpy.GetParameterAsText(1)
rectFC = arcpy.GetParameterAsText(2)

lineDescription = arcpy.Describe(lineFC)

if lineDescription.shapeType != "Polyline":
    msg = "{0} is a {1} not Polyline feature class."
    arcpy.AddError(msg.format(lineFC, lineDescription.shapeType))
    sys.exit(1)

offsetFieldType = ""
# check for offsetFN in the field names
for field in lineDescription.fields:
    if field.name == offsetFN:
        offsetFieldType = field.type
        break

# check for offsetFN in the field alias names
if offsetFieldType == "":
    for field in lineDescription.fields:
        if field.aliasName == offsetFN:
            offsetFieldType = field.type
            break

if offsetFieldType == "":
    msg = "{0} was not found as a field in {1}."
    arcpy.AddError(msg.format(offsetFN, lineFC))
    sys.exit(1)

if (
    offsetFieldType != "SmallInteger"
    and offsetFieldType != "Integer"
    and offsetFieldType != "Single"
    and offsetFieldType != "Double"
):
    msg = "{0}({1}) is not a numeric data type."
    arcpy.AddError(msg.format(offsetFN, offsetFieldType))
    sys.exit(1)

arcpy.AddMessage("Input has been validated")

# start the real work
workspace, featureClass = os.path.split(rectFC)
arcpy.CreateFeatureclass_management(
    workspace,
    featureClass,
    "Polygon",
    lineFC,
    "SAME_AS_TEMPLATE",
    "SAME_AS_TEMPLATE",
    lineFC,
)

arcpy.AddMessage("Empty feature class has been created")

# workaround for bug (#NIM064306)
# wherein ValidateFieldName(field,workspace\feature_dataset)
# returns incorrect results.  Workaround: remove the feature_dataset
workspace = workspace.lower()
if workspace.rfind(".mdb") > 0:
    workspace = workspace[: workspace.rfind(".mdb") + 4]
else:
    if workspace.rfind(".gdb") > 0:
        workspace = workspace[: workspace.rfind(".gdb") + 4]

# create a simple field mapping from input to output
# Need to be a lists, dicts do not have a guaranteed ordering
line_fields = ["SHAPE@", offsetFN]
rect_fields = ["SHAPE@", arcpy.ValidateFieldName(offsetFN, workspace)]
for field in arcpy.ListFields(lineFC):
    name = field.name
    if (
        field.type not in ["OID", "GlobalID", "Geometry", "Blob", "Raster"]
        and name != offsetFN
        and field.editable # skip un-editable fields like Shape_Length
    ):
        line_fields.append(name)
        rect_fields.append(arcpy.ValidateFieldName(name, workspace))

rect_cursor = arcpy.da.InsertCursor(rectFC, rect_fields)
with arcpy.da.SearchCursor(lineFC, line_fields) as line_cursor:
    for row in line_cursor:
        shape = row[0]
        offset = row[1]
        if shape:
            rect = MakeRectFromLine(shape, offset)
            if rect:
                rect_row = [rect, offset] + row[2:]
                rect_cursor.insertRow(rect_row)
del rect_cursor

arcpy.AddMessage("Output feature class has been populated")
