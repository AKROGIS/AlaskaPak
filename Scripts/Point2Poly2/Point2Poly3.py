# ------------------------------------------------------------------------------
# Point2Poly3.py
# Created on: 2014-03-7
# Created by: Regan Sarwas, GIS Team, Alaska Region, National Park Service
#             regan_sarwas@nps.gov
#
# Title:
# Polygons From Control Point
#
# Tags:
# Azimuth, Distance, Campsite 
#
# Summary:
# Takes point features and an ordered sets of azimuth/distance measurements to create a polygon feature class
# 
# Usage:
# Provided point features, and a table of related azimuth/distance measurements this tool will create a
# polygon for each point with at least three valid azimuth/distance measurements.
# The entire table of polygon data is read into memory once, which may cause problems for very, very large data sets.
#
# Parameter 1:
# Control_Point_Features
# A point feature class or layer with the control point for polygons. The control point is the basis or origin of the
# azimuth and distance measurements to the perimeter vertices.
# The Control_Point_Features must be in a spatial reference system with linear units (i.e. projected coordinates)
# If a layer is used, then only the points in the current selection set are used.
# If there is a point without matching data in the Azimuth_Distance_Table, then that point will be skipped with a
# warning. Attributes from the Control_Point_Features will NOT be transfered to the Polygon_Features.
#
# Parameter 2:
# Control_Point_Id_Field
# The name of the field in the control points that uniquely identifies each control points.
# The values in this field will be matched with the values in the Table Id field.
#
# Parameter 3:
# Azimuth_Distance_Table
# This can be a data table or a feature class/layer.
# The table contains a collection of azimuth and distance measurements (as described below) for the control points
# If there is azimuth & distance data that does not relate to a control point, it is silently ignored.
# If a control point has no azimuth & distance that point is skipped, and no polygons are created at that point.
# If a control point has only 1 or 2 azimuth & distance records for a given grouping value, then a polygon can not
# be created in that situation, and a warning will be issued.
#
# Parameter 4:
# Polygon_Id_Field
# The name of a field in the Azimuth_Distance_Table that relates the azimuth & distance records to a control point.
# This must be the same data type as the Control_Point_Id_Field in the Control_Point_Features.
#
# Parameter 5:
# Group_Field
# The name of a field in the Azimuth_Distance_Table that groups the azimuth & distance records into distinct
# polygons for a given control point.
# For example, if azimuth & distance measurements are collected on a yearly basis for each control point, then
# The year attribute would be used as the Group_Field.
#
# Parameter 6:
# Sort_Field
# The name of a field in the Azimuth_Distance_Table that sorts the azimuth & distance records in clockwise
# order around the perimeter of the polygon.
#
# Parameter 7:
# Azimuth_Field
# The name of a field in the Azimuth_Distance_Table that contains the azimuth measurements (floating point number)
# Azimuth values are assumed to be in degrees and referenced from the control point to true north.
# True north is zero degrees and azimuth values increase clockwise up to 360 degrees.
# A value less than zero or greater than 360 is considered invalid and is ignored with a warning.
#
# Parameter 8:
# Distance_Field
# The name of a field in the Azimuth_Distance_Table that contains the distance measurements (floating point number)
# Distances are distance measures from the control point to a vertex in the perimeter of the polygon.  Distances are
# assumed to be in the same linear units as the spatial reference of the Control_Point_Features.
# A value less than or equal to zero is ignored with a warning.
#
# Parameter 9:
# Polygon_Features
# The output polygon feature class to be created.
# The polygons will inherit the spatial reference of the Control_Point_Features, but no other attributes.
# The Polygon_Id_Field and Group_Field (if provided) attributes from the Azimuth_Distance_Table will be inherited.
# There may be multiple polygons for each control point which are distinguished by the attributes in the Group_Field.
#
# Scripting Syntax:
# PolygonBuilder (Control_Point_Features, Control_Point_Id_Field, Azimuth_Distance_Table,
# Polygon_Id_Field, Group_Field, Sort_Field, Azimuth_Field, Distance_Field, Polygon_Features)
#
# Credits:
# Regan Sarwas, Alaska Region GIS Team, National Park Service
#
# Limitations:
# Public Domain
#
# Requirements
# arcpy module - requires ArcGIS v10.1 and a valid license
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

import os
import math
from numbers import Number
import arcpy
import utils


