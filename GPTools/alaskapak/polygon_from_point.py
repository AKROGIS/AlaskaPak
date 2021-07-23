# -*- coding: utf-8 -*-
"""
Create polygons from a control point and a set of azimuths and distances.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import math
from numbers import Number
import os
import sys

import arcpy

from . import utils


def get_polygon_data(
    polygon_data_table,
    polygon_id_field_name,
    polygon_group_field_name,
    polygon_sort_field_name,
    polygon_azimuth_field_name,
    polygon_distance_field_name,
):
    """Selects and sorts all the records in polygon_data_table.

    Assumes data are small enough that it is faster to query the database once,
    and do the rest in python. Records are sorted by polygon_id_field_name,
    polygon_group_field_name and then polygon_sort_field_name. If there is no
    polygon_group_field_name then lists of (azimuth,distance) tuples are
    returned in a dictionary keyed on the polygon id (values in the
    polygon_id_field_name). Otherwise the lists of (azimuth,distance) tuples are
    returned in dictionaries keyed on the group ids (values in
    polygon_group_field_name) which is wrapped in a dictionary keyed on the
    polygon ids (values in the polygon_id_field_name).
    """
    # FIXME: Sort could be None
    if polygon_group_field_name:
        fields = [
            polygon_id_field_name,
            polygon_group_field_name,
            polygon_sort_field_name,
            polygon_azimuth_field_name,
            polygon_distance_field_name,
        ]
        data = {}
        previous_point_id = None
        previous_group_id = None
        for row in sorted(arcpy.da.SearchCursor(polygon_data_table, fields)):
            point_id = row[0]
            group_id = row[1]
            azimuth = row[3]
            distance = row[4]
            if not point_id:
                msg = "Found record with null {0} in polygon table. Skipping"
                utils.warn(msg.format(polygon_id_field_name))
                continue
            if not group_id:
                msg = "Found record with null {0} in polygon table. Skipping"
                utils.warn(msg.format(polygon_group_field_name))
                continue
            if point_id != previous_point_id:
                previous_point_id = point_id
                data[point_id] = {}
                previous_group_id = None
            if group_id != previous_group_id:
                previous_group_id = group_id
                data[point_id][group_id] = []
            data[point_id][group_id].append((azimuth, distance))
        return data
    else:
        fields = [
            polygon_id_field_name,
            polygon_sort_field_name,
            polygon_azimuth_field_name,
            polygon_distance_field_name,
        ]
        data = {}
        previous_point_id = None
        for row in sorted(arcpy.da.SearchCursor(polygon_data_table, fields)):
            point_id = row[0]
            azimuth = row[2]
            distance = row[3]
            if not point_id:
                msg = "Found record with null {0} in polygon table. Skipping"
                utils.warn(msg.format(polygon_id_field_name))
                continue
            if point_id != previous_point_id:
                previous_point_id = point_id
                data[point_id] = []
            data[point_id].append((azimuth, distance))
        return data


def make_polygon(point, point_id, group_id, polygon_data):
    """Point must be an (x,y) tuple, where x and y are numbers
    point_id and group_id identify the point for error reporting
    polygon_data is a list of (azimuth,distance) tuples.
    Returns an arcpy.Polygon or None if there was a problem"""

    if group_id:
        point_name = "{0}/{1}".format(point_id, group_id)
    else:
        point_name = "{0}".format(point_id)

    if len(polygon_data) < 3:
        msg = "Polygon {0} has only {1:d} pairs of Azimuth/Distance, skipping."
        utils.warn(msg.format(point_name, len(polygon_data)))
        return None

    vertices = []
    for azimuth, distance in polygon_data:
        if not isinstance(azimuth, Number) or azimuth < 0 or azimuth > 360:
            msg = "Azimuth {0} for polygon {1} is out of range 0-360.  Skipping"
            utils.warn(msg.format(azimuth, point_name))
            continue
        if not isinstance(distance, Number) or distance <= 0:
            msg = "Distance {0} for polygon {1} is not a positive number.  Skipping"
            utils.warn(msg.format(distance, point_name))
            continue
        try:
            pt_x = point[0] + distance * (math.sin(azimuth * math.pi / 180.0))
            pt_y = point[1] + distance * (math.cos(azimuth * math.pi / 180.0))
        except (KeyError, TypeError):
            msg = "Point {0} for polygon {1} is not valid.  Skipping".format(
                point, point_name
            )
            utils.warn(msg)
            continue
        vertices.append(arcpy.Point(pt_x, pt_y))
    if len(vertices) < 3:
        msg = "Polygon {0} has {1:d} pairs of valid Azimuth/Distance.  Skipping."
        utils.warn(msg.format(point_name, len(vertices)))
        return None
    vertices.append(vertices[0])
    return arcpy.Polygon(arcpy.Array(vertices))


def polygon_from_control_point(
    point_layer,
    point_id_field_name,
    polygon_data_table,
    polygon_id_field_name,
    polygon_feature_class,
    polygon_group_field_name=None,
    polygon_sort_field_name=None,
    polygon_azimuth_field_name="Azimuth",
    polygon_distance_field_name="Distance",
):

    workspace, feature_class = os.path.split(polygon_feature_class)
    arcpy.CreateFeatureclass_management(
        workspace, feature_class, "Polygon", "#", "#", "#", point_layer
    )

    utils.info("Empty polygon feature class has been created")

    polygon_fields = arcpy.ListFields(polygon_data_table)
    # Add the polygon_id_field_name to the polygon FC
    polygon_id_new_field_name = utils.valid_field_name(
        polygon_id_field_name, polygon_feature_class
    )
    field_type = None
    for field in polygon_fields:
        if field.name == polygon_id_field_name:
            field_type = field.type
            break
    if field_type is None:
        msg = "Id field '{0}' could not be found in polygon data table {1}"
        utils.die(msg.format(polygon_id_field_name, polygon_data_table))
    arcpy.AddField_management(
        polygon_feature_class, polygon_id_new_field_name, field_type
    )

    # Add the polygon_group_field_name to the polygon FC
    polygon_group_new_field_name = None
    if polygon_group_field_name:
        polygon_group_new_field_name = utils.valid_field_name(
            polygon_group_field_name, polygon_feature_class
        )
        field_type = None
        for field in polygon_fields:
            if field.name == polygon_group_field_name:
                field_type = field.type
                break
        if field_type is None:
            msg = "Group field '{0}' could not be found in polygon data table {1}"
            utils.die(msg.format(polygon_group_field_name, polygon_data_table))
        arcpy.AddField_management(
            polygon_feature_class, polygon_group_new_field_name, field_type
        )

    utils.info("Reading polygon data.")
    all_polygon_data = get_polygon_data(
        polygon_data_table,
        polygon_id_field_name,
        polygon_group_field_name,
        polygon_sort_field_name,
        polygon_azimuth_field_name,
        polygon_distance_field_name,
    )
    if polygon_group_new_field_name:
        polygon_fields = [
            polygon_id_new_field_name,
            polygon_group_new_field_name,
            "SHAPE@",
        ]
    else:
        polygon_fields = [polygon_id_new_field_name, "SHAPE@"]
    point_fields = [point_id_field_name, "SHAPE@XY"]
    utils.info("Creating polygons.")
    with arcpy.da.InsertCursor(polygon_feature_class, polygon_fields) as polygons:
        with arcpy.da.SearchCursor(point_layer, point_fields) as points:
            for point in points:
                point_id = point[0]
                centroid = point[1]
                try:
                    polygon_data = all_polygon_data[point_id]
                except KeyError:
                    msg = "No polygon data for point {0}. Skipping."
                    utils.warn(msg.format(point_id))
                    continue
                # utils.info("Creating polygons for point {0}".format(point_id))
                if polygon_group_new_field_name:
                    for group_id in polygon_data:
                        polygon_shape = make_polygon(
                            centroid, point_id, group_id, polygon_data[group_id]
                        )
                        if polygon_shape:
                            polygons.insertRow([point_id, group_id, polygon_shape])
                else:
                    polygon_shape = make_polygon(centroid, point_id, "", polygon_data)
                    if polygon_shape:
                        polygons.insertRow(point_id, polygon_shape)

    utils.info("Output feature class has been populated")


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

    # pylint: disable=too-many-branches

    arg_count = len(args)
    if arg_count < 5 or arg_count > 9:
        usage = (
            "Usage: {0} point_layer, point_id_field_name, polygon_data_table, "
            "polygon_id_field_name, polygon_feature_class, [polygon_group_field_name], "
            "[polygon_sort_field_name], [polygon_azimuth_field_name], [polygon_distance_field_name]"
        )
        utils.die(usage.format(sys.argv[0]))

    if arg_count < 9:
        polygon_distance_field_name = "#"
    else:
        polygon_distance_field_name = args[8]
    if arg_count < 8:
        polygon_azimuth_field_name = "#"
    else:
        polygon_azimuth_field_name = args[7]
    if arg_count < 7:
        polygon_sort_field_name = "#"
    else:
        polygon_sort_field_name = args[6]
    if arg_count < 6:
        polygon_group_field_name = "#"
    else:
        polygon_group_field_name = args[5]
    point_layer = args[0]
    point_id_field_name = args[1]
    polygon_data_table = args[2]
    polygon_id_field_name = args[3]
    polygon_feature_class = args[4]

    # validate point_layer
    if not arcpy.Exists(point_layer):
        utils.die("Control point layer cannot be found. Quitting.")
    # TODO: test for points

    # validate point_id_field_name
    # TODO: check that field exists and is the correct type

    # validate polygon_data_table
    if not arcpy.Exists(polygon_data_table):
        utils.die("Polygon data table cannot be found. Quitting.")

    # validate polygon_id_field_name
    # TODO: check that field exists and is the correct type

    # validate polygon_feature_class
    if arcpy.Exists(polygon_feature_class):
        if arcpy.env.overwriteOutput:
            utils.info("Over-writing existing output.")
            arcpy.Delete_management(polygon_feature_class)
        else:
            utils.die("Output exists, overwrite is not authorized. Quitting.")

    # validate polygon_group_field_name
    if polygon_group_field_name == "#":
        polygon_group_field_name = None

    # validate polygon_sort_field_name
    if polygon_sort_field_name == "#":
        polygon_sort_field_name = None

    # validate polygon_azimuth_field_name
    if polygon_azimuth_field_name == "#":
        polygon_azimuth_field_name = "Azimuth"
    # TODO: check that field exists and is the correct type

    # validate polygon_distance_field_name
    if polygon_distance_field_name == "#":
        polygon_distance_field_name = "Distance"
    # TODO: check that field exists and is the correct type

    return [
        point_layer,
        point_id_field_name,
        polygon_data_table,
        polygon_id_field_name,
        polygon_feature_class,
        polygon_group_field_name,
        polygon_sort_field_name,
        polygon_azimuth_field_name,
        polygon_distance_field_name,
    ]


def set_test_command_line(args):
    """Set command line or simple testing."""
    sys.argv[1:] = [
        r"c:\tmp\test.gdb\campsite",
        "Tag_Number",
        r"C:\tmp\VariableTransectDataAllYears.xls\all$",
        "Tag",
        r"c:\tmp\test.gdb\campsites11",
        "Year",
        "AutoSort",
        "A_Calc_T",
        "D",
    ]


if __name__ == "__main__":
    # Set command line or simple testing
    # sys.argv[1:] = ["C:/tmp/test.gdb/bldg_edge", "C:/tmp/test.gdb/bldg_footprint"]
    utils.execute(polygon_from_control_point, parameter_fixer)
