# ------------------------------------------------------------------------------
# AddMiles.py
# Created: 2011-01-25
#
# Title:
# Add Miles atribute to Polyline or Polygon features
#
# Tags:
# length perimeter add calculate miles attribute column field
#
# Summary:
# This tool will add Miles atribute to Polyline or Polygon features.
#
# Usage:
# To do.
#
# Parameter 1:
# Features
# A semicolon separated list of polygon or polyline feature class. Each must have a defined coordinate system. If it has a field called "Miles" it will be overwritten, and it must be of type double.
#
# Scripting Syntax:
# AddMiles(Features)
#
# Example1:
# Scripting Example
# The following example shows how this script can be used in another python script, or directly in the ArcGIS Python Window.  It assumes that the script has been loaded into a toolbox, and the toolbox has been loaded into the active session of ArcGIS.
#  features = r"C:\tmp\roads.shp"
#  AddMiles(features)
#
# Example2:
# Command Line Example
# The following example shows how the script can be used from the operating system command line.  It assumes that the current directory is the location of the script, and that the python interpeter is the path.
#  C:\tmp> python AddMiles.py "C:\tmp\roads.shp;C:\tmp\test.gdb\fences"
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

import arcpy

featureList = arcpy.GetParameterAsText(0)
fieldName = "Miles"

for feature in featureList.split(";"):
    if fieldName not in arcpy.ListFields(feature):
        arcpy.AddField_management(feature, fieldName, "Double", "", "", "", "",
                                  "NULLABLE", "NON_REQUIRED", "")
    arcpy.CalculateField_management(feature, fieldName, "!shape.length@miles!",
                                    "PYTHON_9.3", "")

