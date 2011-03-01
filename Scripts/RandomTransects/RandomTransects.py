# ------------------------------------------------------------------------------
# ObscurePoints.py
# Created: 2010-08-30 (9.3)
# Updated: 2011-01-31 (10.0)
#
# Title:
# Obscure Points
#
# Tags:
# random, sensitive, offset, hide, buffer, obscure
#
# Summary:
# Creates a new data set from sensitive point data (like cabins and eagle nests), by adding a random offset to each point, so that the new dataset can be shared with the public.
#
# Usage:
# Creates a new data set from sensitive point data (like cabins and eagle nests), by adding a random offset to each point, so that the new dataset can be shared with the public.#
# Parameter 1:
# Sensitive_Points
# The full name of a feature class of sensitive points.
# The input features must be points or multipoints.  However multipoints cannot be used if there are No-Go or Must-Go areas specified.
# The spatial reference should be a projected system. Calculating distances with a geographic system introduces errors.
#
# Parameter 2:
# Obscured_Features
# The name and location of the feature class to create.
# If the feature class already exists. You can only overwrite it if you have set that option in the geoprocessing tab in Tools->Options menu.
# The output coordinate system will be determined by the environment settings. Typically it will default to the same as the input. Click on the Environment... button and then the General Settings tab to check and set the output coordinate system.
# All attributes of the sensitive features will be copied to these output features. If there is sensitive information in these attributes, then that must be removed separately.
#
# Parameter 3:
# Obscured_Feature_Type
# What kind of output is desired. The default is Points.
# Points:
# <image>
# The output will be a point or multipoint feature class to match the input. With multipoint, each of the individual points will be offset as though the feature class was individual points.
# Circles:
# <image>
# The output feature class will be a circle (polygon) centered at the randomly offset location, with the radius of the circle equal to the Maximum Radius for the offset of center. This guarantees that the real point will fall somewhere in the circle.
#
# Parameter 4:
# Minimum_Offset
# The mimimum distance that the obscured point will be from the actual point. The default is zero.
# The measurement units (feet/meters) are the same as the input feature class. If the input is in lat/long (geographic), Then the units are interpreted as meters.
# <image> with caption: Non-zero minimum offset
# <image> with caption: Default (0) minimum offset
#
# Parameter 5:
# Maximum_Offset
# The maximum distance that the obscured point will be from the actual point. The default is 500.
# The measurement units (feet/meters) are the same as the input feature class. If the input is in lat/long (geographic), Then the units are interpreted as meters.
#
# Parameter 6:
# No_Go_Areas
# Areas in which points will not be placed. Typically this will be water bodies, but it could be any polygon areas that would not be a logical location for the obscured points.
# What to do if there is no solution???
#
# Parameter 7:
# Must_Go_Areas
# Areas in which points must be placed. Typically this will be shorelines or park boundaries, but it could be any polygon areas outside of which would not be a logical location for the obscured points.
# What to do if there is no solution???
#
# Scripting Syntax:
# ObscurePoints_AlaskaPak (Sensitive_Points, Obscured_Features, Obscured_Feature_Type, Minimum_Offset, Maximum_Offset, No_Go_Areas, Must_Go_Areas))
#
# Example1:
# Scripting Example
# The following example shows how this script can be used in another python script, or directly in the ArcGIS Python Window.  It assumes that the script has been loaded into a toolbox, and the toolbox has been loaded into the active session of ArcGIS.
#  ptFC = r"C:\tmp\gps_lines.shp"
#  newPtFC = r"C:\tmp\test.gdb\park\bldg"
#  mustgo = r"C:\tmp\park.shp;c:\tmp\shoreline.shp"
#  nogo = r"C:\tmp\lakes.shp;c:\tmp\bldgs.shp"
#  Line2Rect(ptFC, newPtFC, "Circles", 25, 100, nogo, mustgo)
#
# Example2:
# Command Line Example
# The following example shows how the script can be used from the operating system command line.  It assumes that the current directory is the location of the script, and that the python interpeter is the path.
#  C:\tmp> python ObscurePoints.py c:\tmp\nests.shp c:\tmp\newnests.shp Points 0 100 
#
# Credits:
# Regan Sarwas, Alaska Region GIS Team, National Park Service
#
# Limitations:
# Public Domain
#
# Requirements
# arcpy module - requires ArcGIS v10+ and a valid license
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
# ------------------------------------------------------------------------------

# Problems:
#  Source data canot have a CID field

import sys, os
import random, math

