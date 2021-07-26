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


def lake_volume(shoreline, depth_points, lakes, surface):
    """Creates lakes and surface from shoreline and depth_points"""

    # Check out any necessary licenses
    arcpy.CheckOutExtension("3D")

    # Local variables:
    lakes_temp = surface
    lakes_temp2 = lakes_temp
    output_layer = shoreline
    output_layer_name = output_layer
    output_with_depth = output_layer_name
    output_with_depth2 = output_with_depth
    output_dataset = depth_points

    # Process: Merge
    arcpy.Merge_management(depth_points, output_dataset, "")

    # Process: Make Feature Layer
    arcpy.MakeFeatureLayer_management(
        shoreline,
        output_layer,
        "",
        "",
        (
            "FID FID VISIBLE NONE;Shape Shape VISIBLE NONE;OBJECTID OBJECTID VISIBLE NONE;"
            "SHAPE_Leng SHAPE_Leng VISIBLE NONE;SHAPE_Area SHAPE_Area VISIBLE NONE;"
            "PONDNAME PONDNAME VISIBLE NONE"
        ),
    )

    # Process: Select Layer By Location
    arcpy.SelectLayerByLocation_management(
        output_layer, "INTERSECT", output_dataset, "", "NEW_SELECTION"
    )

    if arcpy.TestSchemaLock(output_layer_name):
        new_field_name = "xx_depth"
        utils.info("Creating new field {0}".format(new_field_name))
        arcpy.AddField_management(output_layer_name, new_field_name, "Double")
    else:
        msg = "Unable to acquire a schema lock to add the new field. Skipping..."
        utils.warn(msg)
        return

    # Process: Calculate Field
    arcpy.CalculateField_management(output_with_depth, "xx_depth", "0", "VB", "")

    # Process: Create TIN
    arcpy.CreateTin_3d(
        surface,
        "",
        "# Depth masspoints <None>;DENA_SamplingLakes_Digitized xx_depth hardclip <None>",
        "DELAUNAY",
    )

    # Process: Polygon Volume (2)
    arcpy.PolygonVolume_3d(
        surface, output_with_depth2, "xx_depth", "ABOVE", "Volume", "SArea", "0"
    )

    # Process: Delete Field
    arcpy.DeleteField_management(lakes_temp, "xx_depth")

    # Process: Copy Features
    arcpy.CopyFeatures_management(lakes_temp2, lakes, "", "0", "0", "0")


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
    if not arg_count == 4:
        usage = "Usage: {0} shore_lines depth_points lakes surface"
        utils.die(usage.format(sys.argv[0]))

    # TODO: check parameters.
    # depth points can be a list of point feature classes that will be merged

    return args


if __name__ == "__main__":
    # Set command line or simple testing
    # sys.argv[1:] = ["TODO Make test case"]
    utils.execute(lake_volume, parameter_fixer)
