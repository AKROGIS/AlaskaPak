# -*- coding: utf-8 -*-
"""
Create rectangular polygons from a single line and offset.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import math
import os
import sys

import arcpy

from . import utils


def make_rect(pt1, pt2, width):
    """Assumes pt1 and pt2 are arcpy.Points, and width is numeric.
    Returns a tuple of the next two points in the rectangle.
    Points proceed clockwise for a positive width and
    counterclockwise for a negative width."""

    # pylint: disable=invalid-name

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
    # Line is not a multi-part
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
        usage = "Usage: {0} path_to_line_feature Offset_Field_Name path_to_outputFC"
        print(usage.format(sys.argv[0]))
        sys.exit(1)

    line_feature = args[0]
    offset_field_name = args[1]
    rect_feature = args[2]

    line_description = arcpy.Describe(line_feature)

    if line_description.shapeType != "Polyline":
        msg = "{0} is a {1} not Polyline feature class."
        arcpy.AddError(msg.format(line_feature, line_description.shapeType))
        sys.exit(1)

    offset_field_type = ""
    # check for offset_field_name in the field names
    for field in line_description.fields:
        if field.name == offset_field_name:
            offset_field_type = field.type
            break

    # check for offset_field_name in the field alias names
    if offset_field_type == "":
        for field in line_description.fields:
            if field.aliasName == offset_field_name:
                offset_field_type = field.type
                break

    if offset_field_type == "":
        msg = "{0} was not found as a field in {1}."
        arcpy.AddError(msg.format(offset_field_name, line_feature))
        sys.exit(1)

    if offset_field_type not in ["SmallInteger", "Integer", "Single", "Double"]:
        msg = "{0}({1}) is not a numeric data type."
        arcpy.AddError(msg.format(offset_field_name, offset_field_type))
        sys.exit(1)

    arcpy.AddMessage("Input has been validated")
    return [line_feature, rect_feature, offset_field_name]


def line_to_rectangle(line_feature, rect_feature, offset_field_name):
    """Creates rect_features by adding offset to line_features.

    `rect_feature` will inherit all the attributes of the line it is based on.

    Args:
        line_feature (text): An ArcGIS path to a polyline feature class. The
            shape should be a simple (two vertex) line that will be one side
            of the generated rectangles shape.
        rect_feature (text): An ArcGIS path where the new polygon feature class
            will be saved.
        offset_field_name (text): The name of a numerical field in
            `line_rectangle` that contains the offset for the line opposite
            the shape in `line_rectangle`.  The offset is assumed to be in
            units of the feature class.  A positive number is offset to the
            to the right (looking from first vertex to last).
    """
    # start the real work
    workspace, feature_class = os.path.split(rect_feature)
    arcpy.CreateFeatureclass_management(
        workspace,
        feature_class,
        "Polygon",
        line_feature,
        "SAME_AS_TEMPLATE",
        "SAME_AS_TEMPLATE",
        line_feature,
    )

    arcpy.AddMessage("Empty feature class has been created")

    # create a simple field mapping from input to output
    # Need to be a lists, dicts do not have a guaranteed ordering
    line_fields = ["SHAPE@", offset_field_name]
    rect_fields = ["SHAPE@", utils.valid_field_name(offset_field_name, rect_feature)]
    for field in arcpy.ListFields(line_feature):
        if (
            field.type not in ["OID", "GlobalID", "Geometry", "Blob", "Raster"]
            and field.name != offset_field_name
            and field.editable  # skip un-editable fields like Shape_Length
        ):
            line_fields.append(field.name)
            rect_fields.append(utils.valid_field_name(field.name, rect_feature))

    rect_cursor = arcpy.da.InsertCursor(rect_feature, rect_fields)
    with arcpy.da.SearchCursor(line_feature, line_fields) as line_cursor:
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
