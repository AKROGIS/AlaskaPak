ObscurePoints.py
Created: 2010-08-30 (9.3)
Updated: 2011-01-31 (10.0)

Title:
Obscure Points

Tags:
random, sensitive, offset, hide, buffer, obscure

Summary:
Creates a new data set from sensitive point data (like cabins and eagle nests), by adding a random offset to each point, so that the new dataset can be shared with the public.

Usage:
Creates a new data set from sensitive point data (like cabins and eagle nests), by adding a random offset to each point, so that the new dataset can be shared with the public.#
Parameter 1:
Sensitive_Points
The full name of a feature class of sensitive points.
The input features must be points or multipoints.  However multipoints cannot be used if there are No-Go or Must-Go areas specified.
The spatial reference should be a projected system. Calculating distances with a geographic system introduces errors.

Parameter 2:
Obscured_Features
The name and location of the feature class to create.
If the feature class already exists. You can only overwrite it if you have set that option in the geoprocessing tab in Tools->Options menu.
The output coordinate system will be determined by the environment settings. Typically it will default to the same as the input. Click on the Environment... button and then the General Settings tab to check and set the output coordinate system.
All attributes of the sensitive features will be copied to these output features. If there is sensitive information in these attributes, then that must be removed separately.

Parameter 3:
Obscured_Feature_Type
What kind of output is desired. The default is Points.
Points:
<image>
The output will be a point or multipoint feature class to match the input. With multipoint, each of the individual points will be offset as though the feature class was individual points.
Circles:
<image>
The output feature class will be a circle (polygon) centered at the randomly offset location, with the radius of the circle equal to the Maximum Radius for the offset of center. This guarantees that the real point will fall somewhere in the circle.

Parameter 4:
Minimum_Offset
The mimimum distance that the obscured point will be from the actual point. The default is zero.
The measurement units (feet/meters) are the same as the input feature class. If the input is in lat/long (geographic), Then the units are interpreted as meters.
<image> with caption: Non-zero minimum offset
<image> with caption: Default (0) minimum offset

Parameter 5:
Maximum_Offset
The maximum distance that the obscured point will be from the actual point. The default is 500.
The measurement units (feet/meters) are the same as the input feature class. If the input is in lat/long (geographic), Then the units are interpreted as meters.

Parameter 6:
No_Go_Areas
Areas in which points will not be placed. Typically this will be water bodies, but it could be any polygon areas that would not be a logical location for the obscured points.
What to do if there is no solution???

Parameter 7:
Must_Go_Areas
Areas in which points must be placed. Typically this will be shorelines or park boundaries, but it could be any polygon areas outside of which would not be a logical location for the obscured points.
What to do if there is no solution???

Scripting Syntax:
ObscurePoints_AlaskaPak (Sensitive_Points, Obscured_Features, Obscured_Feature_Type, Minimum_Offset, Maximum_Offset, No_Go_Areas, Must_Go_Areas))

Example1:
Scripting Example
The following example shows how this script can be used in another python script, or directly in the ArcGIS Python Window.  It assumes that the script has been loaded into a toolbox, and the toolbox has been loaded into the active session of ArcGIS.
 ptFC = r"C:\tmp\gps_lines.shp"
 newPtFC = r"C:\tmp\test.gdb\park\bldg"
 mustgo = r"C:\tmp\park.shp;c:\tmp\shoreline.shp"
 nogo = r"C:\tmp\lakes.shp;c:\tmp\bldgs.shp"
 Line2Rect(ptFC, newPtFC, "Circles", 25, 100, nogo, mustgo)

Example2:
Command Line Example
The following example shows how the script can be used from the operating system command line.  It assumes that the current directory is the location of the script, and that the python interpreter is the path.
 C:\tmp> python ObscurePoints.py c:\tmp\nests.shp c:\tmp\newnests.shp Points 0 100

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