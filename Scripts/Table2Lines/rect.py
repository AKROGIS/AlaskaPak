# ---------------------------------------------------------------------------
# Line2Rect.py
# Created: 2011-01-14
# Author: Regan Sarwas, National Park Service
#
# Builds a polygon feature class containing rectangles derived from a line
# feature class.  The line is used as the base of the rectangle, and an
# attribute in the line feature class provides the height.  If the height is
# positive, the rectangle is drawn on the right side of the line.  If it is
# negative it is drawn on the left side.  Right and left are determined by the
# order of the vertices in the line.
#
# * The input lines features can have any number of parts, and any number of
# vertices in each part, however only the first and last vertex are used in
# the output rectangle.  If the input shape is a multipart, then the output
# shape is also multipart.
# * The offset must be a numeric field, and it will be interpreted as a double
# in the same units/coordinate system as the line feature class.
# * All attributes of the line feature class are copied forward to the output
# feature class.
# * The output feature class must not exist unless the user's environment is
# set to allow overwrite
#
# Usage:
# python Line2Rect.py path_to_lineFC Offset_Field_Name path_to_outputFC
#
# Example:
# python Line2Rect.py "c:\tmp\gps_lines.shp" "width" "c:\tmp\test.gdb\park\bldg"
#
# License:
# Public Domain
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
# ---------------------------------------------------------------------------

import os
import math

class Point:
    def __init__(self, x, y):
        self.X = x
        self.Y = y

    def __str__(self):
        return "("+str(self.X)+","+str(self.Y)+")"

def MakeRect(pt1, pt2, width):
    """Assumes pt1 and pt2 are arcpy.Points, and width is numeric.
    Returns a tuple of the next two points in the rectangle.
    Points proceed clockwise for a positive width and
    counterclockwise for a negative width."""
    dx = pt2.X - pt1.X
    dy = pt2.Y - pt1.Y
    length = math.sqrt(dx*dx + dy*dy)
    angle = math.atan2(dy,dx)
    # rotate 90 degree to the right
    angle = angle - math.pi/2.0
    y = width * math.sin(angle)
    x = width * math.cos(angle)
    pt3 = Point(pt2.X + x, pt2.Y + y)
    pt4 = Point(pt1.X + x, pt1.Y + y)
    return (pt3,pt4)


pt1 = Point(-1.0,-1.0)
pt2 = Point(-1.0,-4.0)
dist = -2.0
pt3,pt4 = MakeRect(pt1, pt2, dist)
print pt1, pt2, pt3, pt4

    