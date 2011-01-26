# ------------------------------------------------------------------------------
# AddID.py
# Created: 2011-01-25
#
# Title:
# Add Unique ID to a dataset
#
# Tags:
# unique identification add calculate attribute column field
#
# Summary:
# This tool will add and populate an ID attribute to a list of feature classes.
#
# Usage:
# To do.
#
# Parameter 1:
# Features
# A semicolon separated list of data sets. If it has a field called idFieldName it will be overwritten, and it must be of type long.
#
# Parameter 2:
# Features
# A semicolon separated list of data sets. If it has a field called idFieldName it will be overwritten, and it must be of type long.
#
# Parameter 3:
# Features
# A semicolon separated list of data sets. If it has a field called idFieldName it will be overwritten, and it must be of type long.
#
# Parameter 4:
# Features
# A semicolon separated list of data sets. If it has a field called idFieldName it will be overwritten, and it must be of type long.
#
# Parameter 5:
# Features
# A semicolon separated list of data sets. If it has a field called idFieldName it will be overwritten, and it must be of type long.
#
# Scripting Syntax:
# AddID(Features)
#
# Example1:
# Scripting Example
# The following example shows how this script can be used in another python script, or directly in the ArcGIS Python Window.  It assumes that the script has been loaded into a toolbox, and the toolbox has been loaded into the active session of ArcGIS.
#  features = r"C:\tmp\roads.shp"
#  AddID(features, "EvenIDs", 2, 2, length)
#
# Example2:
# Command Line Example
# The following example shows how the script can be used from the operating system command line.  It assumes that the current directory is the location of the script, and that the python interpeter is the path.
#  C:\tmp> python AddMiles.py "C:\tmp\roads.shp;C:\tmp\test.gdb\fences" newID 1 1 #
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

#get input
featureList = arcpy.GetParameterAsText(0)
idFieldName = arcpy.GetParameterAsText(1)
start = arcpy.GetParameterAsText(2)
increment = arcpy.GetParameterAsText(3)
sortFieldName = arcpy.GetParameterAsText(4)

#validate input
if idFieldName == "" or idFieldName == "#":
    idFieldName = "UniqueID"
try:
    start = int(start)
except:
    start = 1
    
try:
    increment = int(increment)
except:
    increment = 1

#process features  
for feature in featureList.split(";"):
    if idFieldName not in arcpy.ListFields(feature):
        arcpy.AddField_management(feature, idFieldName, "Long", "", "", "", "",
                                  "NULLABLE", "NON_REQUIRED", "")
    id = start
    rows = arcpy.UpdateCursor(feature,"","",idFieldName, sortFieldName)
    for row in rows:
        row.setValue(idFieldName, id)
        rows.updateRow(row)
        id = id + increment

