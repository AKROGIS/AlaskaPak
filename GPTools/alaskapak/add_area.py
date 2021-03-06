# -*- coding: utf-8 -*-
"""
Add an area attribute to one or more polygon feature classes.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import sys

import arcpy

from . import utils

valid_units = [
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

    # Get some info about the feature
    feature_description = arcpy.Describe(feature)
    shape_name = feature_description.shapeFieldName
    feature_sr = feature_description.spatialReference
    feature_is_projected = (
        feature_sr.type == "Projected" and feature_sr.name != "Unknown"
    )
    feature_is_polygon = feature_description.shapeType != "Polygon"

    # Validate Feature - We only work on polygons
    if not feature_is_polygon:
        utils.warn("feature is not a polygon.  Skipping...")
        return

    # Verify or create field name
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
        new_field_name = field_name
    else:
        if arcpy.TestSchemaLock(feature):
            new_field_name = utils.valid_field_name(field_name, feature)
            utils.info("Creating new field {0}".format(new_field_name))
            arcpy.AddField_management(feature, new_field_name, "Double",)
        else:
            msg = "Unable to acquire a schema lock to add the new field. Skipping..."
            utils.warn(msg)
            return

    # TODO: Handle units = None

    # Sanitize Units
    if units.upper() in valid_units:
        out_units = "@{0}".format(units.upper())
    else:
        msg = "Unknown units {0}, area will be in the feature's units."
        utils.warn(msg.format(units))
        out_units = ""

    # Determine Area Calculation Method
    if feature_is_projected:
        area_method = ".area"
    else:
        if out_units:
            area_method = ".geodesicArea"
            utils.info("Calculating geodesic area for {0}".format(feature))
        else:
            area_method = ".area"
            utils.warn(
                "Calculating area in square degrees." "This is usually meaningless."
            )

    # Do Calculation
    calculation = "!{0}{1}{2}!".format(shape_name, area_method, out_units)
    arcpy.CalculateField_management(feature, new_field_name, calculation, "PYTHON_9.3")


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
        utils.info("Adding Area to {0}".format(feature))
        add_area_to_feature(feature, units, field_name, overwrite)


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
        field_name = "Area"

    # validate overwrite
    if overwrite == "#":
        overwrite = False

    return [features, units, field_name, overwrite]


def add_area_commandline():
    """Parse and validate command line arguments then add area to features."""
    args = toolbox_validation()
    add_area_to_features(*args)


if __name__ == "__main__":
    # For testing
    # Change `from . import utils` to `import utils` to run as a script
    add_area_commandline()
