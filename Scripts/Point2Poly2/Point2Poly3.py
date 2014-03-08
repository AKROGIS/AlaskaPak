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
#
# Parameter 1:
# Control_Point_Features
# A point feature class or layer with the control point for polygons. The control point is the basis or origin of the
# azimuth and distance measurements to the perimeter vertices.
# If a layer is used, then only the points in the current selection set are used.
# If there is a point without matching data in the Azimuth/Distance table, then that point will be skipped.
# Attributes from the points will be applied to all polygons generated from that point.
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
# A value less than zero or greater than 360 is considered is ignored with a warning.
#
# Parameter 8:
# Distance_Field
# The name of a field in the Azimuth_Distance_Table that contains the distance measurements (floating point number)
# Distances are assumed to be meters from the control point to the perimeter of the polygon.
# A value less than or equal to zero is ignored with a warning.
#
# Parameter 9:
# Polygon_Features
# The output polygon feature class to be created.
# The polygons will inherit the spatial reference and all attributes of the control points, as well as the data
# in the in the Year_Id_Field of the Azimuth_Distance_Table.
# There may be multiple polygons for each control point which are distinguished by the Year_Id_Field attribute.
#
# Scripting Syntax:
# PolygonBuilder (Control_Point_Features, Control_Point_Id_Field, Azimuth_Distance_Table,
# Fieldname_for_table_Identifier, Identifier_for_table_data, Polygon_Id_Field, Azimuth_Field, Distance_Field,
# Polygon_Features)
#
# Credits:
# Regan Sarwas, Alaska Region GIS Team, National Park Service
#
# Limitations:
# Public Domain
#
# Requirements
# arcpy module - requires ArcGIS v10.2 and a valid license
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

import sys
import os
import math
import arcpy


def parse_polygon_data(
        polygon_data_table, polygon_id_field_name,
        polygon_azimuth_field_name, polygon_distance_field_name):
    """ Returns a dictionary where key is the point/polygon id, and
    the value is an ordered list of (azimuth/distance) tuples"""
    result = {}
    current_id = None
    rows = arcpy.SearchCursor(polygon_data_table)
    current_list = []
    for row in rows:
        polygon_id = row.getValue(polygon_id_field_name)
        # We are done if we find a null id
        if polygon_id is None:
            break
            # If we have seen this id before, then skip this row
        if polygon_id in result:
            msg = u"Polygon {0:d} has already been closed, skipping.".format(polygon_id)
            print("Warning: " + msg)
            arcpy.AddWarning(msg)
            continue
            # we have a new id, and an old id
        if polygon_id != current_id:
            #save the old list
            if current_id and current_list:
                result[current_id] = current_list
                # start a new list
            current_list = []
            current_id = polygon_id
            #add the point to the current list
        current_list.append(
            (row.getValue(polygon_azimuth_field_name),
             row.getValue(polygon_distance_field_name)))
        # save any open lists
    if current_id and current_list:
        result[current_id] = current_list
    return result


def make_polygon(point, point_id, group_id, polygon_data):
    """point must be an arcpy.Point,
    point_id, group_id are keys to the dictionaries in polygon_data
    polygon_data is a dictionary with keys in type of point_id and values of dictionary with keys in type of group_id
    and values of list of (azimuth,distance) tuples (both floats).
    Returns an arcpy.Polygon or None if there was a problem"""
    try:
        data = polygon_data[point_id][group_id]
    except KeyError:
        return None

    if group_id:
        point_name = str(point_id) + "/" + str(group_id)
    else:
        point_name = str(point_id)

    if len(data) < 3:
        msg = "Polygon {0} has only {1:d} pairs of Azimuth/Distance, skipping.".format(point_name, len(data))
        print("Warning: " + msg)
        arcpy.AddWarning(msg)
        return None

    vertices = []
    for azimuth, distance in data:
        if azimuth < 0 or azimuth > 360:
            if azimuth is None:
                msg = u"An azimuth is null for polygon {0}.  Skipping".format(point_name)
            else:
                msg = "Azimuth {0:3.2f} for polygon {1} is out of range 0-360.  Skipping".format(azimuth, point_name)
            print("Warning: " + msg)
            arcpy.AddWarning(msg)
            continue
        if distance <= 0:
            if distance is None:
                msg = u"A distance is null for polygon {0:d}.  Skipping".format(point_name)
            else:
                msg = "Distance {0:3.2f} for polygon {1} is out of range d <= 0.  Skipping".format(distance, point_name)
            print("Warning: " + msg)
            arcpy.AddWarning(msg)
            continue

        x = point.getPart().X + distance * (math.sin(azimuth * math.pi / 180))
        y = point.getPart().Y + distance * (math.cos(azimuth * math.pi / 180))
        vertices.append(arcpy.Point(x, y))
    if len(vertices) < 3:
        msg = "Polygon {0} has {1:d} pairs of valid Azimuth/Distance.  Skipping.".format(point_name, len(vertices))
        print("Warning: " + msg)
        arcpy.AddWarning(msg)
        return None
    vertices.append(vertices[0])
    return arcpy.Polygon(arcpy.Array(vertices))


