# -*- coding: utf-8 -*-
"""
Create polygons from a control point and a set of azimuths and distances.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import math
from numbers import Number
import os

import arcpy

import utils

# FIXME: Merge with or replace polygon_from_point.py


def get_polygon_data(
    polygon_data_table,
    polygon_id_field_name,
    polygon_group_field_name,
    polygon_sort_field_name,
    polygon_azimuth_field_name,
    polygon_distance_field_name,
):
    """Selects and sorts all the records in polygon_data_table.
    Assumes data are small enough that it is faster to query the database once, and do the rest in python.
    Records are sorted by polygon_id_field_name, polygon_group_field_name and then polygon_sort_field_name.
    If there is no polygon_group_field_name then lists of (azimuth,distance) tuples are returned in a dictionary
    keyed on the polygon id (values in the polygon_id_field_name).
    otherwise the lists of (azimuth,distance) tuples are returned in dictionaries keyed on the
    group ids (values in polygon_group_field_name) which is wrapped in a dictionary keyed on the
    polygon ids (values in the polygon_id_field_name).
    """
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
                msg = "Found record with null {0} in polygon table. Skipping".format(
                    polygon_id_field_name
                )
                utils.warn(msg)
                continue
            if not group_id:
                msg = "Found record with null {0} in polygon table. Skipping".format(
                    polygon_group_field_name
                )
                utils.warn(msg)
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
                msg = "Found record with null {0} in polygon table. Skipping".format(
                    polygon_id_field_name
                )
                utils.warn(msg)
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
        msg = "Polygon {0} has only {1:d} pairs of Azimuth/Distance, skipping.".format(
            point_name, len(polygon_data)
        )
        utils.warn(msg)
        return None

    vertices = []
    for azimuth, distance in polygon_data:
        if not isinstance(azimuth, Number) or azimuth < 0 or azimuth > 360:
            msg = "Azimuth {0} for polygon {1} is out of range 0-360.  Skipping".format(
                azimuth, point_name
            )
            utils.warn(msg)
            continue
        if not isinstance(distance, Number) or distance <= 0:
            msg = "Distance {0} for polygon {1} is not a positive number.  Skipping".format(
                distance, point_name
            )
            utils.warn(msg)
            continue
        try:
            x = point[0] + distance * (math.sin(azimuth * math.pi / 180.0))
            y = point[1] + distance * (math.cos(azimuth * math.pi / 180.0))
        except (KeyError, TypeError):
            msg = "Point {0} for polygon {1} is not valid.  Skipping".format(
                point, point_name
            )
            utils.warn(msg)
            continue
        vertices.append(arcpy.Point(x, y))
    if len(vertices) < 3:
        msg = (
            "Polygon {0} has {1:d} pairs of valid Azimuth/Distance.  Skipping.".format(
                point_name, len(vertices)
            )
        )
        utils.warn(msg)
        return None
    vertices.append(vertices[0])
    return arcpy.Polygon(arcpy.Array(vertices))


def polygon_from_control_point(
    point_layer,
    point_id_field_name,
    polygon_data_table,
    polygon_id_field_name,
    polygon_group_field_name,
    polygon_sort_field_name,
    polygon_azimuth_field_name,
    polygon_distance_field_name,
    polygon_feature_class,
):

    workspace, feature_class = os.path.split(polygon_feature_class)
    arcpy.CreateFeatureclass_management(
        workspace, feature_class, "Polygon", "#", "#", "#", point_layer
    )

    utils.info("Empty polygon feature class has been created")

    # Workaround for bug (still in 10.2) wherein
    #   ValidateFieldName(field,workspace\feature_data_set) returns incorrect results.
    # Fix is to remove the feature_data_set"
    workspace = workspace.lower()
    if workspace.rfind(".mdb") > 0:
        workspace = workspace[: workspace.rfind(".mdb") + 4]
    else:
        if workspace.rfind(".gdb") > 0:
            workspace = workspace[: workspace.rfind(".gdb") + 4]

    polygon_fields = arcpy.ListFields(polygon_data_table)
    # Add the polygon_id_field_name to the polygon FC
    polygon_id_new_field_name = arcpy.ValidateFieldName(
        polygon_id_field_name, workspace
    )
    field_type = None
    for field in polygon_fields:
        if field.name == polygon_id_field_name:
            field_type = field.type
            break
    if field_type is None:
        msg = "Id field '{0}' could not be found in polygon data table {1}".format(
            polygon_id_field_name, polygon_data_table
        )
        utils.die(msg)
    arcpy.AddField_management(
        polygon_feature_class, polygon_id_new_field_name, field_type
    )

    # Add the polygon_group_field_name to the polygon FC
    polygon_group_new_field_name = None
    if polygon_group_field_name:
        polygon_group_new_field_name = arcpy.ValidateFieldName(
            polygon_group_field_name, workspace
        )
        field_type = None
        for field in polygon_fields:
            if field.name == polygon_group_field_name:
                field_type = field.type
                break
        if field_type is None:
            msg = (
                "Group field '{0}' could not be found in polygon data table {1}".format(
                    polygon_group_field_name, polygon_data_table
                )
            )
            utils.die(msg)
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
                    utils.warn(
                        "No polygon data for point {0}. Skipping.".format(point_id)
                    )
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


if __name__ == "__main__":

    pointLayer = arcpy.GetParameterAsText(0)
    pointIdFieldName = arcpy.GetParameterAsText(1)
    polygonDataTable = arcpy.GetParameterAsText(2)
    polygonIdFieldName = arcpy.GetParameterAsText(3)
    polygonGroupFieldName = arcpy.GetParameterAsText(4)
    polygonSortFieldName = arcpy.GetParameterAsText(5)
    polygonAzimuthFieldName = arcpy.GetParameterAsText(6)
    polygonDistanceFieldName = arcpy.GetParameterAsText(7)
    polygonFeatureClass = arcpy.GetParameterAsText(8)

    test = False
    if test:
        # pointLayer = r"c:\tmp\test.gdb\w2011a0901"
        # pointIdFieldName = "ESRI_OID"
        # polygonDataTable = r"c:\tmp\test.gdb\pdata"
        pointLayer = r"c:\tmp\test.gdb\campsite"
        pointIdFieldName = "Tag_Number"
        polygonDataTable = r"C:\tmp\VariableTransectDataAllYears.xls\all$"
        polygonIdFieldName = "Tag"
        polygonGroupFieldName = "Year"
        polygonSortFieldName = "AutoSort"
        polygonAzimuthFieldName = "A_Calc_T"
        polygonDistanceFieldName = "D"
        polygonFeatureClass = r"c:\tmp\test.gdb\campsites11"

    #
    # Input validation
    #  for command line and IDE usage,
    #  ArcToolbox provides validation before calling script.
    #
    if not polygonFeatureClass:
        utils.die("No output requested. Quitting.")

    if arcpy.Exists(polygonFeatureClass):
        if arcpy.env.overwriteOutput:
            utils.info("Over-writing existing output.")
            arcpy.Delete_management(polygonFeatureClass)
        else:
            utils.die("Output exists, overwrite is not authorized. Quitting.")

    if not pointLayer:
        utils.die("No control point layer was provided. Quitting.")

    if not arcpy.Exists(pointLayer):
        utils.die("Control point layer cannot be found. Quitting.")

    if not polygonDataTable:
        utils.die("No polygon data table was provided. Quitting.")

    if not arcpy.Exists(polygonDataTable):
        utils.die("Polygon data table cannot be found. Quitting.")

    # Consider validating field names (ArcToolbox does this for us, but useful for command line usage).

    #
    # Create polygons
    #
    polygon_from_control_point(
        pointLayer,
        pointIdFieldName,
        polygonDataTable,
        polygonIdFieldName,
        polygonGroupFieldName,
        polygonSortFieldName,
        polygonAzimuthFieldName,
        polygonDistanceFieldName,
        polygonFeatureClass,
    )
