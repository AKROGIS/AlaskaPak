using System;
using System.Collections.Generic;
using System.Linq;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.Geodatabase;
using NPS.AKRO.ArcGIS.Common;

namespace NPS.AKRO.ArcGIS.AddCoordinates
{
    internal class FormData
    {
        internal FormData(List<NamedLayer> pointLayers)
        {
            Format = new Formatter();
            PointLayers = pointLayers;
            if (PointLayers.Count == 0)
                LayerIndex = -1;
        }

        // LayerIndex and FeatureClass are mutually exclusive,
        // although both can be empty (-1 and null/empty respectively)
        internal int LayerIndex
        {
            get { return _layerIndex; }
            set
            {
                if (value == _layerIndex)
                    return;
                if (value < -1 || value > PointLayers.Count)
                    throw new ArgumentOutOfRangeException("value");
                _layerIndex = value;
                if (_layerIndex != -1)
                    _featureClassPath = string.Empty;
            }
        }

        private int _layerIndex;

        internal string FeatureClassPath
        {
            get { return _featureClassPath; }
            set
            {
                if (value == _featureClassPath)
                    return;
                _featureClassPath = value;
                if (!string.IsNullOrEmpty(_featureClassPath))
                    _layerIndex = -1;
            }
        }

        private string _featureClassPath;

        internal string XFieldName { get; set; }
        internal string YFieldName { get; set; }
        internal Formatter Format { get; private set; }

        internal List<NamedLayer> PointLayers
        {
            get { return _pointLayers; }
            set
            {
                if (_pointLayers == value)
                    return;
                if (value == null || value.Count == 0)
                {
                    _pointLayers = value;
                    LayerIndex = -1;
                    return;
                }
                if (_pointLayers != null && LayerIndex != -1)
                {
                    //try to find the old name in the new list
                    if (value.Select(n => n.Name).Contains(_pointLayers[LayerIndex].Name))
                        LayerIndex = value.IndexOf(value.First(n => n.Name == _pointLayers[LayerIndex].Name));
                }
                _pointLayers = value;
                // Make sure the index is not out of bounds
                if (LayerIndex != -1 && _pointLayers.Count <= LayerIndex)
                    LayerIndex = _pointLayers.Count - 1;
                //if no featureclass is set, give layerIndex a deault value
                if (string.IsNullOrEmpty(FeatureClassPath) && LayerIndex == -1 && PointLayers.Count > 0)
                    LayerIndex = 0;
            }
        }

        private List<NamedLayer> _pointLayers;

        internal List<string> PointLayerNames
        {
            get { return PointLayers.Select(nl => nl.Name).ToList(); }
        }

        internal bool IsReady
        {
            get
            {
                return
                    !string.IsNullOrEmpty(XFieldName) &&
                    !string.IsNullOrEmpty(YFieldName) &&
                    (!string.IsNullOrEmpty(FeatureClassPath) && IsFeatureClassValid || LayerIndex != -1);
            }
        }

        internal bool IsFeatureClassValid
        {
            get
            {
                //FIXME - do something intelligent
                return true;
            }
        }

        internal string DefaultXFieldName
        {
            get
            {
                if (Format == null)
                    return string.Empty;
                switch (Format.OutputFormat)
                {
                    default:
                        return "X_Coord";
                    case FormatterOutputFormat.DecimalDegress:
                        return "Lon_DD";
                    case FormatterOutputFormat.DegreesDecimalMinutes:
                        return "Lon_DDM";
                    case FormatterOutputFormat.DegreesMinutesSeconds:
                        return "Lon_DMS";
                }
            }
        }

        internal string DefaultYFieldName
        {
            get
            {
                if (Format == null)
                    return string.Empty;
                switch (Format.OutputFormat)
                {
                    default:
                        return "Y_Coord";
                    case FormatterOutputFormat.DecimalDegress:
                        return "Lat_DD";
                    case FormatterOutputFormat.DegreesDecimalMinutes:
                        return "Lat_DDM";
                    case FormatterOutputFormat.DegreesMinutesSeconds:
                        return "Lat_DMS";
                }
            }
        }

        internal IEnumerable<string> GetAllFieldNames()
        {
            return GetFields("*");
        }

        internal IEnumerable<string> GetAppropriateFieldNames()
        {
            return GetFields(Format.Formattable ? "string" : "double");
        }

        internal IFeatureClass GetFeatureClass()
        {
            if (LayerIndex != -1)
                return ((IFeatureLayer)PointLayers[LayerIndex].Layer).FeatureClass;
            if (!string.IsNullOrEmpty(FeatureClassPath))
                //FIXME
                throw new NotImplementedException();
            return null;
        }

        private IEnumerable<string> GetFields(string type)
        {
            IFeatureClass featureClass = GetFeatureClass();
            if (featureClass == null)
                yield break;
            int fieldCount = featureClass.Fields.FieldCount;
            for (int counter = 0; counter < fieldCount; counter++)
            {
                if (type == "*")
                    yield return featureClass.Fields.Field[counter].Name;
                if (type == "double" && featureClass.Fields.Field[counter].Type == esriFieldType.esriFieldTypeDouble)
                    yield return featureClass.Fields.Field[counter].Name;
                if (type == "string" && featureClass.Fields.Field[counter].Type == esriFieldType.esriFieldTypeString)
                    yield return featureClass.Fields.Field[counter].Name;
            }
        }

        internal bool FieldNameExists(string name)
        {
            IFeatureClass featureClass = GetFeatureClass();
            if (featureClass == null)
                throw new Exception("Feature class is null");
            IFields fields = ((IFeatureLayer)PointLayers[LayerIndex].Layer).FeatureClass.Fields;
            return fields.FindField(name) != -1;
        }

        internal int FieldNameIndex(string name)
        {
            IFeatureClass featureClass = GetFeatureClass();
            if (featureClass == null)
                throw new Exception("Feature class is null");
            IFields fields = ((IFeatureLayer)PointLayers[LayerIndex].Layer).FeatureClass.Fields;
            return fields.FindField(name);
        }

        internal esriFieldNameErrorType ValidateFieldName(string name)
        {
            IFeatureClass featureClass = GetFeatureClass();
            if (featureClass == null)
                return esriFieldNameErrorType.esriNoFieldError;

            IFields fields = featureClass.Fields;
            IWorkspace workspace = ((IDataset)featureClass).Workspace;
            IField newField = new FieldClass();
            ((IFieldEdit)newField).Name_2 = name;
            ((IFieldsEdit)fields).AddField(newField);

            IFieldChecker fieldChecker = new FieldCheckerClass();
            fieldChecker.ValidateWorkspace = workspace;

            // Validate the fields.
            IEnumFieldError enumFieldError;
            IFields validatedFields;
            fieldChecker.Validate(fields, out enumFieldError, out validatedFields);
            ((IFieldsEdit)fields).DeleteField(newField);
            if (enumFieldError == null)
                return esriFieldNameErrorType.esriNoFieldError;
            // Display the field errors.
            enumFieldError.Reset();
            IFieldError fieldError = enumFieldError.Next();
            while (fieldError != null)
            {
                if (fieldError.FieldIndex == fields.FieldCount)
                    return fieldError.FieldError;
            }
            return esriFieldNameErrorType.esriNoFieldError;
        }
    }
}
