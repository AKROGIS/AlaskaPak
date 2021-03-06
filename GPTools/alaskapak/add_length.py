# -*- coding: utf-8 -*-
"""
Add a length attribute to one or more polyline or polygon feature classes.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

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


def add_length_to_feature(feature, units=None, field_name="Length", overwrite=False):
    """Add a length attribute to a single polyline or polygon feature class.

    Args:
        feature (text): The path to an ArcGIS feature class.
        units (text, optional): The linear units for the calculated length.
          must be one of `valid_units`. If None, the units of the feature
          class will be used. Defaults to None.
        field_name (text, optional): The name of the field to store the
          calculated length. Defaults to "Length".
        overwrite (bool, optional): If True, then we are allowed to overwrite
          any existing values in the field named `field_name`. Defaults to False.

    Returns:
        None
    """
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

    # TODO See add_area for handling geographic `shape.geodesicLength@`

    if units is None:
        length = "!shape.length!"
    else:
        length = "!shape.length@{0}!".format(units)
    arcpy.CalculateField_management(feature, field_name, length, "PYTHON_9.3", "")


def add_length_to_features(features, units=None, field_name="Length", overwrite=False):
    """Add a length attribute to multiple polyline or polygon feature classes.

    Args:
        features (list[text]): A list of paths to ArcGIS feature classes.
        units (text, optional): The linear units for the calculated length.
          must be one of `valid_units`. If None, the units of the feature
          class will be used. Defaults to None.
        field_name (text, optional): The name of the field to store the
          calculated length. Defaults to "Length".
        overwrite (bool, optional): If True, then we are allowed to overwrite
          any existing values in the field named `field_name`. Defaults to False.

    Returns:
        None
    """
    for feature in features:
        add_length_to_feature(feature, units, field_name, overwrite)


def toolbox_validation():
    """Exits with an error message if the command line arguments are not valid.

    Provides the same default processing and validation for command line scripts
    that the ArcGIS toolbox framework provides.  It does not do all possible
    validation and error checking.

    Returns:
        A list of validated command line parameters.
    """

    # pylint: disable=too-many-branches

    if len(sys.argv) < 2 or len(sys.argv) > 5:
        usage = (
            "Usage: {0} features [units] [field_name] [overwrite]"
        )
        utils.die(usage.format(sys.argv[0]))

    if sys.argv < 5:
        overwrite = "#"
    else:
        overwrite = arcpy.GetParameterAsText(3)
    if sys.argv < 4:
        field_name = "#"
    else:
        field_name = arcpy.GetParameterAsText(2)
    if sys.argv < 3:
        units = "#"
    else:
        units = arcpy.GetParameterAsText(1)
    feature_list = arcpy.GetParameterAsText(0)

    # validate features
    features = []
    for feature in feature_list.split(";"):
        if feature == "'" and feature[-1] == "'":
            feature = feature[1:-1]
        if arcpy.Exists(feature):
            features.append(feature)
        else:
            utils.warn("Feature class ({0}) not found. Skipping.".format(feature))
    if not features:
        utils.die("No features found.")

    # validate units
    if units == "#":
        units = None

    # validate field_name
    if field_name == "#":
        field_name = "Length"

    # validate overwrite
    if overwrite == "#":
        overwrite = False

    return [features, units, field_name, overwrite]


def add_length_commandline():
    """Parse and validate command line arguments then add length to features."""
    args = toolbox_validation()
    add_length_to_features(*args)


if __name__ == "__main__":
    # For testing
    # Change `from . import utils` to `import utils` to run as a script
    add_length_commandline()
