# -*- coding: utf-8 -*-
"""
Calculates the volume of lakes

Created by Regan Sarwas on 2010-12-14

Calculates the volume of a set of lakes based on depth samples (points) within
the polygon defined by the shoreline.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

import arcpy

if __name__ == "__main__":
    # for use as a command line script and with old style ArcGIS toolboxes (*.tbx)
    import utils
else:
    # for use as a module and Python toolboxes (*.pyt)
    from . import utils


def lake_volume(shoreline, depth_points, depth_field_name, lakes, surface):
    """Creates a bottom surface and volume from a shoreline and depth_points.

    Args:
        shoreline (text): the input polygon features that define the shoreline;
            will be copied to lakes
        depthpoints (text): A semicolon separated list of point feature class that
            have the depth of the lakes at various locations. All feature classes
            must have a DOUBLE column with the name
        depth_field_name (text): the name of a field in depthpoints with a DOUBLE
            representing the depth at that point.
        lakes (text): An output feature class, based on shoreline, with the added
            columns of Volume, and SurfaceArea, for the volume of the lake and the
            bottom's surface area respectively.
        surface (text): An output TIN dataset representing the bottom of the lake
    """

    # Check out any necessary licenses
    arcpy.CheckOutExtension("3D")

    # New field names in output
    shoreline_depth_field_name = "xx_depth" # temporary; assumed 0 needed for calcs
    volume_field_name = "Volume"
    surface_area_field_name = "SArea"

    # Merge all the input depth points
    all_points = "in_memory\\depth"
    arcpy.Merge_management(depth_points, all_points, "")

    # Copy the input to the output
    arcpy.management.CopyFeatures(shoreline, lakes)

    #Add a shoreline depth of zero to the output features
    # No need to test for a schema lock on an in_memory feature class
    arcpy.AddField_management(lakes, shoreline_depth_field_name, "Double")
    # The default expression type is Python3 for Pro and VB for 10.x
    # The expression "0" is valid in both those languages
    arcpy.CalculateField_management(lakes, shoreline_depth_field_name, "0")

    # Create a TIN of the lake bottom
    params = "{0} {1} masspoints;{2} {3} hardclip".format(
        all_points,
        depth_field_name,
        lakes,
        shoreline_depth_field_name
    )
    arcpy.CreateTin_3d(surface, "", params, "DELAUNAY",
    )

    # Add the volume and surface area to the output
    arcpy.PolygonVolume_3d(
        surface, lakes, shoreline_depth_field_name, "ABOVE", volume_field_name, surface_area_field_name, "0"
    )

    # Remove the temporary field from the output
    arcpy.DeleteField_management(lakes, shoreline_depth_field_name)


def parameter_fixer(args):
    """Validates and transforms the command line arguments for the task.

    1) Converts text values from old style toolbox (*.tbx) parameters (or the
       command line) to the python object arguments expected by the primary task
       of the script, and as provided by the new style toolbox (*.pyt).
    2) Validates the correct number of arguments.
    3) Provides default values for command line options provided as "#"
       or missing from the end of the command line.
    4) Provides additional validation for command line parameters to match the
       validation done by the toolbox interface.  This isn't required when
       called by an old style toolbox, but it isn't possible to tell it is
       called by the toolbox or by the command line.

    Args:
        args (list[text]): A list of commands arguments, Usually obtained
        from the sys.argv or arcpy.GetParameterAsText().  Provide "#" as
        placeholder for an unspecified intermediate argument.

    Returns:
        A list of validated arguments expected by the task being called.
        Exits with an error message if the args cannot be transformed.
    """

    arg_count = len(args)
    if not arg_count == 5:
        usage = "Usage: {0} shore_lines depth_points fieldname lakes surface"
        utils.die(usage.format(sys.argv[0]))

    # TODO: check parameters.
    # depth points can be a list of point feature classes that will be merged

    return args


if __name__ == "__main__":
    # Set command line or simple testing
    # sys.argv[1:] = ["TODO Make test case"]
    utils.execute(lake_volume, parameter_fixer)
