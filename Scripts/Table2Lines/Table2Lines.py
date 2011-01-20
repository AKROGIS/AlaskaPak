# ---------------------------------------------------------------------------
# Table2Lines.py
# Created: 2011-01-12
# Author: Regan Sarwas, National Park Service
#
# Builds a line feature class from a line data table and a point feature class
# The line table must have three fields for the line Id, point1 Id, and point2 Id
# The point feature class must be a point (not multi-point) shape type and have a
# field with the point id that matches the type and domain of the point ids in the line table.
# The names of all fields are provided in the input arguments
#
# Usage:
# python Table2Lines.py path_to_line_table Line_ID_Field From_Point_ID_Field To_Point_ID_Field
#                       path_to_point_FC Point_ID_Field output_line_FC
# Example:
# python Table2Lines.py "c:\tmp\lines.csv" "ID" "From" "To" "c:\tmp\pts.shp" "MY_ID" "c:\tmp\lines.shp"
#
# License:
# Public Domain
#
# Disclaimer:
# This software is provide "as is" and the National Park Service gives
# no warranty, expressed or implied, as to the accuracy, reliability,
# or completeness of this software. Although this software has been
# processed successfully on a computer system at the National Park
# Service, no warranty expressed or implied is made regarding the
# functioning of the software on another system or for general or
# scientific purposes, nor shall the act of distribution constitute any
# such warranty. This disclaimer applies both to individual use of the
# software and aggregate use with other software.
# ---------------------------------------------------------------------------

import os, sys
import arcpy

arcpy.Overwriteoutput = 1

# I use one search cursor and cache all the points in a dictionary.
# This avoids creating a search cursor for each point as lines are processed
# Search cursors creation is very expensive, and independent of the # of
# rows returned.  Approx times to create a search cursor is:
# .007s for Shapefile .38s for FGDB, and .89s for PGDB
# iterating the cursor is about the same for all datasets.
def GetPoints(pointFC,pointIdField):
    points = {}
    pointDescription = arcpy.Describe(pointFC)
    pointShapeField = pointDescription.ShapeFieldName
    pointIdFieldDelimited = arcpy.AddFieldDelimiters(pointFC, pointIdField)
    where = pointIdFieldDelimited + " is not null"
    spatialRef = ""
    fields = pointIdField +"; " + pointShapeField
    sort = ""
    pts = arcpy.SearchCursor(pointFC, where, spatialRef, fields, sort)
    
    pt = pts.next()
    while pt != None:
        points[pt.getValue(pointIdField)] = pt.shape.getPart()
        pt = pts.next()
    return points

def MakeLine(pt1, pt2):
    """ pt1 and pt2 should be gp point objects or None """
    if (pt1 == None or pt2 == None):
        return None
    line = arcpy.Polyline(arcpy.Array([pt1,pt2]))
    if (line == None) or (line.firstPoint == None) or (line.lastPoint == None):
        return None
    return line

# Input field types must be in mapType (defined below).
# Point id type in both input data sets must map to the same type, i.e. OID and Integer

# Maps the string returned by arcpy.describe.Field.Type to the string required by arcpy.AddField()
mapType = {"SmallInteger" : "SHORT",
           "Integer" : "LONG",
           "Single" : "FLOAT",
           "Double" : "DOUBLE",
           "String" : "TEXT",
           "Date" : "DATE",
           "OID" : "LONG",      #Not usually creatable with AddField() - use with Caution
           "Geometry" : "BLOB", #Not usually creatable with AddField() - use with Caution
           "BLOB" : "BLOB"}

#GET INPUT
if (len(sys.argv) != 8):
    #ArcGIS won't call the script without the correct number of parameters,
    #so this is for command line usage
    print ("Usage: " + sys.argv[0] + "path_to_line_table Line_ID_Field " +
    "From_Point_ID_Field To_Point_ID_Field path_to_point_FC " +
    "Point_ID_Field output_line_FC")
    sys.exit()
    
lineTable = arcpy.GetParameterAsText(0)
lineIdField = arcpy.GetParameterAsText(1)
fromPointIdField = arcpy.GetParameterAsText(2)
toPointIdField = arcpy.GetParameterAsText(3)
pointFC = arcpy.GetParameterAsText(4)
pointIdField = arcpy.GetParameterAsText(5)
lineFC = arcpy.GetParameterAsText(6)

