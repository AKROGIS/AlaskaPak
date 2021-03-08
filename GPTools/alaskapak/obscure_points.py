# -*- coding: utf-8 -*-
"""
Create random circles that contain sensitive points.
"""

from __future__ import absolute_import, division, print_function, unicode_literals


import math
import os
import random
import sys

import arcpy

# Python 2/3 compatible xrange() cabability
# pylint: disable=undefined-variable,redefined-builtin
if sys.version_info[0] < 3:
    range = xrange

# FIXME: Source data cannot have a CID field


def ObscurePoints():
    cleanParams = SanitizeInput(
        arcpy.GetParameterAsText(0),
        arcpy.GetParameterAsText(1),
        arcpy.GetParameterAsText(2),
        arcpy.GetParameterAsText(3),
        arcpy.GetParameterAsText(4),
        arcpy.GetParameterAsText(5),
        arcpy.GetParameterAsText(6),
    )
    pts, circles, workspace, name, min, max, nogo, mustgo = cleanParams

    newFC = None
    if nogo or mustgo:
        # TODO Check for Advanced Licence; required for both functions.
        if circles:
            newFC = CreateLimitedCircles(pts, min, max, nogo, mustgo)
        else:
            newFC = CreateLimitedPoints(pts, min, max, nogo, mustgo)
    else:
        if circles:
            newFC = CreateCircles(pts, min, max)
        else:
            newFC = CreatePoints(pts, min, max)
    if newFC:
        arcpy.FeatureClassToFeatureClass_conversion(newFC, workspace, name)
        arcpy.Delete_management(newFC)
        del newFC


def SanitizeInput(inFC, outFC, type, min, max, nogo, mustgo):
    # validate input feature class
    if inFC in ["", "#"]:
        arcpy.AddError("No input feature class specified.")
        sys.exit()
    if not arcpy.Exists(inFC):
        msg = "The input feature specified ({0}) does not exist."
        arcpy.AddError(msg.format(inFC))
        sys.exit()
    desc = arcpy.Describe(inFC)
    shape = desc.shapeType.lower()
    if shape not in ["point", "multipoint"]:
        msg = "The input feature specified ({0}) is not a point or multipoint."
        arcpy.AddError(msg.format(inFC))
        sys.exit()
    multi = shape == "multipoint"

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

    # validate output type
    if type in ["", "#"]:
        type = "points"
    choices = ["points", "circles"]
    for potential in choices:
        if potential.startswith(type.lower()):
            type = potential
    if type not in choices:
        msg = "The output type specified ({0}) is not in {1}."
        arcpy.AddError(msg.format(type, choices))
        sys.exit()
    circles = type == "circles"

    # validate min/max
    if min in ["", "#"]:
        min = 0.0
        arcpy.AddMessage("Using a default value of 0.0 for the minimum offset")
    if max in ["", "#"]:
        max = 500.0
        arcpy.AddMessage("Using a default value of 100.0 for the maximum offset")
    try:
        min = float(min)
    except ValueError:
        arcpy.AddError("The minimum offset ({0}) is not a number.".format(min))
        sys.exit()
    try:
        max = float(max)
    except ValueError:
        arcpy.AddError("The maximum offset ({0}) is not a number.".format(max))
        sys.exit()
    if min < 0:
        msg = "The minimum offset specified ({0}) is not greater than zero."
        arcpy.AddError(msg.format(min))

        sys.exit()
    if max < min:
        msg = (
            "The maximum offset specified ({0}) is not greater than the minimum offset."
        )
        arcpy.AddError(msg.format(max))
        sys.exit()
    if max == 0:
        msg = "The maximum offset specified ({0}) is not greater than zero."
        arcpy.AddError(msg.format(max))
        sys.exit()

    # validate nogo
    nogo = nogo.split(";")
    for junk in [";", "#", "", " "]:
        while nogo.count(junk) > 0:
            nogo.remove(junk)
    nogo = list(set(nogo))  # removes redundant feature classes
    removelist = []
    for fc in nogo:
        if not arcpy.Exists(fc):
            msg = "'No-Go' feature class ({0}) could not be found - skipping."
            arcpy.AddMessage(msg.format(fc))
            removelist.append(fc)
            continue
        desc = arcpy.Describe(fc)
        shape = desc.shapeType.lower()
        if shape not in ["polygon"]:
            msg = "'No-Go' feature class ({0}) is not polygons - skipping."
            arcpy.AddMessage(msg.format(fc))
            removelist.append(fc)
    for fc in removelist:
        nogo.remove(fc)

    # validate mustgo
    mustgo = mustgo.split(";")
    for junk in [";", "#", "", " "]:
        while mustgo.count(junk) > 0:
            mustgo.remove(junk)
    mustgo = list(set(mustgo))  # removes redundant feature classes
    removelist = []
    for fc in mustgo:
        if not arcpy.Exists(fc):
            msg = "'Must-Go' feature class ({0}) could not be found - skipping."
            arcpy.AddMessage(msg.format(fc))
            removelist.append(fc)
            continue
        desc = arcpy.Describe(fc)
        shape = desc.shapeType.lower()
        if shape not in ["polygon"]:
            msg = "'Must-Go' feature class ({0}) is not polygons - skipping."
            arcpy.AddMessage(msg.format(fc))
            removelist.append(fc)
    for fc in removelist:
        mustgo.remove(fc)

    if (nogo or mustgo) and multi:
        # Not supported because random point in polygon will only put 1
        # point in a multipart polygon
        msg = "Cannot use multipoint input when No-Go or Must-Go areas are specified."
        arcpy.AddError(msg)
        sys.exit()

    arcpy.AddMessage("Input has been validated.")
    # print(inFC, circles, workspace, name, min, max, nogo, mustgo)
    return inFC, circles, workspace, name, min, max, nogo, mustgo


