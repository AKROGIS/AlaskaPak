# -*- coding: utf-8 -*-
"""
ArcGIS Toolbox Class for a Python Toolbox.

Compatible with Python 2.7 and 3.5+ (ArcGIS 10.x and Pro)

The toolbox class must meet specific requirements expected by the ArcGIS host.
See https://pro.arcgis.com/en/pro-app/latest/arcpy/geoprocessing_and_python/
    a-template-for-python-toolboxes.htm
for details.
"""

from __future__ import absolute_import, division, print_function, unicode_literals

import imp

import add_area_tool

# In of ArcGIS 10.2, the tool classes must be in this file
# TODO: Does ArcGIS 10.6+ and Pro support Tool classes in imported files?

# When a Python toolbox is refreshed, only the Python toolbox file is refreshed;
# any modules that are imported within the toolbox are not.
# To reload a module from within a Python toolbox (during development),
# use the importlib module's reload function.
imp.reload(add_area_tool)
# imp works on Python 2.7 and 3.x, however it has be deprecated as of
# Python 3.4 and replaced by importlib
# import importlib
# importlib.import_module(add_area_tool)

# pylint: disable=too-few-public-methods
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
        self.tools = [AddAreaMultiple, AddAreaSingle]


class AddAreaMultiple(add_area_tool.AddAreaMultiple):
    """See add_area_tool.py for class definition."""

    def __init__(self):
        add_area_tool.AddAreaMultiple.__init__(self)
        self.label = "Add Area (Multiple)"
        self.description = "Add an area attribute to multiple polygon feature Classes"
        self.category = "Add Attributes"


class AddAreaSingle(add_area_tool.AddAreaSingle):
    """See add_area_tool.py for class definition."""

    def __init__(self):
        add_area_tool.AddAreaSingle.__init__(self)
        self.label = "Add Area (Single)"
        self.description = "Add an area attribute to polygon features"
        self.category = "Add Attributes"