def get_polygon_data(polygon_data_table, polygon_id_field_name, polygon_group_field_name,
                     polygon_sort_field_name, polygon_azimuth_field_name, polygon_distance_field_name):
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
        fields = [polygon_id_field_name, polygon_group_field_name, polygon_sort_field_name,
                  polygon_azimuth_field_name, polygon_distance_field_name]
        data = {}
        previous_point_id = None
        previous_group_id = None
        for row in sorted(arcpy.da.SearchCursor(polygon_data_table, fields)):
            point_id = row[0]
            group_id = row[1]
            azimuth = row[3]
            distance = row[4]
            if not point_id:
                msg = "Found record with null {0} in polygon table. Skipping".format(polygon_id_field_name)
                utils.warn(msg)
                continue
            if not group_id:
                msg = "Found record with null {0} in polygon table. Skipping".format(polygon_group_field_name)
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
        fields = [polygon_id_field_name, polygon_sort_field_name,
                  polygon_azimuth_field_name, polygon_distance_field_name]
        data = {}
        previous_point_id = None
        for row in sorted(arcpy.da.SearchCursor(polygon_data_table, fields)):
            point_id = row[0]
            azimuth = row[2]
            distance = row[3]
            if not point_id:
                msg = "Found record with null {0} in polygon table. Skipping".format(polygon_id_field_name)
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
        point_name = str(point_id) + "/" + str(group_id)
    else:
        point_name = str(point_id)

    if len(polygon_data) < 3:
        msg = "Polygon {0} has only {1:d} pairs of Azimuth/Distance, skipping.".format(point_name, len(polygon_data))
        utils.warn(msg)
        return None

    vertices = []
    for azimuth, distance in polygon_data:
        if not isinstance(azimuth, Number) or azimuth < 0 or azimuth > 360:
            msg = "Azimuth {0} for polygon {1} is out of range 0-360.  Skipping".format(str(azimuth), point_name)
            utils.warn(msg)
            continue
        if not isinstance(distance, Number) or distance <= 0:
            msg = "Distance {0} for polygon {1} is not a positive number.  Skipping".format(str(distance), point_name)
            utils.warn(msg)
            continue
        try:
            x = point[0] + distance * (math.sin(azimuth * math.pi / 180.0))
            y = point[1] + distance * (math.cos(azimuth * math.pi / 180.0))
        except (KeyError, TypeError):
            msg = "Point {0} for polygon {1} is not valid.  Skipping".format(str(point), point_name)
            utils.warn(msg)
            continue
        vertices.append(arcpy.Point(x, y))
    if len(vertices) < 3:
        msg = "Polygon {0} has {1:d} pairs of valid Azimuth/Distance.  Skipping.".format(point_name, len(vertices))
        utils.warn(msg)
        return None
    vertices.append(vertices[0])
    return arcpy.Polygon(arcpy.Array(vertices))


def polygon_from_control_point(
        point_layer, point_id_field_name,
        polygon_data_table, polygon_id_field_name, polygon_group_field_name, polygon_sort_field_name,
        polygon_azimuth_field_name, polygon_distance_field_name, polygon_feature_class):

    workspace, feature_class = os.path.split(polygon_feature_class)
    arcpy.CreateFeatureclass_management(
        workspace, feature_class, "Polygon", "#", "#", "#", point_layer)

    utils.info("Empty polygon feature class has been created")

    # Workaround for bug (still in 10.2) wherein
    #   ValidateFieldName(field,workspace\feature_data_set) returns incorrect results.
    # Fix is to remove the feature_data_set"
    workspace = workspace.lower()
    if workspace.rfind(".mdb") > 0:
        workspace = workspace[:workspace.rfind(".mdb") + 4]
    else:
        if workspace.rfind(".gdb") > 0:
            workspace = workspace[:workspace.rfind(".gdb") + 4]

    polygon_fields = arcpy.ListFields(polygon_data_table)
    #Add the polygon_id_field_name to the polygon FC
    polygon_id_new_field_name = arcpy.ValidateFieldName(polygon_id_field_name, workspace)
    field_type = None
    for field in polygon_fields:
        if field.name == polygon_id_field_name:
            field_type = field.type
            break
    if field_type is None:
        msg = "Id field '{0}' could not be found in polygon data table {1}"\
            .format(polygon_id_field_name, polygon_data_table)
        utils.die(msg)
    arcpy.AddField_management(polygon_feature_class, polygon_id_new_field_name, field_type)

    #Add the polygon_group_field_name to the polygon FC
    polygon_group_new_field_name = None
    if polygon_group_field_name:
        polygon_group_new_field_name = arcpy.ValidateFieldName(polygon_group_field_name, workspace)
        field_type = None
        for field in polygon_fields:
            if field.name == polygon_group_field_name:
                field_type = field.type
                break
        if field_type is None:
            msg = "Group field '{0}' could not be found in polygon data table {1}"\
                .format(polygon_group_field_name, polygon_data_table)
            utils.die(msg)
        arcpy.AddField_management(polygon_feature_class, polygon_group_new_field_name, field_type)

    utils.info("Reading polygon data.")
    all_polygon_data = get_polygon_data(polygon_data_table, polygon_id_field_name, polygon_group_field_name,
                                        polygon_sort_field_name, polygon_azimuth_field_name,
                                        polygon_distance_field_name)
    if polygon_group_new_field_name:
        polygon_fields = [polygon_id_new_field_name, polygon_group_new_field_name, "SHAPE@"]
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
                    utils.warn("No polygon data for point {0}. Skipping.".format(str(point_id)))
                    continue
                #utils.info("Creating polygons for point {0}".format(str(point_id)))
                if polygon_group_new_field_name:
                    for group_id in polygon_data:
                        polygon_shape = make_polygon(centroid, point_id, group_id, polygon_data[group_id])
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
        #pointLayer = r"c:\tmp\test.gdb\w2011a0901"
        #pointIdFieldName = "ESRI_OID"
        #polygonDataTable = r"c:\tmp\test.gdb\pdata"
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
        pointLayer, pointIdFieldName,
        polygonDataTable, polygonIdFieldName, polygonGroupFieldName, polygonSortFieldName,
        polygonAzimuthFieldName, polygonDistanceFieldName, polygonFeatureClass)
