# -*- coding: utf-8 -*-
"""
Table2Shape.py
Created: 2011-01-20

Title:
Table to Shape

Tags:
point, vertex, list, geometry, polyline, polygon, multi, create, data, convert

Summary:
This tool will create a new feature class from a table of point IDs and a point feature class.

Usage:
Use this tool to build polygons, polylines, or multi-points if you have a point feature class, and a table of vertex ids related to the point feature class.

Parameter 1:
Table
The full name of a data table.  This can be any format understood by ArcGIS (i.e. a CSV text file, a data table in a geodatabase, an Excel spreadsheet, ...).  All attributes in the input table are copied to the output file. The data table must have the column names that match the names of the vertices given in the Vertex_List parameter.  The data type for these columns must be compatible with the data type in the Point_ID parameter.

Parameter 2:
VertexList
This is a semicolon separated list of the attribute (field/column) name for the vertices to use to make this shape.  The vertices are used in the order provided.  If a Polygon shape is requested, the last vertex can be but does not need to be the same as the first vertex.  Two semicolons without a vertex in between (i.e. "pt1;pt2;;pt3;pt4" separate the parts (in a multi-part feature) of a polygon or a polyline. Three or more adjacent semicolons are not allowed.  Double semicolons are treated as a single semicolon for multipoints. The minimum number of vertices is 1 for Multipoint, two for Polyline, and three for Polygon.  If a multipart feature is being created, then each part must have the required number of vertices.
If the parts in a multipart polygon overlap, this will create holes in the polygon (If one part is completely inside another part then it becomes an interior ring instead of a multipart.

Parameter 3:
Points
The full name of the feature class that has the point geometry for the vertices of the output shapes.  This must be a simple point shape (cannot be a multipoint feature class).  All attributes of this feature class are ignored except the shape and the ID column specified by the Point_ID Parameter.  If the points have M or Z values, then the generated shape will have those same values.

Parameter 4:
Point_ID
The name of the attribute (column/field) that contains the ID (name) of the point that is used to reference it in the Shape_Table.  The data type of this attribute must be compatible with the attributes in the Vertex List.

Parameter 5:
Geometry
This determines the shape created by the points.  Valid values are Polygon, Polyline, Multipoint.  Polyline is the default if either "" or "#" is given for this parameter.

Parameter 6:
Output_feature_class
The full name of the feature class to create.  Any existing feature class at that path will not be overwritten, and the script will issue an error if the feature class exists (unless the geoprocessing options are set to overwrite output). The output feature class will have the same spatial reference system as the Point_Features. If the Point_Features has Z or M values then the output will as well, and Z and M values will be preserved. All attributes in the Shape_Table are copied to Output_Features.

Scripting Syntax:
Table2Shape_AlaskaPak (Table, VertexList, Points, Point_ID, Geometry, Output_feature_class)

Example1:
Scripting Example
The following example shows how this script can be used in another python script, or directly in the ArcGIS Python Window.  It assumes that the script has been loaded into a toolbox, and the toolbox has been loaded into the active session of ArcGIS.
 table = r"C:\tmp\facilities.mdb\pipe_segments"
 ptFC = r"C:\tmp\gps_pts.shp"
 outFC = r"C:\tmp\test.gdb\facilities\pipe_cl"
 Table2Shape_AlaskaPak(table, "start;end", ptFC, "id", "Polyline", outFC)

Example2:
Command Line Example
The following example shows how the script can be used from the operating system command line.  It assumes that the current directory is the location of the script, and that the python interpreter is the path.
 C:\tmp> python Table2Shape.py "C:\tmp\facilities.mdb\pipe_segments" start;end C:\tmp\gps_pts.shp id Polyline "C:\tmp\test.gdb\facilities\pipe_cl"

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

import os
import sys

import arcpy

# TODO: fix documentation on vertices (rings are no longer supported)
# TODO: esri bug 1: featureset cannot initialize with in_memory feature class
#            (load does work)
# TODO: esri bug 2: cannot save a feature set to a feature dataset in a FGDB or PGDB

arcpy.Overwriteoutput = 1

# I use one search cursor and cache all the points in a dictionary.
# This avoids creating a search cursor for each point as lines are processed
# Search cursors creation is very expensive, and independent of the # of
# rows returned.  Approx times to create a search cursor is:
# .007s for Shapefile .38s for FGDB, and .89s for PGDB
# iterating the cursor is about the same for all datasets.
def GetPoints(pointFC, pointIdField):
    points = {}
    pointDescription = arcpy.Describe(pointFC)
    pointShapeField = pointDescription.ShapeFieldName
    pointIdFieldDelimited = arcpy.AddFieldDelimiters(pointFC, pointIdField)
    where = "{0} is not null".format(pointIdFieldDelimited)
    spatialRef = ""
    fields = "{0}; {2}".format(pointIdField, pointShapeField)
    sort = ""
    pts = arcpy.SearchCursor(pointFC, where, spatialRef, fields, sort)

    pt = pts.next()
    while pt != None:
        points[pt.getValue(pointIdField)] = pt.shape.getPart()
        pt = pts.next()
    return points


def MakeShape(row, shape, vertices):
    if shape == "multipoint":
        a = arcpy.Array([points[x] for x in map(row.getValue, vertices)])
        if len(a) == 0:
            return None
        return arcpy.Multipoint(a)
    a = arcpy.Array()
    for part in vertices:
        a.add(arcpy.Array([points[x] for x in map(row.getValue, part)]))
    if len(a) == 0:
        return None
    if shape == "polyline":
        return arcpy.Polyline(a)
    if shape == "polygon":
        return arcpy.Polygon(a)
    return None


def RowInfo(row, table):
    dict = {}
    for field in arcpy.ListFields(table):
        dict[field.name] = row.getValue(field.name)
    return dict


# Input field types must be in mapType (defined below).
# All vertex types and point id type must map to the same type,
# i.e. OID and Integer

# Maps the string returned by arcpy.describe.Field.type to the string
# required by arcpy.AddField()
mapType = {
    "SmallInteger": "SHORT",
    "Integer": "LONG",
    "Single": "FLOAT",
    "Double": "DOUBLE",
    "String": "TEXT",
    "Date": "DATE",
    "OID": "LONG",  # Not creatable with AddField() - use caution
    "Geometry": "BLOB",  # Not creatable with AddField() - use caution
    "BLOB": "BLOB",
}

# GET INPUT
if len(sys.argv) != 7:
    # ArcGIS won't call the script without the correct number of parameters,
    # so this is for command line usage
    usage = (
        "Usage: {0} Shape_Table Vertex_List Shape_Type "
        "Point_Features Point_ID Output_Features"
    )
    print(usage.format(sys.argv[0]))
    sys.exit()

table = arcpy.GetParameterAsText(0)
vertexList = arcpy.GetParameterAsText(1)
pointFC = arcpy.GetParameterAsText(2)
pointIdField = arcpy.GetParameterAsText(3)
shapeType = arcpy.GetParameterAsText(4)
outFC = arcpy.GetParameterAsText(5)

# VERIFY INPUT (mostly for command line.  Toolbox does some validation for us)
# verify input files
print()  # start output with a blank line
if not arcpy.Exists(table):
    msg = "Shape_Table ({0}) does not exist."
    arcpy.AddError(msg.format(table))
    sys.exit()
if not arcpy.Exists(pointFC):
    msg = "Point_Features ({0}) does not exist."
    arcpy.AddError(msg.format(pointFC))
    sys.exit()

# verify output shape type:
shape = shapeType.lower()
if shape == "" or shape == "#":
    shape = "polyline"
if shape not in ["polyline", "polygon", "multipoint"]:
    msg = (
        "Shape_Type of '{0}' not understood. Use one of "
        "'Polyline', 'Polygon', 'Multipoint', '#' or ''"
    )
    arcpy.AddError(msg.format(shapeType))
    sys.exit()

# Sanitize the vertex list and check for correct numbers
if ";;;" in vertexList:
    msg = "Vertex_List ({0}) cannot have more than two consecutive semicolons"
    arcpy.AddError(msg.format(vertexList))
    sys.exit()
if shape == "multipoint":
    vertexList = vertexList.replace(";;", ";")

if shape == "polygon":
    parts = vertexList.split(";;")
    vertices = []
    for part in parts:
        vertexs = part.split(";")
        while vertexs.count("") > 0:
            vertexs.remove("")
        if len(vertexs) < 3:
            arcpy.AddError("Polygons must have at least three vertices")
            sys.exit()
        # close the part if not already closed
        if not vertexs[0] == vertexs[-1]:
            vertexs.append(vertexs[0])
        vertices.append(vertexs)

if shape == "polyline":
    parts = vertexList.split(";;")
    vertices = []
    for part in parts:
        vertexs = part.split(";")
        while vertexs.count("") > 0:
            vertexs.remove("")
        if len(vertexs) < 2:
            arcpy.AddError("Polylines must have at least two vertices")
            sys.exit()
        vertices.append(vertexs)

if shape == "multipoint":
    vertices = vertexList.split(";")
    while vertices.count("") > 0:
        vertices.remove("")
    if len(vertices) < 1:
        arcpy.AddError("Multipoints must have at least one vertex")
        sys.exit()

# verify vertex names exist in input table
# ignore the nesting for rings and parts, and put in a set to remove duplicates
vlist = vertexList.replace(";;", ";")
while ";;" in vlist:
    vlist = vlist.replace(";;", ";")
vset = set(vlist.split(";"))
if "" in vset:
    vset.remove("")
vertexFieldType = {}
tableDescription = arcpy.Describe(table)
for field in tableDescription.Fields:
    if field.name in vset:
        vertexFieldType[field.name] = mapType[field.type]
notFound = []
for v in vset:
    if not vertexFieldType.has_key(v):
        notFound.append(v)
if len(notFound) == 1:
    msg = "The following field '{0}' was not found in {1}."
    arcpy.AddError(msg.format(notFound[0], table))
    sys.exit()
if len(notFound) > 1:
    msg = "The following fields {0} were not found in {1}."
    arcpy.AddError(msg.format(notFound, table))
    sys.exit()


pointDescription = arcpy.Describe(pointFC)
if pointDescription.shapeType != "Point":
    msg = "{0} is a {1} not a point feature class."
    arcpy.AddError(msg.format(pointFC, pointDescription.shapeType))
    sys.exit()

pointIdFieldType = ""
for field in pointDescription.Fields:
    if field.name == pointIdField:
        pointIdFieldType = mapType[field.type]
        break

if pointIdFieldType == "":
    msg = "Field '{0}' not found in {1}"
    arcpy.AddError(msg.format(pointIdField, pointFC))
    sys.exit()
for field in vertexFieldType:
    if vertexFieldType[field] != pointIdFieldType:
        arcpy.AddError("Field types do not match. Cannot link points to table.")
        sys.exit()

# check for output workspace
workspace, name = os.path.split(outFC)
if workspace == "":
    workspace = os.getcwd()
    outFC = os.path.join(workspace, outFC)
if not arcpy.Exists(workspace):
    msg = "The destination workspace '{0}' does not exist."
    arcpy.AddError(msg.format(workspace))
    sys.exit()

arcpy.AddMessage("Input validated")

# Create Feature Class...
outSpatialRef = pointDescription.SpatialReference
hasM, hasZ = "DISABLED", "DISABLED"
if pointDescription.hasM:
    hasM = "ENABLED"
if pointDescription.hasZ:
    hasZ = "ENABLED"

# print("in_memory", "tempfc", shape, table, hasM, hasZ, outSpatialRef)

tempFC = arcpy.CreateFeatureclass_management(
    "in_memory", "tempfc", shape, "", hasM, hasZ, outSpatialRef
)

# workaround for bug wherein ValidateFieldName(field,workspace\feature_dataset)
# returns incorrect results.  Fix is to remove the feature_dataset"
workspace = workspace.lower()
if workspace.rfind(".mdb") > 0:
    workspace = workspace[: workspace.rfind(".mdb") + 4]
else:
    if workspace.rfind(".gdb") > 0:
        workspace = workspace[: workspace.rfind(".gdb") + 4]

# create a simple field mapping from input to output
fields = {}
for field in tableDescription.fields:
    name = field.name
    # if (name != tableDescription.shapeFieldName and
    #    name != tableDescription.OIDFieldName and
    #    field.editable): #skip un-editable fields like Shape_Length
    fields[name] = arcpy.ValidateFieldName(name, workspace)
    # AddField_management (in_table, field_name, field_type, {field_precision},
    # {field_scale}, {field_length}, {field_alias}, {field_is_nullable},
    # {field_is_required}, {field_domain})
    arcpy.AddField_management(
        tempFC,
        fields[name],
        field.type,
        field.precision,
        field.scale,
        field.length,
        field.aliasName,
        field.isNullable,
        field.required,
        field.domain,
    )
# print(fields)

arcpy.AddMessage("Reading Points database")

# Put the points in a dictionary, to avoid two search cursors for each line
# assumes Python is more efficient and faster than ArcGIS.  Should be tested.

points = GetPoints(pointFC, pointIdField)
# print(points)

# fromPointIdFieldDelimited = arcpy.AddFieldDelimiters(lineTable, fromPointIdField)
# toPointIdFieldDelimited = arcpy.AddFieldDelimiters(lineTable, toPointIdField)
# where = "{0} is not null and {1} is not null".format(fromPointIdFieldDelimited, toPointIdFieldDelimited)
# spatialRef = ""
# fields = "{0}; {1}; {2}".format(lineIdField, fromPointIdField, toPointIdField)
# fields = ""
# sort = ""

arcpy.AddMessage("Reading table")

# Create the input(search) and output(insert) cursors.
inRows = arcpy.SearchCursor(table)  # , where, spatialRef, fields, sort)
outRows = arcpy.InsertCursor(tempFC)
newRow = None

row = inRows.next()
while row != None:
    try:
        geom = MakeShape(row, shape, vertices)
    except:
        print("exception")
        geom = None
    if geom == None:
        msg = "Unable to create geometry for {0}"
        arcpy.AddWarning(msg.format(RowInfo(row, table)))
    else:
        # Create a new feature in the feature class
        newRow = outRows.newRow()
        for field in fields:
            newRow.setValue(fields[field], row.getValue(field))
        newRow.shape = geom
        outRows.insertRow(newRow)
    row = inRows.next()

# Closes the insert cursor, and release the exclusive lock
if newRow:
    del newRow
del outRows

arcpy.AddMessage("Saving in memory feature class to {0}".format(outFC))
# fs = arcpy.FeatureSet(tempFC)
fs = arcpy.FeatureSet()
fs.load(tempFC)
fs.save(outFC)
arcpy.AddMessage("Done.")
