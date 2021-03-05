# Table2Shape.py
Created: 2011-01-20

* TODO: fix documentation on vertices (rings are no longer supported)
* TODO: esri bug 1: featureset cannot initialize with in_memory feature class
           (load does work)
* TODO: esri bug 2: cannot save a feature set to a feature dataset in a FGDB or PGDB


Title:
Table to Shape

Tags:
point, vertex, list, geometry, polyline, polygon, multi, create, data, convert

Summary:
This tool will create a new feature class from a table of point IDs and a point feature class.

Usage:
Use this tool to build polygons, polylines, or multi-points if you have a point feature class, and a table of vertex ids related to the point feature class.

Parameter 1:
Table
The full name of a data table.  This can be any format understood by ArcGIS (i.e. a CSV text file, a data table in a geodatabase, an Excel spreadsheet, ...).  All attributes in the input table are copied to the output file. The data table must have the column names that match the names of the vertices given in the Vertex_List parameter.  The data type for these columns must be compatible with the data type in the Point_ID parameter.

Parameter 2:
VertexList
This is a semicolon separated list of the attribute (field/column) name for the vertices to use to make this shape.  The vertices are used in the order provided.  If a Polygon shape is requested, the last vertex can be but does not need to be the same as the first vertex.
Mutipart polylines and polygons are not supported. (multiple semicolons are condensed to a single semicolon).
The minimum number of unique vertices is 1 for Multipoint (strange but allowed), 2 for Polyline, and 3 for Polygon.


example: Creates polygons (triangles)

pt_features:
pt_id,SHAPE
1,{0,0}
2,{2,0}
3,{1.1}
4,{2,2}
5,{0,2}

table:
(field type of all ptX columns must match field type of pt_id in pt_features)
name,pt1,pt2,pt3,other_attributes...
t1,1,2,3, ...
t2,5,4,3, ...
t3,1,2,5, ...

vertex_list:  "pt1;pt2;pt3"

results:
name,SHAPE,other_attributes...
t1, [{0,0}, {2,0}, {1.1}], ...
t2, [{0,2}, {2,2}, {1.1}], ...
t3, [{0,0}, {2,0}, {0,2}], ...


Parameter 3:
Points
The full name of the feature class that has the point geometry for the vertices of the output shapes.  This must be a simple point shape (cannot be a multipoint feature class).  All attributes of this feature class are ignored except the shape and the ID column specified by the Point_ID Parameter.
M and Z values are ignored.

Parameter 4:
Point_ID
The name of the attribute (column/field) that contains the ID (name) of the point that is used to reference it in the Shape_Table.  The data type of this attribute must be compatible with the attributes in the Vertex List.

Parameter 5:
Geometry
This determines the shape created by the points.  Valid values are Polygon, Polyline, Multipoint.  Polyline is the default if either "" or "#" is given for this parameter.

Parameter 6:
Output_feature_class
The full name of the feature class to create.  Any existing feature class at that path will not be overwritten, and the script will issue an error if the feature class exists (unless the geoprocessing options are set to overwrite output). The output feature class will have the same spatial reference system as the Point_Features. If the Point_Features has Z or M values then the output will as well, and Z and M values will be preserved. All attributes in the Shape_Table are copied to Output_Features.

Scripting Syntax:
Table2Shape_AlaskaPak (Table, VertexList, Points, Point_ID, Geometry, Output_feature_class)

Example1:
Scripting Example
The following example shows how this script can be used in another python script, or directly in the ArcGIS Python Window.  It assumes that the script has been loaded into a toolbox, and the toolbox has been loaded into the active session of ArcGIS.
 table = r"C:\tmp\facilities.mdb\pipe_segments"
 ptFC = r"C:\tmp\gps_pts.shp"
 outFC = r"C:\tmp\test.gdb\facilities\pipe_cl"
 Table2Shape_AlaskaPak(table, "start;end", ptFC, "id", "Polyline", outFC)

Example2:
Command Line Example
The following example shows how the script can be used from the operating system command line.  It assumes that the current directory is the location of the script, and that the python interpreter is the path.
 C:\tmp> python Table2Shape.py "C:\tmp\facilities.mdb\pipe_segments" start;end C:\tmp\gps_pts.shp id Polyline "C:\tmp\test.gdb\facilities\pipe_cl"

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
