# -*- coding: utf-8 -*-
"""
Add an area attribute to one or more polygon feature classes.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

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


def add_area_to_feature(feature, units="", field_name="Area", overwrite=False):
    """Add an area attribute to a polygon feature class."""
    # TODO Document parameters in the doc string

    # Check for a feature
    if not arcpy.Exists(feature):
        utils.warn("feature not found.  Skipping...")
        return

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


def add_area_to_features(features, units="", field_name="Area", overwrite=False):
    """Add an area attribute to multiple polygon feature classes."""
    # TODO Document parameters in the doc string

    for feature in features:
        utils.info("Adding Area to {0}".format(feature))
        add_area_to_feature(feature, units, field_name, overwrite)


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
    add_area_to_features(feature_list, user_units, field_name, overwrite_field)
