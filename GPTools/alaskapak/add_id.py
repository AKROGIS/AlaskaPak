# -*- coding: utf-8 -*-
"""
Add a unique integer id to one or more feature classes.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

import arcpy

from . import utils


def toolbox_validation():
    """Exits with an error message if the command line arguments are not valid.

    Provides the same default processing and validation for command line scripts
    that the ArcGIS toolbox framework provides.  It does not do all possible
    validation and error checking, see the validation option of the main function.

    Returns:
        A list of validated command line parameters.
    """

    # pylint: disable=too-many-branches

    arg_count = len(sys.argv)
    if arg_count < 2 or arg_count > 6:
        usage = (
            "Usage: {0} features [id_field_name] [start] "
            "[increment] [sort_field_name]"
        )
        utils.die(usage.format(sys.argv[0]))

    if arg_count < 6:
        sort_field_name = "#"
    else:
        sort_field_name = arcpy.GetParameterAsText(4)
    if arg_count < 5:
        increment = "#"
    else:
        increment = arcpy.GetParameterAsText(3)
    if arg_count < 4:
        start = "#"
    else:
        start = arcpy.GetParameterAsText(2)
    if arg_count < 3:
        id_field_name = "#"
    else:
        id_field_name = arcpy.GetParameterAsText(1)
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

    # validate id_field_name
    if id_field_name == "#":
        id_field_name = "UniqueID"

    # validate start
    if start == "#":
        start = 1
    else:
        try:
            start = int(start)
        except ValueError:
            utils.die("Start ({0}) is not an integer.".format(start))

    # validate increment
    if increment == "#":
        increment = 1
    else:
        try:
            increment = int(increment)
        except ValueError:
            utils.die("Increment ({0}) is not an integer.".format(increment))

    # validate sort_field_name
    if sort_field_name == "#":
        sort_field_name = None

    return [features, id_field_name, start, increment, sort_field_name]


def add_id_to_features(
):
    """Add id to multiple feature classes."""

    for feature_class in feature_classes:


def add_id_to_feature(
):
    """Add id to a feature class."""

    utils.info("Adding {0} to {2}".format(field_name, feature_class))
    field_names = [field.name for field in arcpy.ListFields(feature_class)]
    id_field_name = utils.valid_field_name(field_name, feature_class)
    if id_field_name not in field_names:
        if arcpy.TestSchemaLock(feature_class):
            utils.info("Creating new field {0}".format(id_field_name))
            arcpy.AddField_management(feature_class, id_field_name, "Long")
        else:
            msg = "Unable to acquire a schema lock to add the new field. Skipping..."
            utils.warn(msg)
            return

    order_by = None
    if sort_field_name:
        if sort_field_name not in field_names:
            msg = "Sort field `{0}` not in {1}. Ignoring"
            utils.warn(msg.format(sort_field_name, feature_class))
        else:
            if arcpy.describe(feature_class).dataType == "ShapeFile":
                utils.warn("Shapefiles do not support sort fields. Ignoring")
            else:
                order_by = "ORDER BY {0}".format(sort_field_name)

    feature_id = start
    with arcpy.da.UpdateCursor(
        feature_class, [id_field_name], sql_clause=(None, order_by)
    ) as cursor:
        for row in cursor:
            row[0] = feature_id
            feature_id += increment
            cursor.updateRow(row)


def add_id_commandline():
    """Parse and validate command line arguments then add id to features."""
    args = toolbox_validation()
    add_id_to_features(*args)


if __name__ == "__main__":
    # For testing
    # Change `from . import utils` to `import utils` to run as a script
    add_id_commandline()