def RandomTransects():
    import arcpy
    cleanParams = SanitizeInput(arcpy,
                                arcpy.GetParameterAsText(0),
                                arcpy.GetParameterAsText(1),
                                arcpy.GetParameterAsText(2),
                                arcpy.GetParameterAsText(3),
                                arcpy.GetParameterAsText(4),
                                arcpy.GetParameterAsText(5),
                                arcpy.GetParameterAsText(6))
    polygons, workspace, name, linesPerPoly, minLength, maxLength, maxTrys, allowOverlap = cleanParams

    lines = CreateFeatureClass(arcpy, polygons, workspace, name)
    featureCount = GetFeatureCount(arcpy, polygons)
    arcpy.SetProgressor("step", "Creating Transects...", 0, featureCount, 1)
    
    #polyList = arcpy.CopyFeatures_management(polygons, arcpy.Geometry())
    #for polygon in polyList:
    #    lines = GetLines(arcpy, polygon, linesPerPoly, maxTrys,
    #             minLength, maxLength, allowOverlap, None)
    #print lines
    #sys.exit()
    
    CreateLines(arcpy, polygons, lines, linesPerPoly, maxTrys,
                minLength, maxLength, allowOverlap)
    arcpy.ResetProgressor()



def SanitizeInput(arcpy, inFC, outFC, linesPerPoly, min, max, maxTrys, allowOverlap):
    # validate input feature class
    if inFC in ["","#"]:
        arcpy.AddError("No input feature class specified.")
        sys.exit()
    if not arcpy.Exists(inFC):
        arcpy.AddError("The input feature specified ("+inFC+") does not exist.")
        sys.exit()
    desc = arcpy.Describe(inFC)
    shape = desc.shapeType.lower()
    if shape != 'polygon':
        arcpy.AddError("The input features specified (" + inFC +
                       ") is not a polygons.")
        sys.exit()

    # validate output feature class
    if outFC in ["","#"]:
        arcpy.AddError("No output feature class specified.")
        sys.exit()
    workspace, name = os.path.split(outFC)
    if not arcpy.Exists(workspace):
        arcpy.AddError("The output workspace specified (" + workspace +
                       ") does not exist.")
        sys.exit()
    name = arcpy.ValidateTableName(name,workspace)
    fc = os.path.join(workspace,name)
    if arcpy.Exists(fc):
        if not arcpy.env.overwriteOutput:
            arcpy.AddError("Cannot overwrite existing data at: " + fc)
            sys.exit()
    # no easy way to check that fc is not readonly or locked, so dont

    # validate linesPerPoly
    if linesPerPoly in ["","#"]:
        linesPerPoly = 5
        arcpy.AddMessage("Using a default value of 5 for transects per feature")
    try:
        linesPerPoly = int(linesPerPoly)
    except ValueError:
        arcpy.AddError("The transects per feature (" + linesPerPoly + ") is not a whole number.")
        sys.exit()
    if (linesPerPoly < 0):
        arcpy.AddError("The transects per feature (" + str(linesPerPoly) +
                       ") is not greater than zero.")
        sys.exit()

    # validate maxTrys
    if maxTrys in ["","#"]:
        maxTrys = 100
        arcpy.AddMessage("Using a default value of 100 for number of attempts")
    try:
        maxTrys = int(maxTrys)
    except ValueError:
        arcpy.AddError("The number of attempts (" + maxTrys + ") is not a whole number.")
        sys.exit()
    if (maxTrys < 0):
        arcpy.AddError("The number of attempts (" + str(maxTrys) +
                       ") is not greater than zero.")
        sys.exit()
    
    #validate min/max
    if min in ["","#"]:
        min = 1000.0
        arcpy.AddMessage("Using a default value of 1000.0 for the minimum offset")
    if max in ["","#"]:
        max = 2000.0
        arcpy.AddMessage("Using a default value of 2000.0 for the maximum offset")
    try:
        min = float(min)
    except ValueError:
        arcpy.AddError("The minimum offset (" + min + ") is not a number.")
        sys.exit()
    try:
        max = float(max)
    except ValueError:
        arcpy.AddError("The maximum offset (" + max + ") is not a number.")
        sys.exit()
    if (min < 0):
        arcpy.AddError("The minimum offset specified (" + str(min) +
                       ") is not greater than zero.")
        sys.exit()
    if (max < min):
        arcpy.AddError("The maximum offset specified (" + str(max) +
                       ") is not greater than the minimum offset.")
        sys.exit()
    if (max == 0):
        arcpy.AddError("The maximum offset specified (" + str(max) +
                       ") is not greater than zero.")
        sys.exit()

    # validate allowOverlap
    if allowOverlap in ["","#"]:
        allowOverlap = 100
        arcpy.AddMessage("Using a default value of 100 for number of attempts")
    if allowOverlap == True:
        allowOverlap = True
    else:
        allowOverlap = False
     
    arcpy.AddMessage("Input has been validated.")
    #print inFC, workspace, name, linesPerPoly, min, max, maxTrys, allowOverlap
    return inFC, workspace, name, linesPerPoly, min, max, maxTrys, allowOverlap


