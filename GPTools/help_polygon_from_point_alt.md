Point2Poly3.py
Created on: 2014-03-7
Created by: Regan Sarwas, GIS Team, Alaska Region, National Park Service
            regan_sarwas@nps.gov

Title:
Polygons From Control Point

Tags:
Azimuth, Distance, Campsite

Summary:
Creates polygon features from point features and azimuth/distance measurements relative to the point features.

Usage:
Provided point features, and a table of related azimuth/distance measurements this tool will create a
polygon for each point with at least three valid azimuth/distance measurements.
The entire table of polygon data is read into memory once, which may cause problems for very, very large data sets.

Parameter 1:
Control_Point_Features
A point feature class or layer with the control point for polygons. The control point is the basis or origin of the
azimuth and distance measurements to the perimeter vertices.
The Control_Point_Features must be in a spatial reference system with linear units (i.e. projected coordinates)
If a layer is used, then only the points in the current selection set are used.
If there is a point without matching data in the Azimuth_Distance_Table, then that point will be skipped with a
warning. Attributes from the Control_Point_Features will NOT be transferred to the Polygon_Features.

Parameter 2:
Control_Point_Id_Field
The name of the field in the control points that uniquely identifies each control points.
The values in this field will be matched with the values in the Polygon_Id_Field in the Azimuth_Distance_Table.

Parameter 3:
Azimuth_Distance_Table
This can be a data table or a feature class/layer.
The table contains a collection of azimuth and distance measurements (as described below) for the control points
If there is azimuth & distance data that does not relate to a control point, it is silently ignored.
If a control point has no azimuth & distance that point is skipped, and no polygons are created at that point.
If a control point has only 1 or 2 azimuth & distance records for a given grouping value, then a polygon can not
be created in that situation, and a warning will be issued.

Parameter 4:
Polygon_Id_Field
The name of a field in the Azimuth_Distance_Table that relates the azimuth & distance records to a control point.
This must be the same data type as the Control_Point_Id_Field in the Control_Point_Features.

Parameter 5:
Group_Field
The name of a field in the Azimuth_Distance_Table that groups the azimuth/distance records into distinct
polygons for a given control point.
For example, if azimuth/distance measurements are collected on a yearly basis for each control point, then
the year attribute would be used as the Group_Field.
If the Group_Field is not provided, then one polygon per control point is assumed.

Parameter 6:
Sort_Field
The name of a field in the Azimuth_Distance_Table that sorts the azimuth & distance records in clockwise
order around the perimeter of the polygon.
If the vertices are not sorted properly, you will get some very bizarre looking polygons.

Parameter 7:
Azimuth_Field
The name of a field in the Azimuth_Distance_Table that contains the azimuth measurements (as numbers)
Azimuth values are assumed to be in degrees and referenced from the control point to true north.
True north is zero degrees and azimuth values increase clockwise up to 360 degrees.
A value less than zero or greater than 360 is considered invalid and is ignored with a warning.

Parameter 8:
Distance_Field
The name of a field in the Azimuth_Distance_Table that contains the distance measurements (as numbers)
Distances are distance measures from the control point to a vertex in the perimeter of the polygon.  Distances are
assumed to be in the same linear units as the spatial reference of the Control_Point_Features.
A value less than or equal to zero is ignored with a warning.

Parameter 9:
Polygon_Features
The output polygon feature class to be created.
The polygons will inherit the spatial reference of the Control_Point_Features, but no other attributes.
The Polygon_Id_Field and Group_Field (if provided) attributes from the Azimuth_Distance_Table will be inherited.
There may be multiple polygons for each control point which are distinguished by the attributes in the Group_Field.

Scripting Syntax:
PolygonBuilder (Control_Point_Features, Control_Point_Id_Field, Azimuth_Distance_Table,
Polygon_Id_Field, Group_Field, Sort_Field, Azimuth_Field, Distance_Field, Polygon_Features)

Credits:
Regan Sarwas, Alaska Region GIS Team, National Park Service

Limitations:
Public Domain

Requirements
arcpy module - requires ArcGIS v10.1 and a valid license

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