#VERIFY INPUT (mostly for command line.  Toolbox does some validation for us)
lineIdFieldType = ""
fromPointIdFieldType = ""
toPointIdFieldType = ""
tableDescription = arcpy.Describe(lineTable)
for field in tableDescription.Fields:
    if field.Name == lineIdField:
        lineIdFieldType = mapType[field.Type]
    if field.Name == fromPointIdField:
        fromPointIdFieldType = mapType[field.Type]
    if field.Name == toPointIdField:
        toPointIdFieldType = mapType[field.Type]

if lineIdFieldType == "":
    raise ValueError("Field '" + lineIdField + "' not found in " + lineTable)
if fromPointIdFieldType == "":
    raise ValueError("Field '" + fromPointIdField + "' not found in " + lineTable)
if toPointIdFieldType == "":
    raise ValueError("Field '" + toPointIdField + "' not found in " + lineTable)

pointDescription = arcpy.Describe(pointFC)
if pointDescription.shapeType != "Point":
    raise ValueError(pointFC + " is a " + pointDescription.shapeType +
                     " not a Point Feature Class.")

pointIdFieldType = ""    
for field in pointDescription.Fields:  
    if field.Name == pointIdField:
        pointIdFieldType = mapType[field.Type]
        break

if pointIdFieldType == "":
    raise ValueError("Field '" + pointIdField + "' not found in " + pointFC)
if (pointIdFieldType != fromPointIdFieldType or
    pointIdFieldType != fromPointIdFieldType):
    raise ValueError("Field types do not match - cannot link points to lines.")

arcpy.AddMessage("Input validated")

# Create Feature Class...
outSpatialRef = pointDescription.SpatialReference
outPath, outName = os.path.split(lineFC)
tempFC = "in_memory/tempfc"
fc = arcpy.CreateFeatureclass_management("in_memory", "tempfc", "POLYLINE", "", "DISABLED", "DISABLED", outSpatialRef, "", "0", "0", "0")

arcpy.AddMessage("Created the output feature class")

# Add Fields...
lineIdFieldValid = arcpy.ValidateFieldName(lineIdField,outPath)
arcpy.AddField_management(tempFC, lineIdFieldValid, lineIdFieldType, "", "", "", "", "NON_NULLABLE", "REQUIRED", "")
fromPointIdFieldValid = arcpy.ValidateFieldName(fromPointIdField,outPath)
arcpy.AddField_management(tempFC, fromPointIdFieldValid, fromPointIdFieldType, "", "", "", "", "NON_NULLABLE", "REQUIRED", "")
toPointIdFieldValid = arcpy.ValidateFieldName(toPointIdField,outPath)
arcpy.AddField_management(tempFC, toPointIdFieldValid, toPointIdFieldType, "", "", "", "", "NON_NULLABLE", "REQUIRED", "")

arcpy.AddMessage("Added the fields to the output feature class")

#Put the points in a dictionary, to avoid two search cursors for each line
#assumes Python is more efficient and faster than ArcGIS.  Should be tested.
points = GetPoints(pointFC,pointIdField)
#print points

fromPointIdFieldDelimited = arcpy.AddFieldDelimiters(lineTable, fromPointIdField)
toPointIdFieldDelimited = arcpy.AddFieldDelimiters(lineTable, toPointIdField)
where = fromPointIdFieldDelimited + " is not null and " + toPointIdFieldDelimited + " is not null"
spatialRef = ""
#fields = lineIdField +"; " + fromPointIdField +"; " +toPointIdField
fields = ""
sort = ""
#Create the input(search) and output(insert) cursors.
lines = arcpy.SearchCursor(lineTable, where, spatialRef, fields, sort)
newLines = arcpy.InsertCursor(tempFC)
newLine = None

line = lines.next()
while line != None:
    pt1Id = line.getValue(fromPointIdField)
    pt2Id = line.getValue(toPointIdField)
    #print pt1Id,pt2Id,points[pt1Id],points[pt2Id]
    try:
        lineGeom = MakeLine(points[pt1Id],points[pt2Id])
    except:
        print "exception"
        lineGeom = None
    if lineGeom == None:
        arcpy.AddWarning("Unable to create line " + str(line.getValue(lineIdField)))
    else:
        # Create a new feature in the feature class
        newLine = newLines.newRow()
        newLine.shape = lineGeom
        newLine.setValue(lineIdFieldValid, line.getValue(lineIdField))
        newLine.setValue(fromPointIdFieldValid, pt1Id)
        newLine.setValue(toPointIdFieldValid, pt2Id)
        newLines.insertRow(newLine)
    line = lines.next()
    
#Closes the insert cursor, and releases the exclusive lock
if newLine:
    del newLine
del newLines

print "Copy", tempFC, lineFC
fs = arcpy.FeatureSet()
fs.load(fc)
fs.save(lineFC)
arcpy.AddMessage("Done.")