def polygon_from_control_point(
        point_layer, point_id_field_name,
        polygon_data_table, polygon_id_field_name, polygon_group_field_name, polygon_sort_field_name,
        polygon_azimuth_field_name, polygon_distance_field_name, polygon_feature_class):

    workspace, feature_class = os.path.split(polygon_feature_class)
    arcpy.CreateFeatureclass_management(
        workspace, feature_class, "Polygon", point_layer, "SAME_AS_TEMPLATE",
        "SAME_AS_TEMPLATE", point_layer)

    arcpy.AddMessage("Empty polygon feature class has been created")

    # workaround for bug wherein
    # ValidateFieldName(field,workspace\feature_dataset)
    # returns incorrect results.  Fix is to remove the feature_dataset"
    workspace = workspace.lower()
    if workspace.rfind(".mdb") > 0:
        workspace = workspace[:workspace.rfind(".mdb") + 4]
    else:
        if workspace.rfind(".gdb") > 0:
            workspace = workspace[:workspace.rfind(".gdb") + 4]

    #create a simple field mapping from input to output
    point_layer_description = arcpy.Describe(point_layer)
    polygon_layer_description = arcpy.Describe(polygon_feature_class)
    fields = {}
    for field in point_layer_description.fields:
        name = field.name
        if (name != point_layer_description.shapeFieldName and name != point_layer_description.OIDFieldName
                and field.editable):  # skip un-editable fields like Shape_Length
            fields[name] = arcpy.ValidateFieldName(name, workspace)
            #print workspace, name, "=>", fields[name]  

    #Add the polygon_group_field_name to the polygon FC
    polygon_group_new_field_name = None
    if polygon_group_field_name:
        polygon_group_new_field_name = arcpy.ValidateFieldName(polygon_group_field_name, workspace)
        field_type = None
        for field in polygon_layer_description.fields:
            if field.name == polygon_group_field_name:
                field_type = field.type
                break
        if field_type is None:
            sys.exit()
        arcpy.AddField_management(polygon_feature_class, polygon_group_new_field_name, field_type)

    #preprocess the polygonTable data
    polygon_data = parse_polygon_data(
        polygon_data_table, polygon_id_field_name, polygon_azimuth_field_name,
        polygon_distance_field_name)

    #create the cursors
    poly = None
    polygons = arcpy.InsertCursor(polygon_feature_class)
    points = arcpy.SearchCursor(point_layer)
    for point in points:
        point_shape = point.getValue(point_layer_description.shapeFieldName)
        if point_shape:
            group_id = None  # FIXME: set this in a loop
            polygon_shape = make_polygon(
                point_shape, point.getValue(point_id_field_name), group_id, polygon_data)
            if polygon_shape:
                poly = polygons.newRow()
                for field in fields:
                    poly.setValue(fields[field], point.getValue(field))
                if polygon_group_field_name:
                    poly.setValue(polygon_group_new_field_name, group_id)
                poly.setValue(polygon_layer_description.shapeFieldName, polygon_shape)
                polygons.insertRow(poly)

    arcpy.AddMessage("Output feature class has been populated")

    #When writing to a PGDB, you must delete the last row or it will not
    #get written to the database.
    if poly:
        del poly
        #delete the insert cursor to close it and remove the exclusive lock
    del polygons


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

    test = True
    if test:
        #pointLayer = r"c:\tmp\test.gdb\w2011a0901"
        #pointIdFieldName = "ESRI_OID"
        #polygonDataTable = r"c:\tmp\test.gdb\pdata"
        pointLayer = r"T:\PROJECTS\KEFJ\CampsiteInventory\Data\GPSData\KEFJ_2010\GPSData\Export\Campsite.shp"
        pointIdFieldName = "Tag_Number"
        polygonDataTable = r"C:\tmp\VariableTransectData.xls\year2010$"
        polygonIdFieldName = "Tag"
        polygonGroupFieldName = "Year"
        polygonSortFieldName = "AutoSort"
        polygonAzimuthFieldName = "A_Calc_T"
        polygonDistanceFieldName = "D"
        polygonFeatureClass = r"c:\tmp\test.gdb\poly4"

    #
    # Input validation
    #  for command line and IDE usage,
    #  ArcToolbox provides validation before calling script.
    #
    if not polygonFeatureClass:
        print("No output requested. Quitting.")
        sys.exit()

    if arcpy.Exists(polygonFeatureClass):
        if arcpy.env.overwriteOutput:
            print("Over-writing existing output.")
            arcpy.Delete_management(polygonFeatureClass)
        else:
            print("Output exists, overwrite is not authorized. Quitting.")
            sys.exit()

    if not pointLayer:
        print("No control point layer was provided. Quitting.")
        sys.exit()

    if not arcpy.Exists(pointLayer):
        print("Control point layer cannot be found. Quitting.")
        sys.exit()

    if not polygonDataTable:
        print("No polygon data table was provided. Quitting.")
        sys.exit()

    if not arcpy.Exists(polygonDataTable):
        print("Polygon data table cannot be found. Quitting.")
        sys.exit()

    # Consider validating field names (ArcToolbox does this for us, but useful for command line usage).

    #
    # Create polygons
    #
    polygon_from_control_point(
        pointLayer, pointIdFieldName,
        polygonDataTable, polygonIdFieldName, polygonGroupFieldName, polygonSortFieldName,
        polygonAzimuthFieldName, polygonDistanceFieldName, polygonFeatureClass)
