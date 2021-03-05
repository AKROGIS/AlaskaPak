ArcGIS script to add an area attribute to polygon features

:Created:
  2014-11-13

:Title:
  Add an area attribute to polygon features

:Tags:
  calculate, acres, square, unit, attribute, column, field

:Summary:
  Add or update an area field in a set of polygon feature classes.

:Usage:
  This tool will add (or update) a field with the area of the polygon
  features. The field and areal units are defined by the user.  By
  default if the feature class has geographic coordinates and units
  are provided then a geodesic area is calculated.  If the feature
  class has geographic coordinates and no units are provided then the
  area is calculated in square degrees, which is generally meaningless.

:Credits:
  Regan Sarwas, Alaska Region GIS Team, National Park Service

:License:
  Public Domain

:Disclaimer:
  This software is provide "as is" and the National Park Service gives
  no warranty, expressed or implied, as to the accuracy, reliability,
  or completeness of this software. Although this software has been
  processed successfully on a computer system at the National Park
  Service, no warranty expressed or implied is made regarding the
  functioning of the software on another system or for general or
  scientific purposes, nor shall the act of distribution constitute any
  such warranty. This disclaimer applies both to individual use of the
  software and aggregate use with other software.

Requirements:
  * Python 2.7+ or 3.x
  * ArcGIS arcpy module v10.2+ with basic (or better) license

Scripting Syntax
================
add_area(features, units, field_name, overwrite)

:features:
  A semicolon separated list of polygon feature classes.  This
  parameter is required, and there is no default.

:units:
  The units for the area of the polygon.  See the system tool
  Calculate Field (Data Management) for valid units.  If units
  are not valid, or not provided, then the units of the feature
  class are used.

:field_name:
  The name of the field to add or update. If the field does not exist,
  it will be added. If the field exists, it must be a double field.
  The Field_Name may get mangled to ensure it is valid for the feature's
  workspace.  If no Field_Name is provided, the default is "Area".

:overwrite:
  If the Field_Name already exists in a feature class, it will not be
  overwritten, unless this parameter is "True".  The default is "False".

Examples
========
Scripting Example
-----------------
The following example shows how this script can be used in the ArcGIS
Python Window.  It assumes that the script has been loaded into a
toolbox, and the toolbox has been loaded into the active session of
ArcGIS.

::

  features = r"C:/tmp/parks.shp"
  add_area(features, "ACRES")

Command Line Example
--------------------
The following example shows how the script can be used from the
operating system command line.  It assumes that the current directory
is the location of the script, and that the python interpreter is in
the path.

::

  C:/tmp> python add_area.py
          "C:/tmp/parks.shp;C:/tmp/test.gdb/preserves"
          SQUAREKILOMETERS SqKm True