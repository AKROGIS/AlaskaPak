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

if __name__ == "__main__":
    # for use as a command line script and with old style ArcGIS toolboxes (*.tbx)
    import utils
else:
    # for use as a module and Python toolboxes (*.pyt)
    from . import utils


# Python 2/3 compatible xrange() cabability
# pylint: disable=undefined-variable,redefined-builtin
if sys.version_info[0] < 3:
    range = xrange

# FIXME: WIll fail if the source data has a field called "CID" (created script)
# TODO: Remove/replace ObscurePoints() and SanitizeInput()
# use *_commandline() , *_testing() and toolbox_validation()
# TODO: import utils and use message functions.


def obscure_points(pts, circles, workspace, name, min, max, no_go, must_go):
    """Create points or circles in workspace by obscuring the location of pts"""

    # pylint: disable=too-many-arguments

    new_feature_class = None
    if no_go or must_go:
        # TODO: Check for Advanced Licence; required for both functions.
        if circles:
            new_feature_class = create_limited_circles(pts, min, max, no_go, must_go)
        else:
            new_feature_class = create_limited_points(pts, min, max, no_go, must_go)
    else:
        if circles:
            new_feature_class = create_circles(pts, min, max)
        else:
            new_feature_class = create_points(pts, min, max)
    if new_feature_class:
        arcpy.FeatureClassToFeatureClass_conversion(new_feature_class, workspace, name)
        arcpy.Delete_management(new_feature_class)
        del new_feature_class


def parameter_fixer(args):
    """Validates and transforms the command line arguments for the task.

    1) Converts text values from old style toolbox (*.tbx) parameters (or the
       command line) to the python object arguments expected by the primary task
       of the script, and as provided by the new style toolbox (*.pyt).
    2) Validates the correct number of arguments.
    3) Provides default values for command line options provided as "#"
       or missing from the end of the command line.
    4) Provides additional validation for command line parameters to match the
       validation done by the toolbox interface.  This isn't required when
       called by an old style toolbox, but it isn't possible to tell it is
       called by the toolbox or by the command line.

    Args:
        args (list[text]): A list of commands arguments, Usually obtained
        from the sys.argv or arcpy.GetParameterAsText().  Provide "#" as
        placeholder for an unspecified intermediate argument.

    Returns:
        A list of validated arguments expected by the task being called.
        Exits with an error message if the args cannot be transformed.
    """

    # pylint: disable=too-many-locals,too-many-branches,too-many-statements

    if not len(args) == 7:
        usage = (
            "Usage: {0} sensitive_points obscured_features [output_shape] "
            " [minimum_offset], [maximum_offset], [no_go_areas], [must_go_areas]"
        )
        utils.die(usage.format(sys.argv[0]))

    # FIXME: Handle missing optionals
    (in_features, out_features, type, min, max, no_go, must_go) = args

    # validate input feature class
    if in_features in ["", "#"]:
        arcpy.AddError("No input feature class specified.")
        sys.exit()
    if not arcpy.Exists(in_features):
        msg = "The input feature specified ({0}) does not exist."
        arcpy.AddError(msg.format(in_features))
        sys.exit()
    desc = arcpy.Describe(in_features)
    shape = desc.shapeType.lower()
    if shape not in ["point", "multipoint"]:
        msg = "The input feature specified ({0}) is not a point or multipoint."
        arcpy.AddError(msg.format(in_features))
        sys.exit()
    multi = shape == "multipoint"

    # validate output feature class
    if out_features in ["", "#"]:
        arcpy.AddError("No output feature class specified.")
        sys.exit()
    workspace, name = os.path.split(out_features)
    if not arcpy.Exists(workspace):
        msg = "The output workspace specified ({0}) does not exist."
        arcpy.AddError(msg.format(workspace))
        sys.exit()
    name = arcpy.ValidateTableName(name, workspace)
    feature_class = os.path.join(workspace, name)
    if arcpy.Exists(feature_class):
        if not arcpy.env.overwriteOutput:
            msg = "Cannot overwrite existing data at: {0}"
            arcpy.AddError(msg.format(feature_class))
            sys.exit()
    # no easy way to check that feature_class is not readonly or locked, so don't

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

    # validate no_go
    no_go = no_go.split(";")
    for junk in [";", "#", "", " "]:
        while no_go.count(junk) > 0:
            no_go.remove(junk)
    no_go = list(set(no_go))  # removes redundant feature classes
    removelist = []
    for feature_class in no_go:
        if not arcpy.Exists(feature_class):
            msg = "'No-Go' feature class ({0}) could not be found - skipping."
            arcpy.AddMessage(msg.format(feature_class))
            removelist.append(feature_class)
            continue
        desc = arcpy.Describe(feature_class)
        shape = desc.shapeType.lower()
        if shape not in ["polygon"]:
            msg = "'No-Go' feature class ({0}) is not polygons - skipping."
            arcpy.AddMessage(msg.format(feature_class))
            removelist.append(feature_class)
    for feature_class in removelist:
        no_go.remove(feature_class)

    # validate must_go
    must_go = must_go.split(";")
    for junk in [";", "#", "", " "]:
        while must_go.count(junk) > 0:
            must_go.remove(junk)
    must_go = list(set(must_go))  # removes redundant feature classes
    removelist = []
    for feature_class in must_go:
        if not arcpy.Exists(feature_class):
            msg = "'Must-Go' feature class ({0}) could not be found - skipping."
            arcpy.AddMessage(msg.format(feature_class))
            removelist.append(feature_class)
            continue
        desc = arcpy.Describe(feature_class)
        shape = desc.shapeType.lower()
        if shape not in ["polygon"]:
            msg = "'Must-Go' feature class ({0}) is not polygons - skipping."
            arcpy.AddMessage(msg.format(feature_class))
            removelist.append(feature_class)
    for feature_class in removelist:
        must_go.remove(feature_class)

    if (no_go or must_go) and multi:
        # Not supported because random point in polygon will only put 1
        # point in a multipart polygon
        msg = "Cannot use multipoint input when No-Go or Must-Go areas are specified."
        arcpy.AddError(msg)
        sys.exit()

    arcpy.AddMessage("Input has been validated.")
    # print(in_features, circles, workspace, name, min, max, no_go, must_go)
    return in_features, circles, workspace, name, min, max, no_go, must_go


