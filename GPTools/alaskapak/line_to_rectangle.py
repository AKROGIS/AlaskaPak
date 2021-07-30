# -*- coding: utf-8 -*-
"""
Create rectangular polygons from a single line and offset.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import math
import os
import sys

import arcpy

if __name__ == "__main__":
    # for use as a command line script and with old style ArcGIS toolboxes (*.tbx)
    import utils
else:
    # for use as a module and Python toolboxes (*.pyt)
    # FIXME: the relative import breaks when called by square_building.py
    #        so the python toolbox will now break.
    # from . import utils
    import utils


def make_rect(pt1, pt2, width):
    """Return the two points that complete the rectangle.

    Points proceed clockwise for a positive width and counterclockwise for a
    negative width.

    Args:
        pt1 (arcpy.Point): The first corner of a rectangle
        pt2 (arcpy.Point): The second corner of the rectangle.
        width (Number): The width of the rectangle perpendicular to the
            segment pt1-pt2.

    Returns:
        (arcpy.Point, arcpy.Point): points 3 and 4 in the rectangle.
    """
    # pylint: disable=invalid-name
    # I like x, y, dx, and dy even if they are too short

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
    """Builds a rectangle from `line` that is `width` wide.

    If the input is multipart, so is output. Any degenerate parts (single
    vertex, or first == last) are ignored.  If all parts are degenerate, None
    is returned.

    Args:
        line (arcpy.Polyline): A line defining one side of the rectangle.
            This line is nominally a single part with only two vertices, but
            the more general case is also supported.
        width (Number): The length of the edges connected to the first the last
            vertices and perpendicular to the segment connecting them.

    Returns:
        arcpy.Polygon|None: The rectangle defined by the input or None if the
        input is invalid.
    """
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

    utils.info("Building {0} from {1}.".format(rect_feature, line_feature))

    # workspace may be a feature dataset, that's ok
    workspace, feature_class = os.path.split(rect_feature)
    arcpy.CreateFeatureclass_management(
        workspace,
        feature_class,
        "Polygon",
        line_feature,
        "SAME_AS_TEMPLATE",
        "SAME_AS_TEMPLATE",
        line_feature
    )

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
                    # row is a tuple in arcpy.da
                    rect_row = (rect, offset) + row[2:]
                    rect_cursor.insertRow(rect_row)
    del rect_cursor


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

    arg_count = len(args)
    if arg_count < 3 or arg_count > 3:
        usage = "Usage: {0} line_feature rect_feature offset_field_name"
        utils.die(usage.format(sys.argv[0]))

    line_feature = args[0]
    rect_feature = args[1]
    offset_field_name = args[2]

    line_description = arcpy.Describe(line_feature)

    if line_description.shapeType != "Polyline":
        msg = "{0} is a {1} not Polyline feature class."
        utils.die(msg.format(line_feature, line_description.shapeType))

    offset_field_type = None
    # check for offset_field_name in the field names
    for field in line_description.fields:
        if field.name == offset_field_name:
            offset_field_type = field.type
            break

    # check for offset_field_name in the field alias names
    if offset_field_type is None:
        for field in line_description.fields:
            if field.aliasName == offset_field_name:
                offset_field_name = field.name
                offset_field_type = field.type
                break

    if offset_field_type is None:
        msg = "{0} was not found as a field in {1}."
        utils.die(msg.format(offset_field_name, line_feature))

    if offset_field_type not in ["SmallInteger", "Integer", "Single", "Double"]:
        msg = "{0}({1}) is not a numeric data type."
        utils.die(msg.format(offset_field_name, offset_field_type))

    return [line_feature, rect_feature, offset_field_name]


if __name__ == "__main__":
    # Set command line or simple testing
    # sys.argv[1:] = ["C:/tmp/AkPakTest.gdb/bldg_edge", "C:/tmp/AkPakTestOut.gdb/bldg_foot", "Width_Ft"]
    utils.execute(line_to_rectangle, parameter_fixer)
