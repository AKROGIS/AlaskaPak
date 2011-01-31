# ------------------------------------------------------------------------------
# ObscurePoints.py
# Created: 2010-08-30 (9.3)
# Updated: 2011-01-31 (10.0)
#
# Title:
# Obscure Points
#
# Tags:
# Building, Offset, Width, Height, Square, Polygon
#
# Summary:
# This tool will derive rectangles from lines and associated offsets.
#
# Usage:
# Use this tool to build a polygon feature class containing rectangles derived from a line feature class.  The line feature class must contain an attribute for each feature which provides the perpendicular distance from the line to the far side of the rectangle.
#
# Parameter 1:
# Line_Features
# The full name of a polyline feature class.  Each line defines the base or first side of a generated rectangle. Each line can have 1 or more parts (i.e. it may be a multi-line), and there may be two or more vertices in each part, however only the first and last vertex of each part are used in the output rectangle.  If the line is a multi-part shape, then the rectangle is also a multi-part shape.  If any line (or part) is degenerate (i.e. a single vertex, or first vertex and last vertext are the same) then that line (or line part) is skipped. If all parts in the line are degenerate then no output is created for that line.
#
# Parameter 2:
# Rectangle_Width_Field
# This is the name of an attribute (column/field) in the line feature class which specifies the width of the rectangle. Width may also be known as offset or height.  Specifically It is the distance perpendicular to the line at which the far side of the rectangle is drawn. If the width is positive, the rectangle is drawn on the right side of the line.  If it is negative it is drawn on the left side.  Right and left are from the prespective of the line looking from the first vertex to the last. The width must be a numeric (integer or real) field, and it must be in the same units/coordinate system as the line feature class. The field name can be either an actual field name, or the alias for the field name.  Actual field names are given priority in case of ambiguity.
#
# Parameter 3:
# Rectangle_Features
# The full name of a polygon feature class to create.  Any existing feature class at that path will not be overwritten, and the script will issue an error if the feature class exists (unless the geoprocessing options are set to overwrite output). The output feature class will have the same spatial reference system as the input. If the input feature class has Z or M values then the output will as well, however no Z or M values will be written to the output. All attributes of the line feature class are copied to the output feature class, except Shape, OID, and any non-editable fields (i.e. Shape_Length).
#
# Scripting Syntax:
# Line2Rect(Line_Features, Rectangle_Width_Field, Rectangle_Features)
#
# Example1:
# Scripting Example
# The following example shows how this script can be used in another python script, or directly in the ArcGIS Python Window.  It assumes that the script has been loaded into a toolbox, and the toolbox has been loaded into the active session of ArcGIS.
#  lineFC = r"C:\tmp\gps_lines.shp"
#  rectFC = r"C:\tmp\test.gdb\park\bldg"
#  Line2Rect(lineFC, "width", rectFC)
#
# Example2:
# Command Line Example
# The following example shows how the script can be used from the operating system command line.  It assumes that the current directory is the location of the script, and that the python interpeter is the path.
#  C:\tmp> python Line2Rect.py "c:\tmp\gps_lines.shp" "width" "c:\tmp\test.gdb\park\bldg"
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
#  * None yet.

import sys, os
import random, math

def ObscurePoints():
    import arcpy
    cleanParams = SanitizeInput(arcpy,
                                arcpy.GetParameterAsText(0),
                                arcpy.GetParameterAsText(1),
                                arcpy.GetParameterAsText(2),
                                arcpy.GetParameterAsText(3),
                                arcpy.GetParameterAsText(4),
                                arcpy.GetParameterAsText(5))
    pts, circles, workspace, name, min, max, nogo = cleanParams

    newFC = None    
    if nogo:
        newFC = DoNoGo(arcpy, pts, circles, min, max, nogo)
    else:
        if circles:
            newFC = CreateCircles(arcpy, pts, min, max)
        else:
            newFC = CreatePoints(arcpy, pts, min, max)
    if newFC:
        arcpy.FeatureClassToFeatureClass_conversion(newFC, workspace, name)
        arcpy.Delete_management(newFC)
        del newFC