def create_limited_points(pts, min, max, no_go, must_go):
    """Create randomized points, considering the constraints

    It is very slow to create a random point, then check it against
    a no-go area.  The New strategy is:
    buffer each input point with the max offset
    erase with a buffer of each point with min offset (if not 0)
    erase with each polygon in no go
    if any polygon has area < 0 issue warning
    put 1 random point in this area."""

    allowed = arcpy.Buffer_analysis(pts, "in_memory\\allow", max)
    if min > 0:
        min_buffer = arcpy.Buffer_analysis(pts, "in_memory\\min_buffer", min)
        # Requires advanced (ArcInfo) license
        erase1 = arcpy.Erase_analysis(allowed, min_buffer, "in_memory\\erase1")
        arcpy.Delete_management(allowed)
        arcpy.Delete_management(min_buffer)
        del min_buffer
        allowed = erase1
    index = 0
    for feature_class in no_go:
        new_allowed = arcpy.Erase_analysis(
            allowed, feature_class, "in_memory\\allow{0}".format(index)
        )
        index = index + 1
        arcpy.Delete_management(allowed)
        allowed = new_allowed
    for feature_class in must_go:
        new_allowed = arcpy.Clip_analysis(
            allowed, feature_class, "in_memory\\allow{0}".format(index)
        )
        index = index + 1
        arcpy.Delete_management(allowed)
        allowed = new_allowed

    # requires Advanced (ArcInfo) license or Spatial Analyst or 3d Analyst
    newpts = arcpy.CreateRandomPoints_management(
        "in_memory", "pts", allowed, "", 1, "", "POINT", ""
    )

    # CID is an attribute created by CreateRandomPoints to tie back to source
    desc = arcpy.Describe(allowed)
    arcpy.JoinField_management(newpts, "CID", allowed, desc.OIDFieldName)
    arcpy.DeleteField_management(newpts, "CID")
    arcpy.Delete_management(allowed)
    del allowed
    return newpts


def create_limited_circles(pts, min, max, no_go, must_go):
    """returns a polygon feature class called "in_memory\\circles". The
    caller is responsible for deleting this feature class when they are
    done. See create_points for more information."""
    newpts = create_limited_points(pts, min, max, no_go, must_go)
    circles = arcpy.Buffer_analysis(newpts, "in_memory\\circles", max)
    arcpy.Delete_management(newpts)
    del newpts
    return circles


def create_points(existing, min_offset, max_offset):
    """existing is a point or multipoint feature class
    if a multipoint feature class, the centroid is used as the basis for the new point.
    min = minimum distance of random point from source point in (0,max_offset)
    max_offset = maximum distance of random point from source point in (min,..)
    returns a feature class called "in_memory\temp". The caller
    is responsible for deleting this feature class when they are done."""

    # pylint: disable=invalid-name
    # I like x, y even if they are too short

    newpts = arcpy.FeatureClassToFeatureClass_conversion(existing, "in_memory", "temp")
    with arcpy.da.UpdateCursor(newpts, ["SHAPE@XY"]) as cursor:
        for row in cursor:
            x, y = row[0]
            row[0] = randomize_point(x, y, min_offset, max_offset)
            cursor.updateRow(row)
    return newpts


def create_circles(existing, min_offset, max_offset):
    """returns a polygon feature class called "in_memory\\circles". The
    caller is responsible for deleting this feature class when they are
    done. See create_points for more information."""
    newpts = create_points(existing, min_offset, max_offset)
    circles = arcpy.Buffer_analysis(newpts, "in_memory\\circles", max_offset)
    arcpy.Delete_management(newpts)
    del newpts
    return circles


def randomize_geometry(geom, min_offset, max_offset):
    """returns None, new pointGeometry or new multipoint
    depending on the input geometry.  Each new point is
    between min and max distance away from the input point"""

    # pylint: disable=invalid-name
    # I like x, y even if they are too short

    part_count = geom.partCount
    if part_count == 0:
        return None

    if part_count == 1:
        pnt = geom.getPart(0)
        x, y = randomize_point(pnt.X, pnt.Y, min_offset, max_offset)
        return arcpy.PointGeometry(arcpy.Point(x, y))

    points = arcpy.Array()
    for part_index in range(part_count):
        pnt = geom.getPart(part_index)
        x, y = randomize_point(pnt.X, pnt.Y, min_offset, max_offset)
        points.append(arcpy.Point(x, y))
    return arcpy.Multipoint(points)


def randomize_point(x, y, min_radius, max_radius):
    """Return a coordinate somewhere in the donut surrounding (x,y)"""

    # pylint: disable=invalid-name
    # I like x, y, x2, and y2 even if they are too short

    radius = random.uniform(min_radius, max_radius)
    phi = random.uniform(0, 2 * math.pi)
    x2 = x + radius * math.cos(phi)
    y2 = y + radius * math.sin(phi)
    return (x2, y2)


if __name__ == "__main__":
    # Set command line or simple testing
    # sys.argv[1:] = ["TODO create test case"]
    utils.execute(obscure_points, parameter_fixer)
