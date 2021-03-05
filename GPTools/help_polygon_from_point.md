
Point2Poly2.py
Created on: 2012-06-12

Title:
Polygons From Control Point

Tags:
Azimuth, Distance, Campsite

Summary:
Takes an point feature class and an ordered sets of azimuth/distance measurements to create a polygon feature class

Usage:
Provide a point feature class, and a table of related azimuth/distance measurements, and this tool will create a polygon for each point with at least three valid azimuth/distance measurements.

Parameter 1:
Control_Point_Features
A point feature class or layer with the control point for polygons. The control point is the basis or origin of the azimuth and distance measurements to the perimeter vertices.
If a layer is used, then only the points in the current selection set are used.
If there is a point without a matching data in the Azimuth/Distance table, then that point will not result in a polygon.
Attributes from the points will be applied to the new polygon

Parameter 2:
Control_Point_Id_Field
A unique value to identify each control points. The values in this filed will be matched with the values in the Table Id field.

Parameter 3:
Azimuth_Distance_Table
If there is Azimuth/Distance data for which the tag does not match to a point in the Control Point Features, a warning will be given, and that data will be skipped.
It is assumed that the data will be sorted first by polygon id, then by azimuth/distance data. The azimuths should generally proceed counter clockwise from zero to 360 degrees.
The vertices of the polygons will be generated in the order the azimuth/distance data is provided, An out of sequence azimuth (i.e. an azimuth value is less than the value of the preceding azimuth), is valid, but will generate a warning.
There should only be one set of azimuth/distance measurements for each polygon id in the input table.
When the polygon id changes, a new polygon will be started.
If a polygon id is re-encountered after that polygon has been finished (i.e. one or more polygons are in between, then the new data will generate an error and be ignored. The ignored lines will not signal the end of the preceding polygon.
It is an error for a polygon to have less than 3 azimuth/distance pairs. These polygons will generate a warning, and will be skipped.
A blank polygon id, will signal the end of data processing.

Parameter 4:
Fieldname_for_table_Identifier
The name of a new field in the output feature class that will hold information identifying the azimuth/distance data table.
If this field is  empty or null, then no additional field is created, and the following parameter is ignored.

Parameter 5:
Identifier_for_table_data
Text that tags each polygon created as coming from this specific data table.  For example, the year the polygon perimeters were collected.

Parameter 6:
Polygon_Id_Field
The name of a field in the Azimuth/Distance data table.  This field links the polygon perimeter points to the polygon control point.  The values in this column must match the values in the Control Point Id field.

Parameter 7:
Azimuth_Field
Azimuth values are assumed to be in degrees and referenced from the control point to true north. True north is zero degrees and azimuth values increase clockwise up to 360 degrees.
A value less than zero, or greater than 360 is considered an error, and will be noted and skipped.

Parameter 8:
Distance_Field
Distances are assumed to be meters from the control point to the perimeter of the polygon.
A value less than or equal to zero is considered an error and will be noted, and skipped.

Parameter 9:
Polygon_Features
The output polygons. A polygon will be created for each control point with 3 or more pairs of matching valid azimuth/distance measurements.
The polygons will inherit the spatial reference and all attributes of the control points.

Scripting Syntax:
PolygonBuilder (Control_Point_Features, Control_Point_Id_Field, Azimuth_Distance_Table, Fieldname_for_table_Identifier, Identifier_for_table_data, Polygon_Id_Field, Azimuth_Field, Distance_Field, Polygon_Features)

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