def CreateLimitedPoints(pts, min, max, nogo, mustgo):
    # It is very slow to create a random point, then check it against
    # a no-go area.  The New strategy is:
    # buffer each input point with the max offset
    # erase with a buffer of each point with min offset (if not 0)
    # erase with each polygon in no go
    # if any polygon has area < 0 issue warning
    # put 1 random point in this area.
    allowed = arcpy.Buffer_analysis(pts, "in_memory\\allow", max)
    if min > 0:
        minbuf = arcpy.Buffer_analysis(pts, "in_memory\\minbuf", min)
        # Requires advanced (ArcInfo) license
        erase1 = arcpy.Erase_analysis(allowed, minbuf, "in_memory\\erase1")
        arcpy.Delete_management(allowed)
        arcpy.Delete_management(minbuf)
        del minbuf
        allowed = erase1
    index = 0
    for fc in nogo:
        newAllowed = arcpy.Erase_analysis(
            allowed, fc, "in_memory\\allow{0}".format(index)
        )
        index = index + 1
        arcpy.Delete_management(allowed)
        allowed = newAllowed
    for fc in mustgo:
        newAllowed = arcpy.Clip_analysis(
            allowed, fc, "in_memory\\allow{0}".format(index)
        )
        index = index + 1
        arcpy.Delete_management(allowed)
        allowed = newAllowed

    # requires Advanced (ArcInfo) license or Spatial Analyst or 3d Analyst
    newpts = arcpy.CreateRandomPoints_management(
        "in_memory", "pts", allowed, "", 1, "", "POINT", ""
    )

    # CID is an attribute created by CreateRandomPoints to tie back to source
    d = arcpy.Describe(allowed)
    arcpy.JoinField_management(newpts, "CID", allowed, d.OIDFieldName)
    arcpy.DeleteField_management(newpts, "CID")
    arcpy.Delete_management(allowed)
    del allowed
    return newpts


def CreateLimitedCircles(pts, min, max, nogo, mustgo):
    """returns a polygon feature class called "in_memory\circles". The
    caller is responsible for deleting this feature class when they are
    done. See CreatePoints for more information."""
    newpts = CreateLimitedPoints(pts, min, max, nogo, mustgo)
    circles = arcpy.Buffer_analysis(newpts, "in_memory\\circles", max)
    arcpy.Delete_management(newpts)
    del newpts
    return circles


def CreatePoints(existing, min, max):
    """existing is a point or multipoint feature class
    if a multipoint feature class, the centroid is used as the basis for the new point.
    min = minimum distance of random point from source point in (0,max)
    max = maximum distance of random point from source point in (min,..)
    returns a feature class called "in_memory\temp". The caller
    is responsible for deleting this feature class when they are done."""
    newpts = arcpy.FeatureClassToFeatureClass_conversion(existing, "in_memory", "temp")
    with arcpy.da.UpdateCursor(newpts, ["SHAPE@XY"]) as cursor:
        x, y = row[0]
        row[0] = RandomizePoint(x, y, min, max)
        cursor.updateRow(row)
    return newpts


def CreateCircles(existing, min, max):
    """returns a polygon feature class called "in_memory\circles". The
    caller is responsible for deleting this feature class when they are
    done. See CreatePoints for more information."""
    newpts = CreatePoints(existing, min, max)
    circles = arcpy.Buffer_analysis(newpts, "in_memory\\circles", max)
    arcpy.Delete_management(newpts)
    del newpts
    return circles


def RandomizeGeom(geom, min, max):
    """returns None, new pointGeometry or new multipoint
    depending on the input geometry.  Each new point is
    between min and max distance away from the input point"""
    pc = geom.partCount
    if pc == 0:
        return None

    if pc == 1:
        pnt = geom.getPart(0)
        x, y = RandomizePoint(pnt.X, pnt.Y, min, max)
        return arcpy.PointGeometry(arcpy.Point(x, y))

    a = arcpy.Array()
    for i in range(pc):
        pnt = geom.getPart(i)
        x, y = RandomizePoint(pnt.X, pnt.Y, min, max)
        a.append(arcpy.Point(x, y))
    return arcpy.Multipoint(a)


def RandomizePoint(x, y, r1, r2):
    r = random.uniform(r1, r2)
    phi = random.uniform(0, 2 * math.pi)
    x2 = x + r * math.cos(phi)
    y2 = y + r * math.sin(phi)
    return (x2, y2)


if __name__ == "__main__":
    ObscurePoints()