def SanitizeInput(arcpy, inFC, outFC, type, min, max, nogo):
    # validate input feature class
    if inFC in ["","#"]:
        arcpy.AddError("No input feature class specified.")
        sys.exit()
    if not arcpy.Exists(inFC):
        arcpy.AddError("The input feature specified ("+inFC+") does not exist.")
        sys.exit()
    desc = arcpy.Describe(inFC)
    shape = desc.shapeType.lower()
    if shape not in ['point', 'multipoint']:
        arcpy.AddError("The input feature specified (" + inFC +
                       ") is not a point or multipoint.")
        sys.exit()
    multi = (shape == 'multipoint')

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

    # validate output type
    if type in ["","#"]:
        type = "points"
    choices = ['points', 'circles']
    for potential in choices:
        if potential.startswith(type.lower()):
            type = potential
    if type not in choices:
        arcpy.AddError("The output type specified ("+type+") is not in"+choices+".")
        sys.exit()
    circles = (type == 'circles')
    
    #validate min/max
    if min in ["","#"]:
        min = 0.0
        arcpy.AddMessage("Using a default value of 0.0 for the minimum offset")
    if max in ["","#"]:
        max = 500.0
        arcpy.AddMessage("Using a default value of 100.0 for the maximum offset")
    try:
        min = float(min)
    except ValueError:
        arcpy.AddError("The minimum offset specified ("+min+") is not a number.")
        sys.exit()
    try:
        max = float(max)
    except ValueError:
        arcpy.AddError("The maximum offset specified ("+max+") is not a number.")
        sys.exit()
    if (min < 0):
        arcpy.AddError("The minimum offset specified (" + str(min) + ") is not greater than zero.")
        sys.exit()
    if (max < min):
        arcpy.AddError("The maximum offset specified (" + str(max) + ") is not greater than the minimum offset.")
        sys.exit()
    if (max == 0):
        arcpy.AddError("The maximum offset specified (" + str(max) + ") is not greater than zero.")
        sys.exit()

    #validate nogo
    nogo = nogo.split(";")
    for junk in [";","#",""," "]:
        while nogo.count(junk) > 0:
            nogo.remove(junk)
    nogo = list(set(nogo)) #removes redundant feature classes
    removelist = []
    for fc in nogo:
        if not arcpy.Exists(fc):
            arcpy.AddMessage("'No-Go' feature class ("+fc+") could not be found - skipping.")
            removelist.append(fc)
        desc = arcpy.Describe(fc)
        shape = desc.shapeType.lower()
        if shape not in ['polygon']:
            arcpy.AddMessage("'No-Go' feature class ("+fc+") is not polygons - skipping.")
            removelist.append(fc)
    for fc in removelist:
        nogo.remove(fc)

    if nogo and multi:
        # Not supported because random point in polygon will only put 1 point in a
        # multipart polygon
        arcpy.AddError("Cannot use multipoint input when No-Go areas are specified.")
        sys.exit()

    arcpy.AddMessage("Input has been validated.")
    #print inFC, circles, workspace, name, min, max, nogo
    return inFC, circles, workspace, name, min, max, nogo

          
def DoNoGo(arcpy, pts, multi, circles, min, max, nogo):
    arcpy.AddError("No-Go areas are not supported yet.")
    return None
    #It is very slow to create a random point, then check it against a no-go area
    #New strategy:
    # buffer each input point with the max offset
    # erase with a buffer of each point with min offset (if not 0)
    # erase with each polygon in no go
    # if any polyogn has area < 0 issue warning
    # put 1 random point in this area.
    allowed = arcpy.Buffer_analysis(pts,"in_memory\\allow",max)
    if min > 0:
        minbuf = arcpy.Buffer_analysis(pts,"in_memory\\minbuf",min)
        allowed = arcpy.Erase_analysis(allowed, minbuf, "in_memory\\allow")
        arcpy.Delete_management(minbuf)
        del minbuf
    for fc in nogo:
        allowed = arcpy.Erase_analysis(allowed, fc, "in_memory\\allow")
    pts = arcpy.CreateRandomPoints_management("in_memory", "pts", allowed, "", 1, "", "POINT", "")
    #join allowed to pts
    arcpy.Delete_management(allowed)
    del allowed
    if circles:
        pts = arcpy.Buffer_analysis(newpts, "in_memory\\pts", max)
    return pts
    
def CreatePoints(arcpy, existing, min, max):
    """existing is a point or multipoint feature class
    min = minimum distance of random point from source point in (0,max)
    max = maximum distance of random point from source point in (min,..)
    returns a feature class called "in_memory\temp". The caller 
    is responsible for deleting this feature class when they are done."""
    newpts = arcpy.FeatureClassToFeatureClass_conversion(existing, "in_memory", "temp")
    pts = arcpy.UpdateCursor(newpts)
    pt = pts.next()
    while pt != None:
        pt.shape = RandomizeGeom(arcpy, pt.shape, min, max)
        pts.updateRow(pt)
        pt = pts.next()
    del pt, pts
    return newpts
        
def CreateCircles(arcpy, existing, min, max):
    """returns a polygon feature class called "in_memory\circles". The
    caller is responsible for deleting this feature class when they are
    done. See CreatePoints for more information."""
    newpts = CreatePoints(arcpy, existing, min, max)
    circles = arcpy.Buffer_analysis(newpts, "in_memory\\circles", max)
    arcpy.Delete_management(newpts)
    del newpts
    return circles

def RandomizeGeom(arcpy, geom, min, max):
    """returns None, new pointGeometry or new multipoint
    depending on the input geometry.  Each new point is
    between min and max distance away from the input point"""
    pc = geom.partCount
    if pc == 0:
        return None
    
    if pc == 1:
        pnt = geom.getPart(0)
        x,y = RandomizePoint(pnt.X, pnt.Y, min, max)
        return arcpy.PointGeometry(arcpy.Point(x,y))
        
    a = arcpy.Array()    
    for i in xrange(pc):
        pnt = geom.getPart(i)
        x,y = RandomizePoint(pnt.X, pnt.Y, min, max)
        a.append(arcpy.Point(x,y))
    return arcpy.Multipoint(a)

def RandomizePoint(x,y,r1,r2):
    r = random.uniform(r1,r2)
    phi = random.uniform(0,2*math.pi)
    x2 = x + r*math.cos(phi) 
    y2 = y + r*math.sin(phi)
    return (x2,y2)

if __name__ == '__main__':
    ObscurePoints()


