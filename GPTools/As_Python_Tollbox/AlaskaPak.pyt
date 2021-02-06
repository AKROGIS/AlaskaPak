import arcpy
import add_area_tool
import imp
imp.reload(add_area_tool)
#import importlib
#importlib.import_module(add_area)

class Toolbox(object):
    """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
    def __init__(self):
        self.label = "AlaskaPak Toolbox"
        self.alias = "AlaskaPak"
        self.description = "A collection of GIS tools for the Alaska Region"
        #In of ArcGIS 10.2, the tool classes must be in this file
        self.tools = [AddAreaMultiple, AddAreaSingle]


class AddAreaMultiple(add_area_tool.AddAreaMultiple):
    def __init__(self):
        add_area_tool.AddAreaMultiple.__init__(self)
        self.label = "Add Area (Multiple)"
        self.description = ("Add an area attribute to multiple polygon"
                            "feature Classes")
        self.category = "Add Attributes"


class AddAreaSingle(add_area_tool.AddAreaSingle):
    def __init__(self):
        add_area_tool.AddAreaSingle.__init__(self)
        self.label = "Add Area (Single)"
        self.description = "Add an area attribute to polygon features"
        self.category = "Add Attributes"
