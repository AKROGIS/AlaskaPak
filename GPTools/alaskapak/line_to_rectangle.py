# -*- coding: utf-8 -*-
"""
Create rectangular polygons from a single line and offset.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import math
import os
import sys

import arcpy


def make_rect(pt1, pt2, width):
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


def make_rect_from_line(line, width):
    """Assumes an arcpy.Polyline for input, and returns an
    arcpy.Polygon or None.  If the input is multipart, so is output.
    Any degenerate parts (single vertex, or first == last) are
    ignored.  If all parts are degenerate, None is returned."""
    # skip bad shapes
    if line.partCount == 0:
        return None
    # skip bad width
    if width is None or width == 0:
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
            pt3, pt4 = make_rect(pt1, pt2, width)
            parray.add(arcpy.Array([pt1, pt2, pt3, pt4, pt1]))
        if len(parray) == 0:
            return None
        return arcpy.Polygon(parray)
    else:
        pt1 = line.firstPoint
        pt2 = line.lastPoint
        if pt1.equals(pt2):  # this equals is an arcpy method
            return None
        pt3, pt4 = make_rect(pt1, pt2, width)
        return arcpy.Polygon(arcpy.Array([pt1, pt2, pt3, pt4, pt1]))


def toolbox_validation(args):
    """Exits with an error message if the command line arguments are not valid.

    Provides the same default processing and validation for command line scripts
    that the ArcGIS toolbox framework provides.  It does not do all possible
    validation and error checking.

    Args:
        args (list[text]): A list of commands arguments, Usually obtained
        from the sys.argv or arcpy.GetParameterAsText().  Provide "#" as
        placeholder for an unspecified intermediate argument.

    Returns:
        A list of validated command line parameters.
    """

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
    return [lineFC, rectFC, offsetFN]


def line_to_rectangle(lineFC, rectFC, offsetFN):

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
            and field.editable  # skip un-editable fields like Shape_Length
        ):
            line_fields.append(name)
            rect_fields.append(arcpy.ValidateFieldName(name, workspace))

    rect_cursor = arcpy.da.InsertCursor(rectFC, rect_fields)
    with arcpy.da.SearchCursor(lineFC, line_fields) as line_cursor:
        for row in line_cursor:
            shape = row[0]
            offset = row[1]
            if shape:
                rect = make_rect_from_line(shape, offset)
                if rect:
                    rect_row = [rect, offset] + row[2:]
                    rect_cursor.insertRow(rect_row)
    del rect_cursor

    arcpy.AddMessage("Output feature class has been populated")


def line_to_rectangle_commandline():
    """Parse and validate command line arguments then add area to features."""
    args = [arcpy.GetParameterAsText(i) for i in range(arcpy.GetParameterCount())]
    args = toolbox_validation(args)
    line_to_rectangle(*args)


def line_to_rectangle_testing(args):
    """Specify command line arguments for testing."""
    args = toolbox_validation(args)
    print(args)
    line_to_rectangle(*args)


if __name__ == "__main__":
    # For testing
    # Change `from . import utils` to `import utils` to run as a script
    line_to_rectangle_commandline()
    # args = ["C:/tmp/building.gdb/edges", "C:/tmp/building.gdb/footprint", "offset"]
    # line_to_rectangle_testing(args)
