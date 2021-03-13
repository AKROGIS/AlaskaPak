# -*- coding: utf-8 -*-
"""
Create random survey transects (lines) within a polygon boundary.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import math
import os
import random
import sys

import arcpy

# FIXME - use environment SR, Z, M, when creating feature class
# TODO: Remove/replace random_transects() and sanitize_input()
# use *_commandline() , *_testing() and toolbox_validation()


def random_transects():
    clean_params = sanitize_input(
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
        lines_per_poly,
        min_length,
        max_length,
        max_tries,
        allow_overlap,
    ) = clean_params

    lines = create_feature_class(polygons, workspace, name)
    feature_count = get_feature_count(polygons)
    arcpy.SetProgressor("step", "Creating Transects...", 0, feature_count, 1)
    create_lines(
        polygons,
        lines,
        lines_per_poly,
        max_tries,
        min_length,
        max_length,
        allow_overlap,
    )
    arcpy.ResetProgressor()


def sanitize_input(
    in_feature_class,
    out_feature_class,
    lines_per_poly,
    min_length,
    max_length,
    max_tries,
    allow_overlap,
):
    # validate input feature class
    if in_feature_class in ["", "#"]:
        arcpy.AddError("No input feature class specified.")
        sys.exit()
    if not arcpy.Exists(in_feature_class):
        arcpy.AddError(
            "The input feature specified (" + in_feature_class + ") does not exist."
        )
        sys.exit()
    desc = arcpy.Describe(in_feature_class)
    shape = desc.shapeType.lower()
    if shape != "polygon":
        msg = "The input features specified ({0}) is not a polygons."
        arcpy.AddError(msg.format(in_feature_class))
        sys.exit()

    # validate output feature class
    if out_feature_class in ["", "#"]:
        arcpy.AddError("No output feature class specified.")
        sys.exit()
    workspace, name = os.path.split(out_feature_class)
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
    # no easy way to check that fc is not readonly or locked, so don't

    # validate lines_per_poly
    if lines_per_poly in ["", "#"]:
        lines_per_poly = 5
        arcpy.AddMessage("Using a default value of 5 for transects per feature")
    try:
        lines_per_poly = int(lines_per_poly)
    except ValueError:
        msg = "The transects per feature ({0}) is not a whole number."
        arcpy.AddError(msg.format(lines_per_poly))
        sys.exit()
    if lines_per_poly < 0:
        msg = "The transects per feature ({0}) is not greater than zero."
        arcpy.AddError(msg.format(lines_per_poly))
        sys.exit()

    # validate max_tries
    if max_tries in ["", "#"]:
        max_tries = 20
        arcpy.AddMessage("Using a default value of 100 for number of attempts")
    try:
        max_tries = int(max_tries)
    except ValueError:
        msg = "The number of attempts ({0}) is not a whole number."
        arcpy.AddError(msg.format(max_tries))
        sys.exit()
    if max_tries < 0:
        msg = "The number of attempts ({0}) is not greater than zero."
        arcpy.AddError(msg.format(max_tries))
        sys.exit()

    # validate min_length/max_length
    min_input, max_input = min_length, max_length
    if min_length in ["", "#"]:
        min_length = "1 Meters"
        arcpy.AddMessage(
            "Using a default value of 1 Meter for the minimum transect length."
        )
    if max_length in ["", "#"]:
        max_length = "1000 Meters"
        arcpy.AddMessage(
            "Using a default value of 1000 Meters for the minimum transect length."
        )
    min_length = linear_units_to_meters(min_length)
    if min_length == -1:
        msg = "The minimum transect length ({0}) is not a number or the units are invalid."
        arcpy.AddError(msg.format(min_input))
        sys.exit()
    max_length = linear_units_to_meters(max_length)
    if max_length == -1:
        msg = "The maximum transect length ({0}) is not a number or the units are invalid."
        arcpy.AddError(msg.format(max_input))
        sys.exit()
    if min_length <= 0:
        msg = "The minimum transect length specified ({0} Meters) is not greater than zero."
        arcpy.AddError(msg.format(min_length))
        sys.exit()
    if max_length < min_length:
        msg = (
            "The maximum transect length specified ({0} Meters) is not greater "
            "than the minimum transect length ({1} Meters)."
        )
        arcpy.AddError(msg.format(max_length, min_length))
        sys.exit()

    # validate allow_overlap
    if allow_overlap in ["", "#"]:
        allow_overlap = "True"
        arcpy.AddMessage("Allowing overlaping transects (by default)")
    if allow_overlap.lower() == "true":
        allow_overlap = True
    else:
        allow_overlap = False

    arcpy.AddMessage("Input has been validated.")
    # print(in_feature_class, workspace, name, lines_per_poly, min_length,
    # max_length, max_tries, allow_overlap)
    return (
        in_feature_class,
        workspace,
        name,
        lines_per_poly,
        min_length,
        max_length,
        max_tries,
        allow_overlap,
    )


def linear_units_to_meters(distance):
    """Toolbox parameters can have a linear unit type which translates a real
    number and a pick UOM pick box to a string like '10.3 Meters'.  This
    function will convert the known units to meters.
    Return -1 if there is an error."""
    parts = distance.split()
    # Too many or two few parts
    if len(parts) < 1 or len(parts) > 2:
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


def create_feature_class(template, workspace, name):
    shape = "Polyline"
    description = arcpy.Describe(template)
    spatial_reference = description.SpatialReference
    has_m, has_z = "DISABLED", "DISABLED"
    if description.hasM:
        has_m = "ENABLED"
    if description.hasZ:
        has_z = "ENABLED"
    return arcpy.CreateFeatureclass_management(
        workspace, name, shape, "", has_m, has_z, spatial_reference
    )


def create_lines(
    polygons, lines, line_goal, max_attempts, min_length, max_length, allow_overlap
):
    spatial_reference = arcpy.Describe(polygons).SpatialReference

    count = 0
    line_fields = ["SHAPE@"]
    poly_fields = ["OID@", "SHAPE@"]
    line_cursor = arcpy.da.InsertCursor(lines, line_fields)
    with arcpy.da.SearchCursor(polygons, poly_fields) as poly_cursor:
        for row in poly_cursor:
            count += 1
            arcpy.SetProgressorLabel("Processing polygon {0}".format(count))
            oid = row[0]
            shape = row[1]
            name = "OBJECTID = {1}".format(oid)
            lines = get_lines(
                name,
                shape,
                line_goal,
                max_attempts,
                min_length,
                max_length,
                allow_overlap,
                spatial_reference,
            )
            for line in lines:
                line_cursor.insertRow([line])
            arcpy.SetProgressorPosition()  # Steps by 1 from 0 to feature count
    del line_cursor


def get_feature_count(data):
    return len(arcpy.da.SearchCursor(data, ["OID@"]))


def get_lines(
    polygon_name,
    polygon_shape,
    line_goal,
    max_attempts,
    min_length,
    max_length,
    allow_overlap,
    spatial_reference,
):
    attempt_count = 0
    lines_in_poly = []

    while len(lines_in_poly) < line_goal and attempt_count < max_attempts:
        x, y = get_random_point_in_polygon(polygon_shape)
        pt1, pt2 = get_random_line_ends(x, y, min_length, max_length)
        # Spatial compare (i.e. contains) will always fail if the two geometries
        # have different spatial references (including null and not null).
        line = arcpy.Polyline(
            arcpy.Array([arcpy.Point(pt1[0], pt1[1]), arcpy.Point(pt2[0], pt2[1])]),
            spatial_reference,
        )
        if polygon_shape.contains(line) and (
            allow_overlap or not is_overlap(line, lines_in_poly)
        ):
            lines_in_poly.append(line)
            attempt_count = 0
        else:
            attempt_count = attempt_count + 1
    if attempt_count == max_attempts:
        if len(lines_in_poly) == 0:
            msg = (
                "No transect could be created for polygon {0}. Try reducing the length."
            )
            arcpy.AddWarning(msg.format(polygon_name))
        else:
            msg = "Polygon {0} exceeded maximum attempts at finding all transects."
            arcpy.AddWarning(msg.format(polygon_name))
            msg = "   Try increasing the number of attempts, or reducing the transect length."
            arcpy.AddWarning(msg)
    return lines_in_poly


def is_overlap(my_line, other_lines):
    for line in other_lines:
        if my_line.crosses(line):
            return True
    return False


def get_random_line_ends(x1, y1, min_length, max_length):
    length = random.uniform(min_length, max_length)
    angle = random.uniform(0, 2 * math.pi)
    x2 = x1 + length * math.cos(angle)
    y2 = y1 + length * math.sin(angle)
    return ((x1, y1), (x2, y2))


def get_random_point_in_polygon(polygon):
    while True:
        x, y = get_random_point_in_envelope(polygon.extent)
        # do not use a point geometry unless you create it with the
        # same spatial reference as polygon.
        if polygon.contains(arcpy.Point(x, y)):
            return (x, y)


def get_random_point_in_envelope(env):
    x = random.uniform(env.XMin, env.XMax)
    y = random.uniform(env.YMin, env.YMax)
    return (x, y)


if __name__ == "__main__":
    random_transects()
