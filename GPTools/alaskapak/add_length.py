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


def add_length_to_feature(feature, units, fieldname="Length", overwrite=False):
    """Add a length attribute to a single polyline or polygon feature class."""
    # TODO Document parameters in the doc string

    # TODO: addfield may alter the name of the field, but the original name is
    #       still used for calc field
    # TODO: If coordinate system is unknown, units are assumed to be units requested.
    # TODO: If coordinates are geographic, results are wrong. (the shape_length is also
    # wrong - it uses planar geometry with the spherical coordinates.)
    # TODO: Feature may be locked or un-editable
    field_names = arcpy.ListFields(feature)
    if fieldname in field_names and not overwrite:
        msg = "Aborting. Field {0} exists and overwrite is false."
        utils.warn(msg.format(fieldname))
        return

    if fieldname not in field_names:
        arcpy.AddField_management(
            feature, fieldname, "Double", "", "", "", "", "NULLABLE", "NON_REQUIRED", ""
        )
    length = "!shape.length@{0}!".format(units)
    arcpy.CalculateField_management(feature, fieldname, length, "PYTHON_9.3", "")


def add_length_to_features(features, units, fieldname="Length", overwrite=False):
    """Add a length attribute to multiple polyline or polygon feature classes."""
    # TODO Document parameters in the doc string

    for feature in features:
        utils.info("Adding Length to {0}".format(feature))
        add_length_to_feature(feature, units, fieldname, overwrite)


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
