# ------------------------------------------------------------------------------
# AddArea.py
# Created: 2011-01-25
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
#  C:\tmp> python AddArea.py "C:\tmp\parks.shp;C:\tmp\test.gdb\preserves" SqKm SQUAREKILOMETERS
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

validUnits = ["ACRES","ARES","HECTARES","SQUARECENTIMETERS","SQUAREDECIMETERS","SQUAREINCHES","SQUAREFEET","SQUAREKILOMETERS","SQUAREMETERS","SQUAREMILES","SQUAREMILLIMETERS","SQUAREYARDS"]

import arcpy

featureList = arcpy.GetParameterAsText(0)
fieldName = arcpy.GetParameterAsText(1)
units = arcpy.GetParameterAsText(2)

for feature in featureList.split(";"):
    if fieldName not in arcpy.ListFields(feature):
        arcpy.AddField_management(feature, fieldName, "Double", "", "", "", "",
                                  "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(feature, fieldName, "!shape.area@" +
                                    units + "!", "PYTHON_9.3", "")

