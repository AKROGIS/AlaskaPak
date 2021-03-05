Line2Rect.py
Created: 2011-01-14

Title:
Lines to Rectangles

Tags:
Building, Offset, Width, Height, Square, Polygon

Summary:
This tool will derive rectangles from lines and associated offsets.

Usage:
Use this tool to build a polygon feature class containing rectangles derived
from a line feature class.  The line feature class must contain an attribute
for each feature which provides the perpendicular distance from the line to the
far side of the rectangle.

Parameter 1:
Line_Features
The full name of a polyline feature class.  Each line defines the base or first
side of a generated rectangle. Each line can have 1 or more parts (i.e. it may
be a multi-line), and there may be two or more vertices in each part, however
only the first and last vertex of each part are used in the output rectangle.
If the line is a multi-part shape, then the rectangle is also a multi-part shape.
If any line (or part) is degenerate (i.e. a single vertex, or first vertex and
last vertex are the same) then that line (or line part) is skipped. If all parts
in the line are degenerate then no output is created for that line.

Parameter 2:
Rectangle_Width_Field
This is the name of an attribute (column/field) in the line feature class which
specifies the width of the rectangle. Width may also be known as offset or height.
Specifically It is the distance perpendicular to the line at which the far side
of the rectangle is drawn. If the width is positive, the rectangle is drawn on
the right side of the line.  If it is negative it is drawn on the left side.
Right and left are from the perspective of the line looking from the first
vertex to the last. The width must be a numeric (integer or real) field, and it
must be in the same units/coordinate system as the line feature class. The field
name can be either an actual field name, or the alias for the field name.
Actual field names are given priority in case of ambiguity.

Parameter 3:
Rectangle_Features
The full name of a polygon feature class to create.  Any existing feature class
at that path will not be overwritten, and the script will issue an error if the
feature class exists (unless the geoprocessing options are set to overwrite output).
The output feature class will have the same spatial reference system as the input.
If the input feature class has Z or M values then the output will as well, however
no Z or M values will be written to the output. All attributes of the line feature
class are copied to the output feature class, except Shape, OID, and any
non-editable fields (i.e. Shape_Length).

Scripting Syntax:
Line2Rect(Line_Features, Rectangle_Width_Field, Rectangle_Features)

Example1:
Scripting Example
The following example shows how this script can be used in another python script,
or directly in the ArcGIS Python Window.  It assumes that the script has been
loaded into a toolbox, and the toolbox has been loaded into the active session
of ArcGIS.

 lineFC = r"C:/tmp/gps_lines.shp"
 rectFC = r"C:/tmp/test.gdb/park/bldg"
 Line2Rect(lineFC, "width", rectFC)

Example2:
Command Line Example
The following example shows how the script can be used from the operating system
command line.  It assumes that the current directory is the location of the
script, and that the python interpreter is the path.

 C:/tmp> python Line2Rect.py "c:/tmp/gps_lines.shp" "width" "c:/tmp/test.gdb/park/bldg"

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