def CreateFeatureClass(arcpy, template, workspace, name):
    shape = "Polyline"
    description = arcpy.Describe(template)
    outSpatialRef = description.SpatialReference
    hasM, hasZ = "DISABLED", "DISABLED"
    if description.hasM:
        hasM = "ENABLED"
    if description.hasZ:
        hasZ = "ENABLED"
    return arcpy.CreateFeatureclass_management(workspace, name,
                                                 shape, "", hasM,
                                                 hasZ, outSpatialRef)


def CreateLines(arcpy, polygons, lines, lineGoal, maxAttempts,
                minLength, maxLength, allowOverlap):
    description = arcpy.Describe(polygons)
    sr = description.SpatialReference

    d = arcpy.Describe(lines)
    polyCursor = arcpy.SearchCursor(polygons)
    lineCursor = arcpy.InsertCursor(lines, sr)
    polygon = polyCursor.next()
    newLine = None  #positive assignment so del at end will not fail
    while (polygon):
        #FIXME - make this more informative
        arcpy.SetProgressorLabel("Processing polygon X")
        lines = GetLines(arcpy, polygon.Shape, lineGoal, maxAttempts,
                         minLength, maxLength, allowOverlap, sr)
        for line in lines:
            newLine = lineCursor.newRow()
            newLine.Shape = line
            #newLine.setValue(d.shapeFieldName, line)
            lineCursor.insertRow(newLine)
        arcpy.SetProgressorPosition()
        polygon = polyCursor.next()
        
    del polyCursor, lineCursor
    del polygon, newLine

    
def GetFeatureCount(arcpy, data):
    cursor = arcpy.SearchCursor(data)
    row = cursor.next()
    count = 0
    while (row):
        count = count + 1
        row = cursor.next()
    del cursor, row
    print count
    return count

    
def GetLines(arcpy, polygon, lineGoal, maxAttempts,
             minLength, maxLength, allowOverlap, sr):
    attemptCount = 0
    linesInPoly = []
    
    while (len(linesInPoly) < lineGoal and attemptCount < maxAttempts):
        #print attemptCount
        x,y = GetRandomPointInPolygon(arcpy, polygon)
        #print "got point"
        line = GetRandomLine(arcpy, x, y, minLength, maxLength, sr)
        #print "Got line"
        #print polygon, line
        #Debug(polygon, line, None)
        #t1 = polygon.contains(line)
        #t1 = line.within(polygon)
        #t2 = DoesOverlap(line, linesInPoly)
        #print t1, allowOverlap, t2
        #print polygon.contains(line) and (allowOverlap or not DoesOverlap(line, linesInPoly))
        #sys.exit()
        if (polygon.contains(line) and (allowOverlap or
                                        not DoesOverlap(line, linesInPoly))):
            #print "good line"
            linesInPoly.append(line)
            attemptCount = 0;
        else:
            #print "bad line"
            attemptCount = attemptCount + 1;
    if attemptCount == maxAttempts:
        #FIXME - make warning more useful
        arcpy.AddWarning("Exceeded maximum attempts at finding transects for polygon X.")
    return linesInPoly


def DoesOverlap(myLine, otherLines):
    for line in otherLines:
        if myLine.crosses(line):
            return True
    return False


def GetRandomLine(arcpy, x1, y1, minLength, maxLength, sr):
    length = random.uniform(minLength, maxLength)
    angle = random.uniform(0,2*math.pi)
    x2 = x1 + length* math.cos(angle)
    y2 = y1 + length* math.sin(angle)
    return arcpy.Polyline(arcpy.Array([arcpy.Point(x1,y1),
                                       arcpy.Point(x2,y2)]), sr)

    
def GetRandomPointInPolygon(arcpy, polygon):
    while True:
        x,y = GetRandomPointInEnvelope(polygon.extent)
        if polygon.contains(arcpy.Point(x,y)):
            return (x,y)

        
def GetRandomPointInEnvelope(env):
    x = random.uniform(env.XMin, env.XMax) 
    y = random.uniform(env.YMin, env.YMax)
    return (x,y)

def Debug(poly,line,pt):
    if poly:
        print "Polygon"
        print "   Extents:",poly.extent.XMin, poly.extent.YMin, poly.extent.XMax, poly.extent.YMax
        print "   Parts, Area, Centroid:",poly.partCount, poly.area, poly.centroid
    if line:
        print "Line: from: (" + str(line.firstPoint.X) + "," + str(line.firstPoint.Y)+ ")"
        print "        to: (" + str(line.lastPoint.X) + "," + str(line.lastPoint.Y)+ ")"
    if pt:
        print "Point: (" + str(pt.X) + "," + str(pt.Y)+ ")"

if __name__ == '__main__':
    RandomTransects()


