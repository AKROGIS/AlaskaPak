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

def ObscurePoints():
    import arcpy
    cleanParams = SanitizeInput(arcpy,
                                arcpy.GetParameterAsText(0),
                                arcpy.GetParameterAsText(1),
                                arcpy.GetParameterAsText(2),
                                arcpy.GetParameterAsText(3),
                                arcpy.GetParameterAsText(4),
                                arcpy.GetParameterAsText(5),
                                arcpy.GetParameterAsText(6))
    pts, circles, workspace, name, min, max, nogo, mustgo = cleanParams

    newFC = None    
    if nogo or mustgo:
        if circles:
            newFC = CreateLimitedCircles(arcpy, pts, min, max, nogo, mustgo)
        else:
            newFC = CreateLimitedPoints(arcpy, pts, min, max, nogo, mustgo)
    else:
        if circles:
            newFC = CreateCircles(arcpy, pts, min, max)
        else:
            newFC = CreatePoints(arcpy, pts, min, max)
    if newFC:
        arcpy.FeatureClassToFeatureClass_conversion(newFC, workspace, name)
        arcpy.Delete_management(newFC)
        del newFC

def SanitizeInput(arcpy, inFC, outFC, type, min, max, nogo, mustgo):
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
        arcpy.AddError("The output type specified (" + type +
                       ") is not in" + choices + ".")
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

    #validate nogo
    nogo = nogo.split(";")
    for junk in [";","#",""," "]:
        while nogo.count(junk) > 0:
            nogo.remove(junk)
    nogo = list(set(nogo)) #removes redundant feature classes
    removelist = []
    for fc in nogo:
        if not arcpy.Exists(fc):
            arcpy.AddMessage("'No-Go' feature class (" + fc +
                             ") could not be found - skipping.")
            removelist.append(fc)
            continue
        desc = arcpy.Describe(fc)
        shape = desc.shapeType.lower()
        if shape not in ['polygon']:
            arcpy.AddMessage("'No-Go' feature class (" + fc +
                             ") is not polygons - skipping.")
            removelist.append(fc)
    for fc in removelist:
        nogo.remove(fc)

    #validate mustgo
    mustgo = mustgo.split(";")
    for junk in [";","#",""," "]:
        while mustgo.count(junk) > 0:
            mustgo.remove(junk)
    mustgo = list(set(mustgo)) #removes redundant feature classes
    removelist = []
    for fc in mustgo:
        if not arcpy.Exists(fc):
            arcpy.AddMessage("'Must-Go' feature class (" + fc +
                             ") could not be found - skipping.")
            removelist.append(fc)
            continue
        desc = arcpy.Describe(fc)
        shape = desc.shapeType.lower()
        if shape not in ['polygon']:
            arcpy.AddMessage("'Must-Go' feature class (" + fc +
                             ") is not polygons - skipping.")
            removelist.append(fc)
    for fc in removelist:
        mustgo.remove(fc)

    if (nogo or mustgo) and multi:
        # Not supported because random point in polygon will only put 1
        # point in a multipart polygon
        arcpy.AddError("Cannot use multipoint input when No-Go or Must-Go " +
                       " areas are specified.")
        sys.exit()

    arcpy.AddMessage("Input has been validated.")
    #print inFC, circles, workspace, name, min, max, nogo, mustgo
    return inFC, circles, workspace, name, min, max, nogo, mustgo

          
def CreateLimitedPoints(arcpy, pts, min, max, nogo, mustgo):
    #It is very slow to create a random point, then check it against
    #a no-go area.  The New strategy is:
    # buffer each input point with the max offset
    # erase with a buffer of each point with min offset (if not 0)
    # erase with each polygon in no go
    # if any polyogn has area < 0 issue warning
    # put 1 random point in this area.
    allowed = arcpy.Buffer_analysis(pts,"in_memory\\allow",max)
    if min > 0:
        minbuf = arcpy.Buffer_analysis(pts,"in_memory\\minbuf",min)
        erase1 = arcpy.Erase_analysis(allowed, minbuf, "in_memory\\erase1")
        arcpy.Delete_management(allowed)
        arcpy.Delete_management(minbuf)
        del minbuf
        allowed = erase1
    index = 0
    for fc in nogo:
        newAllowed = arcpy.Erase_analysis(allowed, fc,
                                          "in_memory\\allow"+ str(index))
        index = index + 1
        arcpy.Delete_management(allowed)
        allowed = newAllowed
    for fc in mustgo:
        newAllowed = arcpy.Clip_analysis(allowed, fc,
                                         "in_memory\\allow"+ str(index))
        index = index + 1
        arcpy.Delete_management(allowed)
        allowed = newAllowed
        
    newpts = arcpy.CreateRandomPoints_management("in_memory", "pts", allowed, 
                                                 "", 1, "", "POINT", "")

    #CID is an attribute created by CreateRandomPoints to tie back to source
    d = arcpy.Describe(allowed)
    arcpy.JoinField_management (newpts, "CID", allowed, d.OIDFieldName)
    arcpy.DeleteField_management(newpts, "CID")
    arcpy.Delete_management(allowed)
    del allowed
    return newpts
    
def CreateLimitedCircles(arcpy, pts, min, max, nogo, mustgo):
    """returns a polygon feature class called "in_memory\circles". The
    caller is responsible for deleting this feature class when they are
    done. See CreatePoints for more information."""
    newpts = CreateLimitedPoints(arcpy, pts, min, max, nogo, mustgo)
    circles = arcpy.Buffer_analysis(newpts, "in_memory\\circles", max)
    arcpy.Delete_management(newpts)
    del newpts
    return circles

def CreatePoints(arcpy, existing, min, max):
    """existing is a point or multipoint feature class
    min = minimum distance of random point from source point in (0,max)
    max = maximum distance of random point from source point in (min,..)
    returns a feature class called "in_memory\temp". The caller 
    is responsible for deleting this feature class when they are done."""
    newpts = arcpy.FeatureClassToFeatureClass_conversion(existing,
                                                         "in_memory", "temp")
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


