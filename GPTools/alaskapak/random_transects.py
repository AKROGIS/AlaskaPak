# -*- coding: utf-8 -*-
"""
RandomTransects.py
Created: 2011-02-28 (10.0)

Title:
Random Transects

Tags:
survey, inventory, animal, tracking, plane, monitoring, line,

Summary:
Creates random survey transects (lines) within a polygon boundary.

Usage:
This tool uses CreateFeature_Management to create a new polyline feature class
(See the help for that tool regarding the environment variables that will
control the feature class creation).  These feature will have no attributes.
the geometry will be simple straight lines that are wholey within the
boundary polygon.

Parameter 1:
Polygon_Boundaries
A polygon layer in ArcMap, or the full path of a polygon feature class with
boundaries for sets of transect lines.

Parameter 2:
New_Transects
The name and location of the feature class to create.
If the feature class already exists. You can only overwrite it if you have set
that option in the geoprocessing tab in Tools->Options menu.
The output coordinate system will be determined by the environment settings.
Typically it will default to the same as the input. Click on the
Environment... button and then the General Settings tab to check and set the
output coordinate system.  The output coordinate system must be projected
or the length of the line will be undefined.
No attributes are created form the transect lines.
Transects may be M/Z aware (based on environment), but no M/Z values are
added to the vertices.

Parameter 3:
Transects_per_boundary
The number of transects to try and create for each boundary.
This parameter is optional.  The default value is 5.
This parameter must be greater than zero.

Parameter 4:
Minimum_length
The minimum length of the transect line.
This parameter is optional.  The default value is 1 Meters.
This parameter must be greater than zero and less or equal to Maximum_length.
The distance can include a space and units (surround with quotes).
The units (and spelling) understood are predetermined by ArcTool box.
The DecimalDegrees units cannot be used.  Unknown units are an error.
Not specifing the units defaults to meters.

Parameter 5:
Maximum_length
The maximum length of the transect line.
This parameter is optional.  The default value is 1000 Meters.
This parameter must be greater than or equal to Minimum_length.
See Minimum_length for a discussion of units.
If the length is too large then finding a transect that fits within the
boundary may not by possible.

Parameter 6:
Maximum_Attempts
Since it may be impossible to find as many transects as requested, the tool
will stop looking after Maximum_Attempts have failed to find a transect.
The larger this number, the longer the program will take to run.
Increasing this number helps find all the transects requested, but does not
guarantee success, as the input conditions may be impossible to satisfy.
This parameter is optional.  The default value is 100.

Parameter 7:
Allow_Overlap
If transects can overlap one another, then specify True. To ensure that
no transects cross each other, specify False.
This parameter is optional.  The default value is True.

Environment:
 same as arcpy.CreateFeatureclass_management()

Scripting Syntax:
RandomTransects_AlaskaPak (Polygon_Boundaries, New_Transects,
   Transects_per_boundary, Minimum_length, Maximum_length,
   Maximum_Attempts, Allow_Overlap)

Example1:
Scripting Example
The following example shows how this script can be used in another python
script, or directly in the ArcGIS Python Window.  It assumes that the script
has been loaded into a toolbox, and the toolbox has been loaded into the
active session of ArcGIS.
 polyFC = r"C:\tmp\game_units.shp"
 lineFC = r"C:\tmp\test.gdb\park\transects"
 # Create 2 transects less than 500 feet long for each game unit.
 RandomTransects_AlaskaPak (polyFC, lineFC, 2, #, "500 Feet", 10, False)

Example2:
Command Line Example
The following example shows how the script can be used from the operating
system command line.  It assumes that the current directory is the location
of the script, and that the python interpreter is the path.
It will try to create 10 100 meter transects in each polygon in polys.shp
 C:\tmp> python ObscurePoints.py polys.shp c:\tmp\lines.shp 10 100 100

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
import random
import sys

import arcpy

# FIXME - use environment SR, Z, M, when creating feature class


def RandomTransects():
    cleanParams = SanitizeInput(
        arcpy.GetParameterAsText(0),
        arcpy.GetParameterAsText(1),
        arcpy.GetParameterAsText(2),
        arcpy.GetParameterAsText(3),
        arcpy.GetParameterAsText(4),
        arcpy.GetParameterAsText(5),
        arcpy.GetParameterAsText(6),
    )
    (
        polygons,
        workspace,
        name,
        linesPerPoly,
        minLength,
        maxLength,
        maxTrys,
        allowOverlap,
    ) = cleanParams

    lines = CreateFeatureClass(polygons, workspace, name)
    featureCount = GetFeatureCount(polygons)
    arcpy.SetProgressor("step", "Creating Transects...", 0, featureCount, 1)
    CreateLines(
        polygons, lines, linesPerPoly, maxTrys, minLength, maxLength, allowOverlap
    )
    arcpy.ResetProgressor()


def SanitizeInput(inFC, outFC, linesPerPoly, min, max, maxTrys, allowOverlap):
    # validate input feature class
    if inFC in ["", "#"]:
        arcpy.AddError("No input feature class specified.")
        sys.exit()
    if not arcpy.Exists(inFC):
        arcpy.AddError("The input feature specified (" + inFC + ") does not exist.")
        sys.exit()
    desc = arcpy.Describe(inFC)
    shape = desc.shapeType.lower()
    if shape != "polygon":
        msg = "The input features specified ({0}) is not a polygons."
        arcpy.AddError(msg.format(inFC))
        sys.exit()

    # validate output feature class
    if outFC in ["", "#"]:
        arcpy.AddError("No output feature class specified.")
        sys.exit()
    workspace, name = os.path.split(outFC)
    if not arcpy.Exists(workspace):
        msg = "The output workspace specified ({0}) does not exist."
        arcpy.AddError(msg.format(workspace))
        sys.exit()
    name = arcpy.ValidateTableName(name, workspace)
    fc = os.path.join(workspace, name)
    if arcpy.Exists(fc):
        if not arcpy.env.overwriteOutput:
            msg = "Cannot overwrite existing data at: {0}"
            arcpy.AddError(msg.format(fc))
            sys.exit()
    # no easy way to check that fc is not readonly or locked, so don't

    # validate linesPerPoly
    if linesPerPoly in ["", "#"]:
        linesPerPoly = 5
        arcpy.AddMessage("Using a default value of 5 for transects per feature")
    try:
        linesPerPoly = int(linesPerPoly)
    except ValueError:
        msg = "The transects per feature ({0}) is not a whole number."
        arcpy.AddError(msg.format(linesPerPoly))
        sys.exit()
    if linesPerPoly < 0:
        msg = "The transects per feature ({0}) is not greater than zero."
        arcpy.AddError(msg.format(linesPerPoly))
        sys.exit()

    # validate maxTrys
    if maxTrys in ["", "#"]:
        maxTrys = 20
        arcpy.AddMessage("Using a default value of 100 for number of attempts")
    try:
        maxTrys = int(maxTrys)
    except ValueError:
        msg = "The number of attempts ({0}) is not a whole number."
        arcpy.AddError(msg.format(maxTrys))
        sys.exit()
    if maxTrys < 0:
        msg = "The number of attempts ({0}) is not greater than zero."
        arcpy.AddError(msg.format(maxTrys))
        sys.exit()

    # validate min/max
    min_input, max_input = min, max
    if min in ["", "#"]:
        min = "1 Meters"
        arcpy.AddMessage(
            "Using a default value of 1 Meter for the minimum transect length."
        )
    if max in ["", "#"]:
        max = "1000 Meters"
        arcpy.AddMessage(
            "Using a default value of 1000 Meters for the minimum transect length."
        )
    min = LinearUnitsToMeters(min)
    if min == -1:
        msg = "The minimum transect length ({0}) is not a number or the units are invalid."
        arcpy.AddError(msg.format(min_input))
        sys.exit()
    max = LinearUnitsToMeters(max)
    if max == -1:
        msg = "The maximum transect length ({0}) is not a number or the units are invalid."
        arcpy.AddError(msg.format(max_input))
        sys.exit()
    if min <= 0:
        msg = "The minimum transect length specified ({0} Meters) is not greater than zero."
        arcpy.AddError(msg.format(min))
        sys.exit()
    if max < min:
        msg = (
            "The maximum transect length specified ({0} Meters) is not greater "
            "than the minimum transect length ({1} Meters)."
        )
        arcpy.AddError(msg.format(max, min))
        sys.exit()

    # validate allowOverlap
    if allowOverlap in ["", "#"]:
        allowOverlap = "True"
        arcpy.AddMessage("Allowing overlaping transects (by default)")
    if allowOverlap.lower() == "true":
        allowOverlap = True
    else:
        allowOverlap = False

    arcpy.AddMessage("Input has been validated.")
    # print(inFC, workspace, name, linesPerPoly, min, max, maxTrys, allowOverlap)
    return inFC, workspace, name, linesPerPoly, min, max, maxTrys, allowOverlap


def LinearUnitsToMeters(distance):
    """Toolbox parameters can have a linear unit type which translates a real
    number and a pick UOM pick box to a string like '10.3 Meters'.  This
    function will convert the known units to meters.
    Return -1 if there is an error."""
    parts = distance.split()
    # Too many or two few parts
    if len(parts) < 1 or 2 < len(parts):
        return -1
    # first part must be a number, if no second part assume units are meters
    number = parts[0]
    try:
        val = float(number)
    except ValueError:
        val = -1
    if len(parts) == 1:
        return val
    # second part (if given) must be a well known units - these come from toolbox
    units = parts[1]
    units = units.lower()
    if units == "centimeters":
        return val / 100.0
    elif units == "decimaldegrees":
        return -1
    elif units == "decimeters":
        return val / 10.0
    elif units == "feet":  # international
        return val * 12 * 2.54 / 100.0
    elif units == "inches":  # international: 2.54 cm == 1 in
        return val * 2.54 / 100.0
    elif units == "kilometers":
        return val * 1000
    elif units == "meters":
        return val
    elif units == "miles":
        return val * 5280 * 12 * 2.54 / 100.0
    elif units == "millimeters":
        return val / 1000.0
    elif units == "nauticalmiles":
        return val * 1852
    elif units == "points":  # 72 points per inch
        return val * 2.54 / 100.0 / 72
    elif units == "unknown":  # assume meters
        return val
    elif units == "yards":  # international
        return val * 3 * 12 * 2.54 / 100.0
    else:
        return -1


def CreateFeatureClass(template, workspace, name):
    shape = "Polyline"
    description = arcpy.Describe(template)
    outSpatialRef = description.SpatialReference
    hasM, hasZ = "DISABLED", "DISABLED"
    if description.hasM:
        hasM = "ENABLED"
    if description.hasZ:
        hasZ = "ENABLED"
    return arcpy.CreateFeatureclass_management(
        workspace, name, shape, "", hasM, hasZ, outSpatialRef
    )


def CreateLines(
    polygons, lines, lineGoal, maxAttempts, minLength, maxLength, allowOverlap
):
    description = arcpy.Describe(polygons)
    spatialReference = description.SpatialReference
    shapeFieldName = description.shapeFieldName
    oidFieldName = description.OIDFieldName

    d = arcpy.Describe(lines)
    polyCursor = arcpy.SearchCursor(polygons)
    lineCursor = arcpy.InsertCursor(lines)
    polygon = polyCursor.next()
    newLine = None  # positive assignment so del at end will not fail
    count = 1
    while polygon:
        oid = polygon.getValue(oidFieldName)
        arcpy.SetProgressorLabel("Processing polygon {0}".format(count))
        shape = polygon.getValue(shapeFieldName)
        name = "{0} = {1}".format(oidFieldName, oid)
        lines = GetLines(
            name,
            shape,
            lineGoal,
            maxAttempts,
            minLength,
            maxLength,
            allowOverlap,
            spatialReference,
        )
        for line in lines:
            newLine = lineCursor.newRow()
            newLine.setValue(d.shapeFieldName, line)
            lineCursor.insertRow(newLine)
        arcpy.SetProgressorPosition()
        count = count + 1
        polygon = polyCursor.next()

    del polyCursor, lineCursor
    del polygon, newLine


def GetFeatureCount(data):
    cursor = arcpy.SearchCursor(data)
    row = cursor.next()
    count = 0
    while row:
        count = count + 1
        row = cursor.next()
    del cursor, row
    # print(count)
    return count


def GetLines(
    polygonName,
    polygonShape,
    lineGoal,
    maxAttempts,
    minLength,
    maxLength,
    allowOverlap,
    spatialReference,
):
    attemptCount = 0
    linesInPoly = []

    while len(linesInPoly) < lineGoal and attemptCount < maxAttempts:
        x, y = GetRandomPointInPolygon(polygonShape)
        pt1, pt2 = GetRandomLineEnds(x, y, minLength, maxLength)
        # Spatial compare (i.e. contains) will always fail if the two geometries
        # have different spatial references (including null and not null).
        line = arcpy.Polyline(
            arcpy.Array([arcpy.Point(pt1[0], pt1[1]), arcpy.Point(pt2[0], pt2[1])]),
            spatialReference,
        )
        if polygonShape.contains(line) and (
            allowOverlap or not DoesOverlap(line, linesInPoly)
        ):
            linesInPoly.append(line)
            attemptCount = 0
        else:
            attemptCount = attemptCount + 1
    if attemptCount == maxAttempts:
        if len(linesInPoly) == 0:
            msg = (
                "No transect could be created for polygon {0}. Try reducing the length."
            )
            arcpy.AddWarning(msg.format(polygonName))
        else:
            msg = "Polygon {0} exceeded maximum attempts at finding all transects."
            arcpy.AddWarning(msg.format(polygonName))
            msg = "   Try increasing the number of attempts, or reducing the transect length."
            arcpy.AddWarning(msg)
    return linesInPoly


def DoesOverlap(myLine, otherLines):
    for line in otherLines:
        if myLine.crosses(line):
            return True
    return False


def GetRandomLineEnds(x1, y1, minLength, maxLength):
    length = random.uniform(minLength, maxLength)
    angle = random.uniform(0, 2 * math.pi)
    x2 = x1 + length * math.cos(angle)
    y2 = y1 + length * math.sin(angle)
    return ((x1, y1), (x2, y2))


def GetRandomPointInPolygon(polygon):
    while True:
        x, y = GetRandomPointInEnvelope(polygon.extent)
        # do not use a point geometry unless you create it with the
        # same spatial reference as polygon.
        if polygon.contains(arcpy.Point(x, y)):
            return (x, y)


def GetRandomPointInEnvelope(env):
    x = random.uniform(env.XMin, env.XMax)
    y = random.uniform(env.YMin, env.YMax)
    return (x, y)


if __name__ == "__main__":
    RandomTransects()
