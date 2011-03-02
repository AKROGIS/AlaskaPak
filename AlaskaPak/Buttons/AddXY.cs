using System;
using System.Windows.Forms;
using ESRI.ArcGIS.Geodatabase;
using ESRI.ArcGIS.Geometry;
using NPS.AKRO.ArcGIS.Coordinates;
using NPS.AKRO.ArcGIS.Forms;

/*
 * Enhancements/Bug Fixes
 *  - Can we get the users display units/settings and use that as a default?
 *  - Enable selection of Feature Class from form
 *  - Allow selection of a SR in form
 *  - If table is open do a refresh
 *  - If selected workspace is in an edit session, then start/stop a change
 *  - Add option for zero padding
 *  - Change picklist name to "Dataset coords formated as DMS ..."
 * General refactoring
 *   - move general utility functions to common library
 *   - remove ESRI requirements from FormData
 */

namespace NPS.AKRO.ArcGIS
{
    public class AddXY : ESRI.ArcGIS.Desktop.AddIns.Button
    {

        private AlaskaPak _controller;
        private AddXYForm _form;
        private FormData _data;
        
        public AddXY()
        {
            _controller = AlaskaPak.Controller;
            _controller.LayersChanged += Controller_LayersChanged;
            _data = new FormData(_controller.GetPointLayers());
            Enabled = MapHasPointFeatureLayer;
        }

        protected override void OnClick()
        {
            if (Enabled)
            {
                if (_form != null) //User may click when form is already loaded.
                {
                    _form.Activate();
                }
                else
                {
                    _form = new AddXYForm(_data);
                    //What we will do when the form says it is closing
                    _form.FormClosed += delegate { _form = null; };
                    //What we will do when the form says it is ready to process
                    _form.okButton.Click += delegate { EditLayer(_form.Data); _form.Close(); };
                    _form.Show();
                }
            }
            else
            {
                MessageBox.Show("You must have one or more point feature layers in your map to use this command.",
                    "For this command...", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private bool MapHasPointFeatureLayer
        {
            get { return _data.PointLayers.Count > 0; }
        }

        #region Event Handlers

        //What we will do when the controller says the layers have changed
        void Controller_LayersChanged()
        {
            _data.PointLayers = _controller.GetPointLayers();
            Enabled = MapHasPointFeatureLayer;
            if (_form != null)
                _form.PointLayersChanged();
        }

        #endregion

        #region Helper Functions (Tool Specific Logic)

        private void EditLayer(FormData data)
        {
            IFeatureClass featureClass = data.GetFeatureClass();
            if (featureClass == null)
            {
                MessageBox.Show("No feature layer/class was selected.\n");
                return;
            }

            if (featureClass.ShapeType != esriGeometryType.esriGeometryPoint)
            {
                MessageBox.Show("Data is not a point feature.\n");
                return;
            }


            //If fields don't exist, add them
            foreach (string fieldName in new string[] { data.XFieldName, data.YFieldName })
            {
                if (!data.FieldNameExists(fieldName))
                {
                    esriFieldType fieldType;
                    if (data.Format.Formattable)
                        fieldType = esriFieldType.esriFieldTypeString;
                    else
                        fieldType = esriFieldType.esriFieldTypeDouble;
                    try
                    {
                        AddField(featureClass, fieldName, fieldType);
                    }
                    catch (Exception e)
                    {
                        MessageBox.Show("Unable to add new fields.\n" +
                            "Check that the selected data is not open in Catalog.\n" +
                            "Check that the selected layer is not being edited.\n" + 
                            "System Message: " + e.Message);
                        return;
                    }
                }
            }
            //try to get an update cursor on the feature class
            IFeatureCursor cursor;
            try
            {
                cursor = featureClass.Update(null, true);
            }
            catch (Exception e)
            {
                Console.WriteLine("Unable edit the layer.\n" + e.Message);
                return;
            }
            int xIndex = cursor.FindField(data.XFieldName);
            int yIndex = cursor.FindField(data.YFieldName);
            ISpatialReference spatialReference = null;
            if (data.Format.OutputFormat == FormatterOutputFormat.DataFrame)
                spatialReference = ArcMap.Document.FocusMap.SpatialReference;
            if (data.Format.Formattable)
                // We already guaranteed it is a point feature, so it must implement IGeoDataset
                spatialReference = GetGcsFromPcs(((IGeoDataset)featureClass).SpatialReference);
            IFeature feature = cursor.NextFeature();
            while (feature != null)
            {
                IPoint point = (IPoint)feature.Shape;
                if (spatialReference != null)
                    point.Project(spatialReference);

                if (data.Format.Formattable)
                {
                    feature.Value[xIndex] = data.Format.Format(point.X, false);
                    feature.Value[yIndex] = data.Format.Format(point.Y, true);
                }
                else
                {
                    feature.Value[xIndex] = point.X;
                    feature.Value[yIndex] = point.Y;
                }
                cursor.UpdateFeature(feature);
                feature = cursor.NextFeature();
            }
            System.Runtime.InteropServices.Marshal.ReleaseComObject(cursor);
        }

        private ISpatialReference GetGcsFromPcs(ISpatialReference spatialRef)
        {
            if (spatialRef == null || spatialRef is IUnknownCoordinateSystem)
                return null;
            if (spatialRef is IGeographicCoordinateSystem)
                return spatialRef;
            return ((IProjectedCoordinateSystem)spatialRef).GeographicCoordinateSystem;
        }

        private void AddField(IFeatureClass featureClass, string fieldName, esriFieldType fieldType)
        {
            IField newField = new FieldClass();
            ((IFieldEdit)newField).Name_2 = fieldName;
            ((IFieldEdit)newField).Type_2 = fieldType;
                    
            ISchemaLock schemaLock = (ISchemaLock)featureClass;
            try
            {
                // Get an exclusive schema lock to change the schema. 
                schemaLock.ChangeSchemaLock(esriSchemaLock.esriExclusiveSchemaLock);
                featureClass.AddField(newField);
            }
            finally
            {
                //release the exclusive schema lock
                schemaLock.ChangeSchemaLock(esriSchemaLock.esriSharedSchemaLock);
            }
        }

        #endregion
    }
}
