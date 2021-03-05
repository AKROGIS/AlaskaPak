RandomTransects.py
Created: 2011-02-28 (10.0)

Title:
Random Transects

Tags:
survey, inventory, animal, tracking, plane, monitoring, line,

Summary:
Creates random survey transects (lines) within a polygon boundary.

Usage:
This tool uses CreateFeature_Management to create a new polyline feature class
(See the help for that tool regarding the environment variables that will
control the feature class creation).  These feature will have no attributes.
the geometry will be simple straight lines that are wholey within the
boundary polygon.

Parameter 1:
Polygon_Boundaries
A polygon layer in ArcMap, or the full path of a polygon feature class with
boundaries for sets of transect lines.

Parameter 2:
New_Transects
The name and location of the feature class to create.
If the feature class already exists. You can only overwrite it if you have set
that option in the geoprocessing tab in Tools->Options menu.
The output coordinate system will be determined by the environment settings.
Typically it will default to the same as the input. Click on the
Environment... button and then the General Settings tab to check and set the
output coordinate system.  The output coordinate system must be projected
or the length of the line will be undefined.
No attributes are created form the transect lines.
Transects may be M/Z aware (based on environment), but no M/Z values are
added to the vertices.

Parameter 3:
Transects_per_boundary
The number of transects to try and create for each boundary.
This parameter is optional.  The default value is 5.
This parameter must be greater than zero.

Parameter 4:
Minimum_length
The minimum length of the transect line.
This parameter is optional.  The default value is 1 Meters.
This parameter must be greater than zero and less or equal to Maximum_length.
The distance can include a space and units (surround with quotes).
The units (and spelling) understood are predetermined by ArcTool box.
The DecimalDegrees units cannot be used.  Unknown units are an error.
Not specifing the units defaults to meters.

Parameter 5:
Maximum_length
The maximum length of the transect line.
This parameter is optional.  The default value is 1000 Meters.
This parameter must be greater than or equal to Minimum_length.
See Minimum_length for a discussion of units.
If the length is too large then finding a transect that fits within the
boundary may not by possible.

Parameter 6:
Maximum_Attempts
Since it may be impossible to find as many transects as requested, the tool
will stop looking after Maximum_Attempts have failed to find a transect.
The larger this number, the longer the program will take to run.
Increasing this number helps find all the transects requested, but does not
guarantee success, as the input conditions may be impossible to satisfy.
This parameter is optional.  The default value is 100.

Parameter 7:
Allow_Overlap
If transects can overlap one another, then specify True. To ensure that
no transects cross each other, specify False.
This parameter is optional.  The default value is True.

Environment:
 same as arcpy.CreateFeatureclass_management()

Scripting Syntax:
RandomTransects_AlaskaPak (Polygon_Boundaries, New_Transects,
   Transects_per_boundary, Minimum_length, Maximum_length,
   Maximum_Attempts, Allow_Overlap)

Example1:
Scripting Example
The following example shows how this script can be used in another python
script, or directly in the ArcGIS Python Window.  It assumes that the script
has been loaded into a toolbox, and the toolbox has been loaded into the
active session of ArcGIS.
 polyFC = r"C:\tmp\game_units.shp"
 lineFC = r"C:\tmp\test.gdb\park\transects"
 # Create 2 transects less than 500 feet long for each game unit.
 RandomTransects_AlaskaPak (polyFC, lineFC, 2, #, "500 Feet", 10, False)

Example2:
Command Line Example
The following example shows how the script can be used from the operating
system command line.  It assumes that the current directory is the location
of the script, and that the python interpreter is the path.
It will try to create 10 100 meter transects in each polygon in polys.shp
 C:\tmp> python ObscurePoints.py polys.shp c:\tmp\lines.shp 10 100 100

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
