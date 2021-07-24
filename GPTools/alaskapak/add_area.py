# -*- coding: utf-8 -*-
"""
Add an area attribute to one or more polygon feature classes.
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


valid_units_pretty = [
    "Acres",
    "Ares",
    "Hectares",
    "Square Centimeters",
    "Square Decimeters",
    "Square Inches",
    "Square Feet",
    "Square Kilometers",
    "Square Meters",
    "Square Miles",
    "Square Millimeters",
    "Square Yards",
]

valid_units = [units.upper().replace(" ", "") for units in valid_units_pretty]


def add_area_to_feature(feature, units=None, field_name="Area", overwrite=False):
    """Add an area attribute to a polygon feature class.

    Args:
        feature (text): A path to an ArcGIS polygon feature classes.
        units (text, optional): The areal units for the calculated area.
          must be one of `valid_units`. If None, the square units of the feature
          class will be used. Defaults to None.
        field_name (text, optional): The name of the field to store the
          calculated area. Defaults to "Area".
        overwrite (bool, optional): If True, then we are allowed to overwrite
          any existing values in the field named `field_name`. Defaults to False.

    Returns:
        None
    """
    print_units = units if units is not None else "feature's units"
    utils.info("Adding {0} (in {1}) to {2}".format(field_name, print_units, feature))

    # Verify or create field name
    field_names = [field.name for field in arcpy.ListFields(feature)]
    if field_name in field_names:
        if overwrite:
            if not arcpy.ListFields(feature, field_name, "Double"):
                msg = "Field {0} exists, but is not the right type. Skipping..."
                utils.warn(msg.format(field_name))
                return
        else:
            msg = "Not allowed to overwrite existing field {0}. Skipping..."
            utils.warn(msg.format(field_name))
            return
        new_field_name = field_name
    else:
        if arcpy.TestSchemaLock(feature):
            new_field_name = utils.valid_field_name(field_name, feature)
            utils.info("Creating new field {0}".format(new_field_name))
            arcpy.AddField_management(feature, new_field_name, "Double")
        else:
            msg = "Unable to acquire a schema lock to add the new field. Skipping..."
            utils.warn(msg)
            return

    description = arcpy.Describe(feature)
    geometry_name = description.shapeFieldName
    spatial_reference = description.spatialReference
    if spatial_reference.type == "Geographic":
        utils.warn("Calculating area on geographic data is usually suspect.")

    if units is None:
        area = "!{0}.area!".format(geometry_name)
    else:
        if spatial_reference.type == "Geographic":
            area = "!{0}.geodesicArea@{1}!".format(geometry_name, units)
        else:
            area = "!{0}.area@{1}!".format(geometry_name, units)

    # For the !shape! calculation, the expression type must be python.
    # In Pro, the default is "PYTHON3" (ok), but in 10.x, the default is "VB"
    # Need to explicitly use "PYTHON_9.3" in 10.x
    expression_type = "PYTHON3"
    if sys.version_info[0] < 3:
        expression_type = "PYTHON_9.3"

    arcpy.CalculateField_management(feature, new_field_name, area, expression_type)


def add_area_to_features(features, units=None, field_name="Area", overwrite=False):
    """Add an area attribute to a polygon feature class.

    Args:
        features (list[text]): A list of paths to ArcGIS polygon feature classes.
        units (text, optional): The areal units for the calculated length.
          must be one of `valid_units`. If None, the square units of the feature
          class will be used. Defaults to None.
        field_name (text, optional): The name of the field to store the
          calculated area. Defaults to "Area".
        overwrite (bool, optional): If True, then we are allowed to overwrite
          any existing values in the field named `field_name`. Defaults to False.

    Returns:
        None
    """

    for feature in features:
        add_area_to_feature(feature, units, field_name, overwrite)


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

    # pylint: disable=too-many-branches

    arg_count = len(args)
    if arg_count < 1 or arg_count > 4:
        usage = "Usage: {0} features [units] [field_name] [overwrite]"
        utils.die(usage.format(sys.argv[0]))

    if arg_count < 4 or not args[3]:
        overwrite = "#"
    else:
        overwrite = args[3]
    if arg_count < 3 or not args[2]:
        field_name = "#"
    else:
        field_name = args[2]
    if arg_count < 2 or not args[1]:
        units = "#"
    else:
        units = args[1]
    feature_list = args[0]

    # validate features
    features = []
    for feature in feature_list.split(";"):
        if feature[0] == "'" and feature[-1] == "'":
            feature = feature[1:-1]
        if arcpy.Exists(feature):
            if arcpy.Describe(feature).shapeType == "Polygon":
                features.append(feature)
            else:
                msg = "Feature class ({0}) is not polygons. Skipping."
                utils.warn(msg.format(feature))
        else:
            utils.warn("Feature class ({0}) not found. Skipping.".format(feature))
    if not features:
        utils.die("No features found.")

    # validate units
    if units == "#":
        units = None
    if units and units.upper() not in valid_units:
        msg = "Unknown units '{0}'. Area will be in the feature's units."
        utils.warn(msg.format(units))
        units = None

    # validate field_name
    if field_name == "#":
        field_name = "Area"

    # validate overwrite
    if overwrite == "#":
        overwrite = False
    else:
        overwrite = overwrite.upper() in ["TRUE", "YES", "ON"]

    return [features, units, field_name, overwrite]


if __name__ == "__main__":
    # Set command line or simple testing
    # sys.argv[1:] = ["C:/tmp/akr_facility.gdb/PARKLOTS_PY", "Acres", "#", "No"]
    utils.execute(add_area_to_features, parameter_fixer)
