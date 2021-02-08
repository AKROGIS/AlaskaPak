# -*- coding: utf-8 -*-
"""
ArcGIS Toolbox/Tool Classes for the AlaskaPak Tools.

Compatible with Python 2.7 and 3.5+ (ArcGIS 10.2+ and Pro 2.0+)

The toolbox class must meet specific requirements expected by the ArcGIS host.
See https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/
    a-template-for-python-toolboxes.htm
for details.
The tool class must meet specific requirements expected by the ArcGIS host.
See https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/
    defining-a-tool-in-a-python-toolbox.htm
for details.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import imp

import arcpy

import alaskapak

# When a Python toolbox is refreshed, only the Python toolbox file is refreshed;
# any modules that are imported within the toolbox are not.
# To reload a module from within a Python toolbox (during development),
# use the importlib module's reload function.
imp.reload(alaskapak)
# imp works on Python 2.7 and 3.x, however it has be deprecated as of
# Python 3.4 and replaced by importlib
# import importlib
# importlib.import_module(alaskapak)

# pylint: disable=invalid-name,no-self-use,unused-argument,too-few-public-methods
# Framework requirement of the class violate pylint standards.

# pylint: disable=useless-object-inheritance
# required for Python 2/3 compatibility



class Toolbox(object):
    """
    Define the toolbox.

    The name of the toolbox is the name of the .pyt file.
    The label is the display name for the toolbox as shown in the Geoprocessing pane.
    The alias is ??
    The description is shown in the Geoprocessing pane.
    """

    def __init__(self):
        self.label = "AlaskaPak Toolbox"
        self.alias = "AlaskaPak"
        self.description = "A collection of GIS tools for the Alaska Region."

        # List of tool classes associated with this toolbox
        self.tools = [
            AddAreaMultiple,
            AddAreaSingle,
            AddLengthSingle,
            AddLengthMultiple,
            AddUniqueID,
            AddIdMultiple,
            AddXYSingle,
            AddXYMultiple,
            Buildings,
            LineToRectangle,
            PointsToPolygon,
            PolygonFromPoint,
            RandomizePoints,
            ObscurePoints,
            RandomTransects,
            TableToShape,
        ]


class AddAreaMultiple(object):
    """A tool to add an Area column to multiple polygon feature classes."""

    def __init__(self):
        self.label = "Add Area (Multiple)"
        self.description = "Add an area attribute to multiple polygon feature Classes"
        self.category = "Add Attributes"
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
        units.filter.list = alaskapak.valid_units

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
        fieldname = parameters[1].valueAsText
        units = parameters[2].valueAsText
        overwrite = parameters[3].value
        alaskapak.add_area_to_features(features, units, fieldname, overwrite)


class AddAreaSingle(object):
    """A tool to add an Area column to multiple polygon feature classes."""

    def __init__(self):
        self.label = "Add Area (Single)"
        self.description = "Add an area attribute to polygon features"
        self.category = "Add Attributes"
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
        units.filter.list = alaskapak.valid_units

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
        field_name = parameters[1].valueAsText
        units = parameters[2].valueAsText
        overwrite = parameters[3].value
        # TODO: Support or drop the out feature parameter (4)
        alaskapak.add_area_to_feature(feature, units, field_name, overwrite)


class AddLengthSingle(object):
    """A tool to add an Area column to multiple polygon feature classes."""

    def __init__(self):
        self.label = "Add Length (Single)"
        self.description = "Add a length attribute to a single polyline feature Class"
        self.category = "Add Attributes"
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
        # Features (required) - polyline or polygon (perimeter)
        # Field Name - required text - default = Miles
        # Units - optional, default = Miles - Picklist


        parameters = [features]
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
        alaskapak.add_area_to_features(features)


class AddLengthMultiple(object):
    """A tool to add a length attribute to multiple polyline feature Classes."""

    def __init__(self):
        self.label = "Add Area (Multiple)"
        self.description = "Add a length attribute to multiple polyline feature Classes"
        self.category = "Add Attributes"
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


        parameters = [features]
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
        alaskapak.add_area_to_features(features)


class AddUniqueID(object):
    """A tool to add an Area column to multiple polygon feature classes."""

    def __init__(self):
        self.label = "Add Unique ID (Single)"
        self.description = "Add an area attribute to multiple polygon feature Classes"
        self.category = "Add Attributes"
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
        # Data Sets (required)
        # (the rest are optional)
        # Field Name - Default "UniqueID"
        # Starting Value - default 1 (int)
        # Increment - default 1 (int)
        # Sort Field - no default

        parameters = [features]
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
        alaskapak.add_area_to_features(features)


class AddIdMultiple(object):
    """A tool to add a X and Y columns to multiple polygon feature classes."""

    def __init__(self):
        self.label = "Add Unique Id (Multiple)"
        self.description = "Add an area attribute to multiple polygon feature Classes"
        self.category = "Add Attributes"
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


        parameters = [features]
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
        alaskapak.add_area_to_features(features)


class AddXYSingle(object):
    """A tool to add a X and Y columns to multiple polygon feature classes."""

    def __init__(self):
        self.label = "Add XY (Single)"
        self.description = "Add an area attribute to multiple polygon feature Classes"
        self.category = "Add Attributes"
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
        # (all required)
        # Point Feature Class
        # Spatial Reference
        # X Field Name (Longitude, Easting) - Default Lon
        # Y Field Name (Latitude, Northing) - Default Lat


        parameters = [features]
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
        alaskapak.add_area_to_features(features)


class AddXYMultiple(object):
    """A tool to add a X and Y columns to multiple polygon feature classes."""

    def __init__(self):
        self.label = "Add XY (Multiple)"
        self.description = "Add an area attribute to multiple polygon feature Classes"
        self.category = "Add Attributes"
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


        parameters = [features]
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
        alaskapak.add_area_to_features(features)


class Buildings(object):
    """A tool to add a X and Y columns to multiple polygon feature classes."""

    def __init__(self):
        self.label = "Create Square Buildings"
        self.description = "Add an area attribute to multiple polygon feature Classes"
        self.category = "Polygon Generation"
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
        # Building Edges - input line feature class
        # Building Polygon - output feature class


        parameters = [features]
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
        alaskapak.add_area_to_features(features)


class LineToRectangle(object):
    """A tool to add a X and Y columns to multiple polygon feature classes."""

    def __init__(self):
        self.label = "Line to Rectangle"
        self.description = "Create a Rectangle from one side (line) and offset"
        self.category = "Polygon Generation"
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
        # Line features - layer
        # rectangle width field
        # rectangle features - output feature class

        parameters = [features]
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
        alaskapak.add_area_to_features(features)


class PointsToPolygon(object):
    """A tool to add a X and Y columns to multiple polygon feature classes."""

    def __init__(self):
        self.label = "Points to Polygon"
        self.description = "Creates polygons from points on the perimeters"
        self.category = "Polygon Generation"
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
        # Point features - layer
        # polygon features - output feature class
        # polygon Id field
        # sort field

        parameters = [features]
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
        alaskapak.add_area_to_features(features)


class PolygonFromPoint(object):
    """A tool to add a X and Y columns to multiple polygon feature classes."""

    def __init__(self):
        self.label = "Polygons from Control Point"
        self.description = "Creates polygons from control point and a set of azimuths and distances"
        self.category = "Polygon Generation"
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
        # control point features layer
        # control point id field
        # azimuth distance tableview
        # polygon id field
        # group field optional
        # sort field optional
        # azimuth field optional
        # distance field optional
        # polygon features - output


        parameters = [features]
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
        alaskapak.add_area_to_features(features)


class RandomizePoints(object):
    """A tool to add a X and Y columns to multiple polygon feature classes."""

    def __init__(self):
        self.label = "Randomize Points"
        self.description = "Adds a random offset to a point to protect sensitive data"
        self.category = "Randomize"
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
        # Sensitive Points - input point feature layer
        # Obsured Features - output feature class
        # minimum offset - double default 0
        # maximum offset - double 500 feature class units
        # no go areas - multiple polygon feature classes
        # must go areas - multiple polygon features


        parameters = [features]
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
        alaskapak.add_area_to_features(features)


class ObscurePoints(object):
    """A tool to add a X and Y columns to multiple polygon feature classes."""

    def __init__(self):
        self.label = "Obscure Points"
        self.description = "Replaces a point within a random circle to protect sensitive data"
        self.category = "Randomize"
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
        # Sensitive Points - input point feature layer
        # Obsured Features - output feature class
        # minimum offset - double default 0
        # maximum offset - double 500 feature class units
        # no go areas - multiple polygon feature classes
        # must go areas - multiple polygon features

        parameters = [features]
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
        alaskapak.add_area_to_features(features)


class RandomTransects(object):
    """A tool to add a X and Y columns to multiple polygon feature classes."""

    def __init__(self):
        self.label = "Random Transects"
        self.description = "Creates random survey transects (lines) within a polygon boundary."
        self.category = "Randomize"
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
        # Polygon Boundaries - input polygon feature layer
        # New Transects - output feature class
        # transects per boundary - Long - default 5
        # minimum length - linear unit (numerical text box and units picklist)
        # maximum length - linear unit
        # maximum attempts - long default 100
        # Allow overlap - Boolean - default True


        parameters = [features]
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
        alaskapak.add_area_to_features(features)


class TableToShape(object):
    """A tool to add a X and Y columns to multiple polygon feature classes."""

    def __init__(self):
        self.label = "Table to Shape"
        self.description = "Creates a feature from a point file and tabuar shape description"
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
        # Table - TableView - required
        # VertexList  - Multiple Value (list of fields in Table)
        # Points - Feature Layer
        # Point_ID - Field
        # Geometry - String (Polyline, Polygon, multipoint - picklist)
        # Output Feature Class - Feature Class


        parameters = [features]
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
        alaskapak.add_area_to_features(features)
