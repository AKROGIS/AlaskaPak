# -*- coding: utf-8 -*-
"""
ArcGIS Tool Classes for a Python Toolbox.

Compatible with Python 2.7 and 3.5+ (ArcGIS 10.x and Pro)

The tool class must meet specific requirements expected by the ArcGIS host.
See https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/
    defining-a-tool-in-a-python-toolbox.htm
for details.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import arcpy

import add_area

# pylint: disable=invalid-name,no-self-use,unused-argument
# Framework requirement of the class violate pylint standards.

# pylint: disable=useless-object-inheritance
# required for Python 2/3 compatibility


class AddAreaMultiple(object):
    """A tool to add an Area column to multiple polygon feature classes."""

    def __init__(self):
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        features = arcpy.Parameter(
            name="features",
            displayName="Input Features",
            direction="Input",
            datatype="GPFeatureLayer",
            parameterType="Required",
            multiValue=True,
        )
        features.filter.list = ["Polygon"]

        field_name = arcpy.Parameter(
            name="field_name",
            displayName="Field name",
            direction="Input",
            datatype="Field",
            parameterType="Optional",
        )
        field_name.value = "Area"

        units = arcpy.Parameter(
            name="units",
            displayName="Areal Units",
            direction="Input",
            datatype="GPString",
            parameterType="Optional",
        )
        units.filter.list = add_area.valid_units

        overwrite = arcpy.Parameter(
            name="overwrite",
            displayName="Overwrite Existing Values",
            direction="Input",
            datatype="GPBoolean",
            parameterType="Optional",
        )

        parameters = [features, field_name, units, overwrite]
        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """
        Modify the values and properties of parameters before internal
        validation is performed.

        This method is called whenever a parameter has been changed.
        """
        return

    def updateMessages(self, parameters):
        """
        Modify the messages created by internal validation for each tool parameter.

        This method is called after internal validation.
        """
        return

    def execute(self, parameters, messages):
        """Get the parameters and execute the task of the tool."""
        features = parameters[0].value
        units = parameters[1].valueAsText
        fieldname = parameters[2].valueAsText
        overwrite = parameters[3].value
        add_area.add_area_to_features(features, units, fieldname, overwrite)


class AddAreaSingle(object):
    """A tool to add an Area column to multiple polygon feature classes."""

    def __init__(self):
        self.canRunInBackground = True

    def getParameterInfo(self):
        """Define parameter definitions"""
        feature = arcpy.Parameter(
            name="feature",
            displayName="Input Feature",
            direction="Input",
            datatype="GPFeatureLayer",
            parameterType="Required",
        )
        feature.filter.list = ["Polygon"]

        field_name = arcpy.Parameter(
            name="field_name",
            displayName="Field name",
            direction="Input",
            datatype="Field",
            parameterType="Optional",
        )
        field_name.value = "Area"
        field_name.parameterDependencies = [feature.name]
        field_name.filter.list = ["Double"]

        units = arcpy.Parameter(
            name="units",
            displayName="Areal Units",
            direction="Input",
            datatype="GPString",
            parameterType="Optional",
        )
        units.filter.list = add_area.valid_units

        overwrite = arcpy.Parameter(
            name="overwrite",
            displayName="Overwrite Existing Values",
            direction="Input",
            datatype="GPBoolean",
            parameterType="Optional",
        )

        out_feature = arcpy.Parameter(
            name="out_feature",
            displayName="Output Feature",
            direction="Output",
            datatype="GPFeatureLayer",
            parameterType="Derived",
        )
        out_feature.parameterDependencies = [feature.name]
        out_feature.schema.clone = True

        parameters = [feature, field_name, units, overwrite, out_feature]
        return parameters

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """
        Modify the values and properties of parameters before internal
        validation is performed.

        This method is called whenever a parameter has been changed.
        """
        if parameters[0].altered:
            parameters[1].value = arcpy.ValidateFieldName(
                parameters[1].value, parameters[0].value
            )

    def updateMessages(self, parameters):
        """
        Modify the messages created by internal validation for each tool parameter.

        This method is called after internal validation.
        """
        return

    def execute(self, parameters, messages):
        """Get the parameters and execute the task of the tool."""
        feature = parameters[0].valueAsText
        units = parameters[1].valueAsText
        field_name = parameters[2].valueAsText
        overwrite = parameters[3].value
        add_area.add_area_to_feature(feature, units, field_name, overwrite)
