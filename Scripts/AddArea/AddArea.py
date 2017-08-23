# ------------------------------------------------------------------------------
# add_area.py
# Created: 2011-01-25
# rewritten 2014-11-13 for 10.2 to use the new geodesicArea field calculation
#
# Title:
# Add an area field to polygon features
#
# Tags:
# calculate, acres, square, unit, attribute, column, field
#
# Summary:
# Add and/or update an area field to polygon features
#  WARNING: Results will be incorrect if the features have geographic coordinates, or no projection specified.
#
# Usage:
# This tool will add and/or update an area field to polygon features. The field name and units are defined by the user.
#
# Parameter 1:
# Features
# A semicolon separated list of polygon or polyline feature classes.
#
# Parameter 2:
# Field_Name
# The name of the field to add or update. If the field does not exist, it will be added. If the field exists, it must be a numeric field. The field name must be a valid for the features workspace i.e. no spaces, no reserved words, and less than 10 characters for shapefiles.
#
# Parameter 3:
# Units
# The units for the area of the polygon.  See the system "Calculate Field" tool for valid units
#
# Scripting Syntax:
# AddArea_AlaskaPak(Features, Field_Name, Units)
#
# Example1:
# Scripting Example
# The following example shows how this script can be used in another python script, or directly in the ArcGIS Python Window.  It assumes that the script has been loaded into a toolbox, and the toolbox has been loaded into the active session of ArcGIS.
#  features = r"C:\tmp\parks.shp"
#  AddArea(features, "Acres", "ACRES")
#
# Example2:
# Command Line Example
# The following example shows how the script can be used from the operating system command line.  It assumes that the current directory is the location of the script, and that the python interpeter is the path.
#  C:\tmp> python add_area.py "C:\tmp\parks.shp;C:\tmp\test.gdb\preserves" SqKm SQUAREKILOMETERS
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

#issues:
# * addfield may alter the name of the field, but th original name is
# still used for calc field
# * If coordinate system is unknown or geographic, units are assumed to be units
# requested
# * Feature may be locked or uneditable

import os.path
import arcpy
import utils


def add_area_to_feature(feature, units, fieldname="Area", overwrite=False):
    #Check for a feature
    if not arcpy.Exists(feature):
        utils.warn("feature not found.  Skipping...")
        return

    #Get some info about the feature
    feature_description = arcpy.Describe(feature)
    shape_name = feature_description.shapeFieldName
    feature_sr = feature_description.spatialReference
    feature_is_projected = feature_sr.type == "Projected" and feature_sr.name != "Unknown"
    feature_is_polygon = feature_description.shapeType != "Polygon"

    #Validate Feature - We only work on polygons
    if not feature_is_polygon:
        utils.warn("feature is not a polygon.  Skipping...")
        return

    #Validate or Sanitize Field Name
    if fieldname in arcpy.ListFields(feature):
        if overwrite:
            if not fieldname in arcpy.ListFields(feature, fieldname, "Double"):
                utils.warn("field {} exists, but is not the right type.  Skipping...".format(fieldname))
                return
        else:
            utils.warn("field {} already exists.  Skipping...".format(fieldname))
            return
        new_fieldname = fieldname
    else:
        workspace = os.path.dirname(feature)
        new_fieldname = arcpy.ValidateFieldName(field_name, workspace)
        arcpy.AddField_management(feature, new_fieldname, "Double", "", "", "", "", "NULLABLE", "NON_REQUIRED", "")

    #Sanitize Units
    valid_units = ["ACRES", "ARES", "HECTARES", "SQUARECENTIMETERS", "SQUAREDECIMETERS", "SQUAREINCHES", "SQUAREFEET",
                   "SQUAREKILOMETERS", "SQUAREMETERS", "SQUAREMILES", "SQUAREMILLIMETERS", "SQUAREYARDS"]
    if units.upper() in valid_units:
        out_units = "@"+units.upper()
    else:
        utils.warn("Unknown units {}, area will be in the feature's units".format(units))
        out_units = ""

    #Determine Area Calculation Method
    if feature_is_projected:
        area_method = ".area"
    else:
        if out_units:
            area_method = ".geodesicArea"
            utils.info("Calculating geodesic area for {}".format(feature))
        else:
            area_method = ".area"
            utils.warn("Calculating area in square degrees. This is usually meaningless.")

    #Do Calculation
    calculation = "!" + shape_name + area_method + out_units + "!"
    arcpy.CalculateField_management(feature, new_fieldname, calculation, "", "")


def add_area_to_features(features, units, fieldname="Area", overwrite=False):
    for feature in features:
        utils.info("Adding Area to " + feature)
        add_area_to_feature(feature, fieldname, units, overwrite)


if __name__ == "__main__":
    feature_list = arcpy.GetParameterAsText(0).split(";")
    user_units = arcpy.GetParameterAsText(1)
    field_name = arcpy.GetParameterAsText(2)
    overwrite_field = arcpy.GetParameterAsText(3).lower() == 'true'
    add_area_to_features(feature_list, user_units, field_name, overwrite_field)