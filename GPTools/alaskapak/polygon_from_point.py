# -*- coding: utf-8 -*-
"""
Create polygons from a control point and a set of azimuths and distances.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import math
import os
import sys

import arcpy

import utils

# FIXME: Merge with or replace polygon_from_point_alt.py


def ParsePolygonData(
    polygonDataTable,
    polygonIdFieldName,
    polygonAzimuthFieldName,
    polygonDistanceFieldName,
):
    """Returns a dictionary where key is the point/polygon id, and
    the value is an ordered list of (azimuth/distance) tuples"""
    result = {}
    currentId = None
    fields = [polygonIdFieldName, polygonAzimuthFieldName, polygonDistanceFieldName]
    with arcpy.da.SearchCursor(polygonDataTable, fields) as cursor:
        for row in cursor:
            id = row[0]
            # We are done if we find a null id
            if id == None:
                break
            # If we have seen this id before, then skip this row
            if id in result:
                msg = "Polygon {0} has already been closed, skipping."
                utils.warn(msg.format(id))
                continue
            # we have a new id, and an old id
            if id != currentId:
                # save the old list
                if currentId and currentList:
                    result[currentId] = currentList
                # start a new list
                currentList = []
                currentId = id
            # add the point to the current list
            currentList.append((row[1], row[2]))
    # save any open lists
    if currentId and currentList:
        result[currentId] = currentList
    return result


def MakePolygon(point, pointId, polygonData):
    try:
        data = polygonData[pointId]
    except KeyError:
        return None

    if len(data) < 3:
        msg = "Polygon {0} has only {0} pairs of Azimuth/Distance, skipping."
        utils.warn(msg.format(pointId, len(data)))
        return None

    vertices = []
    oldAzimuth = None
    for azimuth, distance in data:
        if oldAzimuth and azimuth < oldAzimuth:
            msg = "Azimuths for polygon {0} go backwards from {0:.2} to {0:.2}."
            utils.warn(msg.format(pointId, oldAzimuth, azimuth))
        oldAzimuth = azimuth
        if azimuth < 0 or azimuth > 360:
            if azimuth == None:
                msg = "An azimuth is null for polygon {0}.".format(pointId)
            else:
                msg = "Azimuth {0:.2} for polygon {1} is out of range 0-360."
                msg = msg.format(azimuth, pointId)
            utils.warn(msg)
            continue
        if distance <= 0:
            if distance == None:
                msg = "A distance is null for polygon {0}.".format(pointId)
            else:
                msg = "Distance {0:.2} for polygon {1} is out of range d <= 0."
                msg = msg.format(distance, pointId)
            utils.warn(msg)
            continue

        x = point.getPart().X + distance * (math.sin(azimuth * math.pi / 180))
        y = point.getPart().Y + distance * (math.cos(azimuth * math.pi / 180))
        vertices.append(arcpy.Point(x, y))
    if len(vertices) < 3:
        msg = "Polygon {0} has {1} pairs of valid Azimuth/Distance, skipping."
        utils.warn(msg.format(pointId, len(vertices)))
        return None
    vertices.append(vertices[0])
    return arcpy.Polygon(arcpy.Array(vertices))


def PolygonFromControlPoint(
    pointLayer,
    pointIdFieldName,
    polygonDataTable,
    dataTableFieldName,
    dataTableIdentifier,
    polygonIdFieldName,
    polygonAzimuthFieldName,
    polygonDistanceFieldName,
    polygonFeatureClass,
):

    workspace, featureClass = os.path.split(polygonFeatureClass)
    arcpy.CreateFeatureclass_management(
        workspace,
        featureClass,
        "Polygon",
        pointLayer,
        "SAME_AS_TEMPLATE",
        "SAME_AS_TEMPLATE",
        pointLayer,
    )

    arcpy.AddMessage("Empty polygon feature class has been created")

    # workaround for bug wherein
    # ValidateFieldName(field,workspace\feature_dataset)
    # returns incorrect results.  Fix is to remove the feature_dataset"
    workspace = workspace.lower()
    if workspace.rfind(".mdb") > 0:
        workspace = workspace[: workspace.rfind(".mdb") + 4]
    else:
        if workspace.rfind(".gdb") > 0:
            workspace = workspace[: workspace.rfind(".gdb") + 4]

    # create a simple field mapping from input to output
    pointLayerDescription = arcpy.Describe(pointLayer)
    polyLayerDescription = arcpy.Describe(polygonFeatureClass)
    fields = {}
    for field in pointLayerDescription.fields:
        name = field.name
        if (
            name != pointLayerDescription.shapeFieldName
            and name != pointLayerDescription.OIDFieldName
            and field.editable
        ):  # skip un-editable fields like Shape_Length
            fields[name] = arcpy.ValidateFieldName(name, workspace)
            # print(workspace, name, "=>", fields[name])

    # Add the dataTableFieldName to the polygon FC
    if dataTableFieldName:
        dataTableFieldName = arcpy.ValidateFieldName(dataTableFieldName, workspace)
        arcpy.AddField_management(polygonFeatureClass, dataTableFieldName, "TEXT")

    # preprocess the polygonTable data
    polygonData = ParsePolygonData(
        polygonDataTable,
        polygonIdFieldName,
        polygonAzimuthFieldName,
        polygonDistanceFieldName,
    )

    # create the cursors
    poly = None
    polys = arcpy.InsertCursor(polygonFeatureClass)
    points = arcpy.SearchCursor(pointLayer)
    for point in points:
        pointShape = point.getValue(pointLayerDescription.shapeFieldName)
        if pointShape:
            polyShape = MakePolygon(
                pointShape, point.getValue(pointIdFieldName), polygonData
            )
            if polyShape:
                poly = polys.newRow()
                for field in fields:
                    poly.setValue(fields[field], point.getValue(field))
                if dataTableFieldName:
                    poly.setValue(dataTableFieldName, dataTableIdentifier)
                poly.setValue(polyLayerDescription.shapeFieldName, polyShape)
                polys.insertRow(poly)

    arcpy.AddMessage("Output feature class has been populated")

    # When writing to a Personal GDB, you must delete the last row or it will not
    # get written to the database.
    if poly:
        del poly
    # delete the insert cursor to close it and remove the exclusive lock
    del polys


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
        # pointLayer = r"c:\tmp\test.gdb\w2011a0901"
        # pointIdFieldName = "ESRI_OID"
        # polygonDataTable = r"c:\tmp\test.gdb\pdata"
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

    # TODO - validate field names.

    #
    # Create polygons
    #
    PolygonFromControlPoint(
        pointLayer,
        pointIdFieldName,
        polygonDataTable,
        dataTableFieldName,
        dataTableIdentifier,
        polygonIdFieldName,
        polygonAzimuthFieldName,
        polygonDistanceFieldName,
        polygonFeatureClass,
    )
