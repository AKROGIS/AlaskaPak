# -*- coding: utf-8 -*-
"""
AddLength.py
Created: 2011-01-25

Title:
Add a length field to polyline or polygon features

Tags:
perimeter, miles, feet, meter, unit, calculate, attribute, column, field

Summary:
Add and/or update a length field for line and polygon features
 WARNING: Results will be incorrect if the features have geographic coordinates,
 or no projection specified.

Usage:
This tool will add and/or update a length field to Polyline or Polygon features.
The field name and units are defined by the user.

Parameter 1:
Features
A semicolon separated list of polygon or polyline feature classes.

Parameter 2:
Field_Name
The name of the field to add or update. If the field does not exist, it will be added.
If the field exists, it must be a numeric field. The field name must be a valid for
the features workspace i.e. no spaces, no reserved words, and less than 10 characters
for shapefiles.

Parameter 3:
Units
The units for the line length or the polygon perimeter.  See the system
"Calculate Field" tool for valid units

Scripting Syntax:
AddLength_AlaskaPak(Features, Field_Name, Units)

Example1:
Scripting Example
The following example shows how this script can be used in another python script,
or directly in the ArcGIS Python Window.  It assumes that the script has been
loaded into a toolbox, and the toolbox has been loaded into the active session of ArcGIS.
 features = r"C:\tmp\roads.shp"
 AddLength_AlaskaPak(features, "Miles", "MILES")

Example2:
Command Line Example
The following example shows how the script can be used from the operating system
command line.  It assumes that the current directory is the location of the script,
and that the python interpreter is the path.
 C:\tmp> python AddLength.py "C:\tmp\roads.shp;C:\tmp\test.gdb\fences" Km KILOMETERS

Credits:
Regan Sarwas, Alaska Region GIS Team, National Park Service

Limitations:
Public Domain

Requirements
arcpy module - requires ArcGIS v10+ and a valid license

Disclaimer:
This software is provide "as is" and the National Park Service gives
no warranty, expressed or implied, as to the accuracy, reliability,
or completeness of this software. Although this software has been
processed successfully on a computer system at the National Park
Service, no warranty expressed or implied is made regarding the
functioning of the software on another system or for general or
scientific purposes, nor shall the act of distribution constitute any
such warranty. This disclaimer applies both to individual use of the
software and aggregate use with other software.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import arcpy

from . import utils


valid_units = [
    "CENTIMETERS",
    "DECIMALDEGREES",
    "DECIMETERS",
    "FEET",
    "INCHES",
    "KILOMETERS",
    "METERS",
    "MILES",
    "MILLIMETERS",
    "NAUTICALMILES",
    "POINTS",
    "UNKNOWN",
    "YARDS",
]


def add_length_to_feature(feature, units, fieldname="Length", overwrite=False):
    """Add a length attribute to a single polyline or polygon feature class."""
    # TODO Document parameters in the doc string

    # TODO: addfield may alter the name of the field, but the original name is
    #       still used for calc field
    # TODO: If coordinate system is unknown, units are assumed to be units requested.
    # TODO: If coordinates are geographic, results are wrong. (the shape_length is also
    # wrong - it uses planar geometry with the spherical coordinates.)
    # TODO: Feature may be locked or un-editable
    field_names = arcpy.ListFields(feature)
    if fieldname in field_names and not overwrite:
        msg = "Aborting. Field {0} exists and overwrite is false."
        utils.warn(msg.format(fieldname))
        return

    if fieldname not in field_names:
        arcpy.AddField_management(
            feature, fieldname, "Double", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""
        )
    length = "!shape.length@{0}!".format(units)
    arcpy.CalculateField_management(feature, fieldname, length, "PYTHON_9.3", "")


def add_length_to_features(features, units, fieldname="Length", overwrite=False):
    """Add a length attribute to multiple polyline or polygon feature classes."""
    # TODO Document parameters in the doc string

    for feature in features:
        utils.info("Adding Length to {0}".format(feature))
        add_length_to_feature(feature, units, fieldname, overwrite)


if __name__ == "__main__":
    # TODO: this is in a package now, so it can't be called as a script.
    # TODO: if run as a script for testing, does the `from . import utils` work?
    feature_list = arcpy.GetParameterAsText(0).split(";")
    user_units = arcpy.GetParameterAsText(1)
    # TODO: what if optional parameters are not provided on the command line
    # TODO: support arcpy command line convention of "#" for None
    field_name = arcpy.GetParameterAsText(2)
    overwrite_field = arcpy.GetParameterAsText(3).lower() == "true"
    # TODO: support parameter(4) output feature class for single or remove option
    add_length_to_features(feature_list, user_units, field_name, overwrite_field)
