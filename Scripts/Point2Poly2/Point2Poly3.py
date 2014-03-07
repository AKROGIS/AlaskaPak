# ------------------------------------------------------------------------------
# Point2Poly3.py
# Created on: 2014-03-7
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
# If there is Azimuth/Distance data for which the tag does not match to a point in the Control Point Features,
# a warning will be given, and that data will be skipped.
# It is assumed that the data will be sorted first by polygon id, then by azimuth/distance data. The azimuths should
# generally proceed counter clockwise from zero to 360 degrees.
# The vertices of the polygons will be generated in the order the azimuth/distance data is provided, An out of
# sequence azimuth (i.e. an azimuth value is less than the value of the preceeding azimuth), is valid, but will
# generate a warning.
# There should only be one set of azimuth/distance measurements for each polygon id in the input table. 
# When the polygon id changes, a new polygon will be started.
# If a polygon id is re-encountered after that polygon has been finished (i.e. one or more polygons are in between,
# then the new data will generate an error and be ignored. The ignored lines will not signal the end of the preceding
# polygon.
# It is an error for a polygon to have less than 3 azimuth/distance pairs. These polygons will generate a warning, and
# will be skipped.
# A blank polygon id, will signal the end of data processing.
#
# Parameter 4:
# Fieldname_for_table_Identifier
# The name of a new field in the output feature class that will hold information identifying the azimuth/distance data
# table.
# If this field is  empty or null, then no additional field is created, and the following parameter is ignored.
#
# Parameter 5:
# Identifier_for_table_data
# Text that tags each polygon created as coming from this specific data table.  For example, the year the polygon
# perimeters were collected.
#
# Parameter 6:
# Polygon_Id_Field
# The name of a field in the Azimuth/Distance data table.  This field links the polygon perimeter points to the polygon
# control point.  The values in this column must match the values in the Control Point Id field.
#
# Parameter 7:
# Azimuth_Field
# Azimuth values are assumed to be in degress and referenced from the control point to true north. True north is zero
# degrees and azimuth values increase clockwise up to 360 degrees.
# A value less than zero, or greater than 360 is considered an error, and will be noted and skipped.
#
# Parameter 8:
# Distance_Field
# Distances are assumed to be meters from the control point to the perimeter of the polygon.
# A value less than or equal to zero is considered an error and will be noted, and skipped.
#
# Parameter 9:
# Polygon_Features
# The output polygons. A polygon will be created for each control point with 3 or more pairs of matching valid
# azimuth/distance measurements.
# The polygons will inherit the spatial reference and all attributes of the control points.
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
# arcpy module - requires ArcGIS v10+ and a valid license
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


def make_polygon(point, point_id, polygon_data):
    try:
        data = polygon_data[point_id]
    except KeyError:
        return None

    if len(data) < 3:
        msg = "Polygon %d has only %d pairs of Azimuth/Distance, skipping." \
              % (point_id, len(data))
        print("Warning: " + msg)
        arcpy.AddWarning(msg)
        return None

    vertices = []
    old_azimuth = None
    for azimuth, distance in data:
        if old_azimuth and azimuth < old_azimuth:
            msg = "Azimuths for polygon {0:d} go backwards from {1:3.2f} to {2:3.2f}."\
                .format(point_id, old_azimuth, azimuth)
            print("Warning: " + msg)
            arcpy.AddWarning(msg)
        old_azimuth = azimuth
        if azimuth < 0 or azimuth > 360:
            if azimuth is None:
                msg = u"An azimuth is null for polygon {0:d}.".format(point_id)
            else:
                msg = "Azimuth {0:3.2f} for polygon {1:d} is out of range 0-360.".format(azimuth, point_id)
            print("Warning: " + msg)
            arcpy.AddWarning(msg)
            continue
        if distance <= 0:
            if distance is None:
                msg = u"A distance is null for polygon {0:d}." \
                    .format(point_id)
            else:
                msg = "Distance {0:3.2f} for polygon {1:d} is out of range d <= 0.".format(distance, point_id)
            print("Warning: " + msg)
            arcpy.AddWarning(msg)
            continue

        x = point.getPart().X + distance * (math.sin(azimuth * math.pi / 180))
        y = point.getPart().Y + distance * (math.cos(azimuth * math.pi / 180))
        vertices.append(arcpy.Point(x, y))
    if len(vertices) < 3:
        msg = "Polygon {0:d} has {1:d} pairs of valid Azimuth/Distance, skipping.".format(point_id, len(vertices))
        print("Warning: " + msg)
        arcpy.AddWarning(msg)
        return None
    vertices.append(vertices[0])
    return arcpy.Polygon(arcpy.Array(vertices))


def polygon_from_control_point(
        point_layer, point_id_field_name,
        polygon_data_table, data_table_field_name, data_table_identifier,
        polygon_id_field_name, polygon_azimuth_field_name,
        polygon_distance_field_name, polygon_feature_class):
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
    poly_layer_description = arcpy.Describe(polygon_feature_class)
    fields = {}
    for field in point_layer_description.fields:
        name = field.name
        if (name != point_layer_description.shapeFieldName and name != point_layer_description.OIDFieldName
                and field.editable):  # skip un-editable fields like Shape_Length
            fields[name] = arcpy.ValidateFieldName(name, workspace)
            #print workspace, name, "=>", fields[name]  

    #Add the dataTableFieldName to the polygon FC
    if data_table_field_name:
        data_table_field_name = arcpy.ValidateFieldName(data_table_field_name, workspace)
        arcpy.AddField_management(polygon_feature_class, data_table_field_name, "TEXT")

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
            polygon_shape = make_polygon(
                point_shape, point.getValue(point_id_field_name), polygon_data)
            if polygon_shape:
                poly = polygons.newRow()
                for field in fields:
                    poly.setValue(fields[field], point.getValue(field))
                if data_table_field_name:
                    poly.setValue(data_table_field_name, data_table_identifier)
                poly.setValue(poly_layer_description.shapeFieldName, polygon_shape)
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
    dataTableFieldName = arcpy.GetParameterAsText(3)
    dataTableIdentifier = arcpy.GetParameterAsText(4)
    polygonIdFieldName = arcpy.GetParameterAsText(5)
    polygonAzimuthFieldName = arcpy.GetParameterAsText(6)
    polygonDistanceFieldName = arcpy.GetParameterAsText(7)
    polygonFeatureClass = arcpy.GetParameterAsText(8)

    test = False
    if test:
        #pointLayer = r"c:\tmp\test.gdb\w2011a0901"
        #pointIdFieldName = "ESRI_OID"
        #polygonDataTable = r"c:\tmp\test.gdb\pdata"
        pointLayer = r"T:\PROJECTS\KEFJ\CampsiteInventory\Data\GPSData\KEFJ_2010\GPSData\Export\Campsite.shp"
        pointIdFieldName = "Tag_Number"
        polygonDataTable = r"C:\tmp\VariableTransectData.xls\year2010$"
        dataTableFieldName = "Year"
        dataTableIdentifier = "2012"
        polygonIdFieldName = "Tag"
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
        polygonDataTable, dataTableFieldName, dataTableIdentifier,
        polygonIdFieldName, polygonAzimuthFieldName,
        polygonDistanceFieldName, polygonFeatureClass)
