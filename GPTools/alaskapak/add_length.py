# -*- coding: utf-8 -*-
"""
Add a length attribute to one or more polyline or polygon feature classes.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import arcpy

from . import utils


valid_units = [
    "CENTIMETERS",
    "DECIMALDEGREES",
    "DECIMETERS",
    "FEET",
    "INCHES",
    "KILOMETERS",
    "METERS",
    "MILES",
    "MILLIMETERS",
    "NAUTICALMILES",
    "POINTS",
    "UNKNOWN",
    "YARDS",
]


def add_length_to_feature(feature, units, field_name="Length", overwrite=False):
    """Add a length attribute to a single polyline or polygon feature class."""
    # TODO Document parameters in the doc string

    # TODO: If coordinate system is unknown, units are assumed to be units requested.
    # TODO: If coordinates are geographic, results are wrong. (the shape_length is also
    # wrong - it uses planar geometry with the spherical coordinates.)

    utils.info("Adding length to {0}".format(feature))

    # Verify and/or create field name
    field_name = utils.valid_field_name(field_name, feature)
    if field_name in arcpy.ListFields(feature):
        if overwrite:
            if not field_name in arcpy.ListFields(feature, field_name, "Double"):
                msg = "Field {0} exists, but is not the right type. Skipping..."
                utils.warn(msg.format(field_name))
                return
        else:
            msg = "Not allowed to overwrite existing field {0}. Skipping..."
            utils.warn(msg.format(field_name))
            return
    else:
        if arcpy.TestSchemaLock(feature):
            utils.info("Creating new field {0}".format(field_name))
            arcpy.AddField_management(feature, field_name, "Double",)
        else:
            msg = "Unable to acquire a schema lock to add the new field. Skipping..."
            utils.warn(msg)
            return

    length = "!shape.length@{0}!".format(units)
    arcpy.CalculateField_management(feature, field_name, length, "PYTHON_9.3", "")


def add_length_to_features(features, units, field_name="Length", overwrite=False):
    """Add a length attribute to multiple polyline or polygon feature classes."""
    # TODO Document parameters in the doc string

    for feature in features:
        add_length_to_feature(feature, units, field_name, overwrite)


if __name__ == "__main__":
    # TODO: this is in a package now, so it can't be called as a script.
    # TODO: if run as a script for testing, does the `from . import utils` work?
    feature_list = arcpy.GetParameterAsText(0).split(";")
    user_units = arcpy.GetParameterAsText(1)
    # TODO: what if optional parameters are not provided on the command line
    # TODO: support arcpy command line convention of "#" for None
    field_name = arcpy.GetParameterAsText(2)
    overwrite_field = arcpy.GetParameterAsText(3).lower() == "true"
    # TODO: support parameter(4) output feature class for single or remove option
    add_length_to_features(feature_list, user_units, field_name, overwrite_field)
