import arcpy

import add_area

class AddAreaMultiple(object):
    def __init__(self):
        self.canRunInBackground = True

    def getParameterInfo(self):
        features = arcpy.Parameter(
            name="features",
            displayName="Input Features",
            direction="Input",
            datatype="GPFeatureLayer",
            parameterType="Required",
            multiValue=True)
        features.filter.list = ["Polygon"]

        field_name = arcpy.Parameter(
            name="field_name",
            displayName="Field name",
            direction="Input",
            datatype="Field",
            parameterType="Optional")
        field_name.value = "Area"

        units = arcpy.Parameter(
            name="units",
            displayName="Areal Units",
            direction="Input",
            datatype="GPString",
            parameterType="Optional")
        units.filter.list = add_area.valid_units

        overwrite = arcpy.Parameter(
            name="overwrite",
            displayName="Overwrite Existing Values",
            direction="Input",
            datatype="GPBoolean",
            parameterType="Optional")

        parameters = [features, field_name, units, overwrite]
        return parameters

    def updateParameters(self, parameters):
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        features = parameters[0].value
        units = parameters[1].valueAsText
        fieldname = parameters[2].valueAsText
        overwrite = parameters[3].value
        add_area.add_area_to_features(features, units,
                                      fieldname, overwrite)


class AddAreaSingle(object):
    def __init__(self):
        self.canRunInBackground = True

    def getParameterInfo(self):
        feature = arcpy.Parameter(
            name="feature",
            displayName="Input Feature",
            direction="Input",
            datatype="GPFeatureLayer",
            parameterType="Required")
        feature.filter.list = ["Polygon"]

        field_name = arcpy.Parameter(
            name="field_name",
            displayName="Field name",
            direction="Input",
            datatype="Field",
            parameterType="Optional")
        field_name.value = "Area"
        field_name.parameterDependencies = [feature.name]
        field_name.filter.list = ["Double"]

        units = arcpy.Parameter(
            name="units",
            displayName="Areal Units",
            direction="Input",
            datatype="GPString",
            parameterType="Optional")
        units.filter.list = add_area.valid_units

        overwrite = arcpy.Parameter(
            name="overwrite",
            displayName="Overwrite Existing Values",
            direction="Input",
            datatype="GPBoolean",
            parameterType="Optional")

        out_feature = arcpy.Parameter(
            name="out_feature",
            displayName="Output Feature",
            direction="Output",
            datatype="GPFeatureLayer",
            parameterType="Derived")
        out_feature.parameterDependencies = [feature.name]
        out_feature.schema.clone = True

        parameters = [feature, field_name, units, overwrite, out_feature]
        return parameters

    def updateParameters(self, parameters):
        if parameters[0].altered:
            parameters[1].value = arcpy.ValidateFieldName(parameters[1].value,
                                                          parameters[0].value)
        return

    def updateMessages(self, parameters):
        return

    def execute(self, parameters, messages):
        feature = parameters[0].valueAsText
        units = parameters[1].valueAsText
        field_name = parameters[2].valueAsText
        overwrite = parameters[3].value
        add_area.add_area_to_feature(feature, units,
                                     field_name, overwrite)