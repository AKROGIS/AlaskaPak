using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.Display;
using ESRI.ArcGIS.Geometry;
using ESRI.ArcGIS.Geodatabase;
using ESRI.ArcGIS.Catalog;
using NPS.AKRO.ArcGIS.Forms;
using NPS.AKRO.ArcGIS.Common;
using System.Windows.Forms;
using System.Drawing;
using NPS.AKRO.ArcGIS.Grids;
using System.Diagnostics;
using ESRI.ArcGIS.ADF;

// OUTSTANDING ISSUES
// grid object is always defined in map's spatial reference.  - capture change SR events to update the grid.
// can't specify spatial reference for output.
// only feature class in a geodatabase dataset get a spatial reference
// TOC does not refresh to show symbology
// remove advanced panel, and remove extents panel.
// Capture move/resize from the grpahic group we create, so that we can update extents
// based on graphical input. 
// if existing polygon fC is selected, then no warning is issued, and grid is appended
//   (if schemas match), otherwise program crashes.
// Rotated Grids???

namespace NPS.AKRO.ArcGIS
{
    public class GenerateGrid : ESRI.ArcGIS.Desktop.AddIns.Tool
    {
        private AlaskaPak _controller;
        private GenerateGridForm _form;

        public GenerateGrid()
        {
            AlaskaPak.RunProtected(GetType(), MyConstructor);
        }

        private void MyConstructor()
        {
            _controller = AlaskaPak.Controller;
            //_controller.LayersChanged += Controller_LayersChanged;
            //_selectableLayers = _controller.GetSelectableLayers();
            Enabled = CheckForCoordinateSystem(); 
        }

        protected override void OnMouseDown(MouseEventArgs arg)
        {
            try
            {
                 if (Enabled)
                {
                    IEnvelope env = GetExtents();
                    //MessageBox.Show(string.Format("({0},{1}) to ({0},{1})", env.XMin, env.YMin, env.XMax, env.YMax), "Envelope");
                    if (_form != null) //User may click when form is already loaded.
                    {
                        UpdateForm(env);
                        _form.Activate();
                    }
                    else
                    {
                        //Grid grid = new Grid(env);
                        _form = new GenerateGridForm();
                        _form.saveButton.Click += Form_CreateGrid;
                        _form.FormClosed += Form_Closed;
                        _form.Grid = new Grid(env); //grid;
                        UpdateForm(env);
                        _form.Show();
                    }
                }
                else
                {
                    MessageBox.Show("The active data frame must be in a projected coordinate system.",
                        "For this command...", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(GetType() + " encountered a problem." +
                                Environment.NewLine + Environment.NewLine + ex.Message,
                                "Unhandled Exception", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        #region Event Handlers

        //What we will do when the form says it has closed
        internal void Form_CreateGrid(object sender, EventArgs e)
        {
            Grid grid = _form.Grid;
            IFeatureClass gridFC = CreateGridFC(grid, _form.Workspace, _form.Dataset, _form.FeatureClassName);
            if (gridFC == null)
                MessageBox.Show("Unable to create " + _form.FeatureClassName, "Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            else
            {
                AddFeatureClassToMap(gridFC);
                _form.Close();
            }
        }

        //What we will do when the form says it has closed
        internal void Form_Closed(object sender, FormClosedEventArgs e)
        {
            _form.Grid.Erase();
            _form = null;
        }
        #endregion

        private void UpdateForm(IEnvelope env)
        {
            //_form.UpdateExtents(env.XMin, env.YMin, env.XMax, env.YMax);
            _form.Grid.Map = ArcMap.Document.ActiveView.FocusMap;
            _form.Grid.Extents = env;
            _form.Grid.AdjustSize();
            _form.Grid.Draw();
            _form.UpdateFormFromGrid();
        }

        private IEnvelope GetExtents()
        {
            IScreenDisplay screenDisplay = ((IActiveView)ArcMap.Document.ActiveView.FocusMap).ScreenDisplay;
            IRubberBand rubberEnv = new RubberEnvelope();
            IEnvelope envelope = rubberEnv.TrackNew(screenDisplay, null) as IEnvelope;
            return envelope;
            //if (envelope.IsEmpty)
            //    return;
        }

        void MapEvents_ContentsChanged()
        {
            Enabled = CheckForCoordinateSystem();
        }

        private bool CheckForCoordinateSystem()
        {
            ISpatialReference sr = ArcMap.Document.FocusMap.SpatialReference;
            if (sr == null)
                return false;
            if (sr is IProjectedCoordinateSystem)
                    return true;
            return false;
        }

        private IFeatureClass CreateGridFC(Grid grid, IFeatureWorkspace workspace, IFeatureDataset dataset, string featureClassName)
        {
            try
            {
                IFields fields;
                IFeatureClass generatedFC;
                if (workspace is IGxFolder)
                {
                    MessageBox.Show("Creating Shapefile " + featureClassName + " in " + ((IWorkspace)workspace).PathName);
                    if (!ValidateShapefileName())
                    {
                        MessageBox.Show("Shapefile may exist, name may be too long," +
                            "folder may not exist, folder may be readonly,", "Error"); 
                        return null;
                    }
                    fields = CreateShapefileFields();
                } 
                else 
                {
                    if (dataset == null)
                    {
                        MessageBox.Show("Creating " + featureClassName + " in " + ((IWorkspace)workspace).PathName);
                    } 
                    else
                    {
                       MessageBox.Show("Creating " + featureClassName + " in " + ((IWorkspace)workspace).PathName + "\\" + dataset.Name);
                    }
                    if (!ValidateGdbfileName())
                        return null;
                    fields = CreateGdbFields();
                }
                generatedFC = CreateFeatureClass((IWorkspace2)workspace, dataset, featureClassName, fields, null, null, "");
                if (generatedFC == null)
                    return null;
                PutGridInFeatureClass(generatedFC, grid);
                return generatedFC;
            }
            catch (Exception ex)
            {
                Debug.Print("Exception Creating Feature Class: {0}",ex);
                return null;
            }
        }

        private void PutGridInFeatureClass(IFeatureClass featureClass, Grid grid)
        {
            using (ComReleaser comReleaser = new ComReleaser())
            {
                // Create a feature buffer.
                IFeatureBuffer featureBuffer = featureClass.CreateFeatureBuffer();
                comReleaser.ManageLifetime(featureBuffer);

                // Create an insert cursor.
                IFeatureCursor insertCursor = featureClass.Insert(true);
                comReleaser.ManageLifetime(insertCursor);

                // All of the features to be created are classified as Primary Highways.
                int colFieldIndex = featureClass.FindField("Col");
                int rowFieldIndex = featureClass.FindField("Row");
                int colLabelFieldIndex = featureClass.FindField("Col_Label");
                int rowLabelFieldIndex = featureClass.FindField("Row_Label");
                int cellLabelFieldIndex = featureClass.FindField("Cell_Label");
                int pageFieldIndex = featureClass.FindField("Page");

                foreach (Cell cell in grid.Cells)
                {
                    featureBuffer.Shape = cell.Shape;
                    featureBuffer.set_Value(colFieldIndex, cell.Column);
                    featureBuffer.set_Value(rowFieldIndex, cell.Row);
                    featureBuffer.set_Value(colLabelFieldIndex, cell.Column_Label);
                    featureBuffer.set_Value(rowLabelFieldIndex, cell.Row_Label);
                    featureBuffer.set_Value(cellLabelFieldIndex, cell.Label);
                    featureBuffer.set_Value(pageFieldIndex, cell.Page);
                    insertCursor.InsertFeature(featureBuffer);
                }

                // Flush the buffer to the geodatabase.
                insertCursor.Flush();
            }

        }

        private IFields CreateGdbFields()
        {
            IObjectClassDescription objectClassDescription = new FeatureClassDescriptionClass();
            // create the required fields
            IFields fields = objectClassDescription.RequiredFields;
            IFieldsEdit fieldsEdit = (IFieldsEdit)fields;
            IFieldEdit fieldEdit;

            fieldEdit = new FieldClass() as IFieldEdit;
            fieldEdit.Name_2 = "Col";
            fieldEdit.Type_2 = esriFieldType.esriFieldTypeInteger;
            fieldEdit.AliasName_2 = "Column";
            fieldsEdit.AddField(fieldEdit);

            fieldEdit = new FieldClass() as IFieldEdit;
            fieldEdit.Name_2 = "Row";
            fieldEdit.Type_2 = esriFieldType.esriFieldTypeInteger;
            fieldsEdit.AddField(fieldEdit);

            fieldEdit = new FieldClass() as IFieldEdit;
            fieldEdit.Name_2 = "Col_Label";
            fieldEdit.Type_2 = esriFieldType.esriFieldTypeString;
            fieldEdit.AliasName_2 = "Column Label";
            fieldEdit.Length_2 = 20;
            fieldsEdit.AddField(fieldEdit);

            fieldEdit = new FieldClass() as IFieldEdit;
            fieldEdit.Name_2 = "Row_Label";
            fieldEdit.Type_2 = esriFieldType.esriFieldTypeString;
            fieldEdit.AliasName_2 = "Row Label";
            fieldEdit.Length_2 = 20;
            fieldsEdit.AddField(fieldEdit);

            fieldEdit = new FieldClass() as IFieldEdit;
            fieldEdit.Name_2 = "Cell_Label";
            fieldEdit.Type_2 = esriFieldType.esriFieldTypeString;
            fieldEdit.AliasName_2 = "Cell Label";
            fieldEdit.Length_2 = 20;
            fieldsEdit.AddField(fieldEdit);

            fieldEdit = new FieldClass() as IFieldEdit;
            fieldEdit.Name_2 = "Page";
            fieldEdit.Type_2 = esriFieldType.esriFieldTypeInteger;
            fieldEdit.AliasName_2 = "Page Number";
            fieldsEdit.AddField(fieldEdit);

            return fields;
        }

        private bool ValidateGdbfileName()
        {
            //FIXME - do something real
            return true;
        }

        private IFields CreateShapefileFields()
        {
            //FIXME - validate and consolidate
            return CreateGdbFields();
        }

        private bool ValidateShapefileName()
        {
            //FIXME - do something real
            return true;
        }

        private void AddFeatureClassToMap(IFeatureClass gridFC)
        {
            ESRI.ArcGIS.Carto.IFeatureLayer featureLayer = new ESRI.ArcGIS.Carto.FeatureLayerClass();
            featureLayer.FeatureClass = gridFC;
            featureLayer.Name = gridFC.AliasName;
            featureLayer.Visible = true;
            ArcMap.Document.ActiveView.FocusMap.AddLayer(featureLayer);
            FixSymbology(featureLayer);
            ArcMap.Document.UpdateContents();
            //ArcMap.Document.ActiveView.Extent = ((IGeoDataset)featureLayer).Extent;
            ArcMap.Document.ActiveView.PartialRefresh(esriViewDrawPhase.esriViewGeography, null, null);
        }

        private void FixSymbology(IFeatureLayer featureLayer)
        {
            //Color
            IGeoFeatureLayer geoLayer = featureLayer as IGeoFeatureLayer;
            if (geoLayer == null)
                return;
            ISimpleRenderer renderer = geoLayer.Renderer as ISimpleRenderer;
            if (renderer == null)
                return;
            IFillSymbol symbol = renderer.Symbol as IFillSymbol;
            if (symbol == null)
                return;

            //The objects at symbol.Color and symbol.Outline are immutable while the properties are not.
            //The objects don't complain if you try and change them, it just has no effect.
            //symbol.Color.NullColor = true;  // appears to work but has no effect.
            IRgbColor nullColor = new RgbColorClass();
            nullColor.NullColor = true;
            symbol.Color = nullColor;

            ILineSymbol outline = new SimpleLineSymbol();
            outline.Width = 1.0;
            IRgbColor color = new RgbColorClass();
            color.Red = 255;
            color.UseWindowsDithering = true;
            outline.Color = color;
            symbol.Outline = outline;

            //Labeling
            IAnnotateLayerProperties annotationProperties;
            IElementCollection unused;
            geoLayer.AnnotationProperties.QueryItem(0, out annotationProperties, out unused, out unused);
            ((ILabelEngineLayerProperties)annotationProperties).Expression = "[Cell_Label]";
            geoLayer.DisplayAnnotation = true;

        }


        ///<summary>Simple helper to create a featureclass in a geodatabase.</summary>
        /// 
        ///<param name="workspace">An IWorkspace2 interface</param>
        ///<param name="featureDataset">An IFeatureDataset interface or Nothing</param>
        ///<param name="featureClassName">A System.String that contains the name of the feature class to open or create. Example: "states"</param>
        ///<param name="fields">An IFields interface</param>
        ///<param name="CLSID">A UID value or Nothing. Example "esriGeoDatabase.Feature" or Nothing</param>
        ///<param name="CLSEXT">A UID value or Nothing (this is the class extension if you want to reference a class extension when creating the feature class).</param>
        ///<param name="strConfigKeyword">An empty System.String or RDBMS table string for ArcSDE. Example: "myTable" or ""</param>
        ///  
        ///<returns>An IFeatureClass interface or a Nothing</returns>
        ///  
        ///<remarks>
        ///  (1) If a 'featureClassName' already exists in the workspace a reference to that feature class 
        ///      object will be returned.
        ///  (2) If an IFeatureDataset is passed in for the 'featureDataset' argument the feature class
        ///      will be created in the dataset. If a Nothing is passed in for the 'featureDataset'
        ///      argument the feature class will be created in the workspace.
        ///  (3) When creating a feature class in a dataset the spatial reference is inherited 
        ///      from the dataset object.
        ///  (4) If an IFields interface is supplied for the 'fields' collection it will be used to create the
        ///      table. If a Nothing value is supplied for the 'fields' collection, a table will be created using 
        ///      default values in the method.
        ///  (5) The 'strConfigurationKeyword' parameter allows the application to control the physical layout 
        ///      for this table in the underlying RDBMSfor example, in the case of an Oracle database, the 
        ///      configuration keyword controls the tablespace in which the table is created, the initial and 
        ///     next extents, and other properties. The 'strConfigurationKeywords' for an ArcSDE instance are 
        ///      set up by the ArcSDE data administrator, the list of available keywords supported by a workspace 
        ///      may be obtained using the IWorkspaceConfiguration interface. For more information on configuration 
        ///      keywords, refer to the ArcSDE documentation. When not using an ArcSDE table use an empty 
        ///      string (ex: "").
        ///</remarks>
        public ESRI.ArcGIS.Geodatabase.IFeatureClass CreateFeatureClass(ESRI.ArcGIS.Geodatabase.IWorkspace2 workspace, ESRI.ArcGIS.Geodatabase.IFeatureDataset featureDataset, System.String featureClassName, ESRI.ArcGIS.Geodatabase.IFields fields, ESRI.ArcGIS.esriSystem.UID CLSID, ESRI.ArcGIS.esriSystem.UID CLSEXT, System.String strConfigKeyword)
        {
            if (featureClassName == "") return null; // name was not passed in 

            ESRI.ArcGIS.Geodatabase.IFeatureClass featureClass;
            ESRI.ArcGIS.Geodatabase.IFeatureWorkspace featureWorkspace = (ESRI.ArcGIS.Geodatabase.IFeatureWorkspace)workspace; // Explicit Cast

            if (workspace.get_NameExists(ESRI.ArcGIS.Geodatabase.esriDatasetType.esriDTFeatureClass, featureClassName)) //feature class with that name already exists 
            {
                featureClass = featureWorkspace.OpenFeatureClass(featureClassName);
                return featureClass;
            }

            // assign the class id value if not assigned
            if (CLSID == null)
            {
                CLSID = new ESRI.ArcGIS.esriSystem.UIDClass();
                CLSID.Value = "esriGeoDatabase.Feature";  //Works for shapefiles as well
            }

            ESRI.ArcGIS.Geodatabase.IObjectClassDescription objectClassDescription = new ESRI.ArcGIS.Geodatabase.FeatureClassDescriptionClass();

            // if a fields collection is not passed in then supply our own
            if (fields == null)
            {
                // create the fields using the required fields method
                fields = objectClassDescription.RequiredFields;
                ESRI.ArcGIS.Geodatabase.IFieldsEdit fieldsEdit = (ESRI.ArcGIS.Geodatabase.IFieldsEdit)fields; // Explicit Cast
                ESRI.ArcGIS.Geodatabase.IField field = new ESRI.ArcGIS.Geodatabase.FieldClass();

                // create a user defined text field
                ESRI.ArcGIS.Geodatabase.IFieldEdit fieldEdit = (ESRI.ArcGIS.Geodatabase.IFieldEdit)field; // Explicit Cast

                // setup field properties
                fieldEdit.Name_2 = "SampleField";
                fieldEdit.Type_2 = ESRI.ArcGIS.Geodatabase.esriFieldType.esriFieldTypeString;
                fieldEdit.IsNullable_2 = true;
                fieldEdit.AliasName_2 = "Sample Field Column";
                fieldEdit.DefaultValue_2 = "test";
                fieldEdit.Editable_2 = true;
                fieldEdit.Length_2 = 100;

                // add field to field collection
                fieldsEdit.AddField(field);
                fields = (ESRI.ArcGIS.Geodatabase.IFields)fieldsEdit; // Explicit Cast
            }

            System.String strShapeField = "";

            // locate the shape field
            for (int j = 0; j < fields.FieldCount; j++)
            {
                if (fields.get_Field(j).Type == ESRI.ArcGIS.Geodatabase.esriFieldType.esriFieldTypeGeometry)
                {
                    strShapeField = fields.get_Field(j).Name;
                    break;
                }
            }

            // Use IFieldChecker to create a validated fields collection.
            ESRI.ArcGIS.Geodatabase.IFieldChecker fieldChecker = new ESRI.ArcGIS.Geodatabase.FieldCheckerClass();
            ESRI.ArcGIS.Geodatabase.IEnumFieldError enumFieldError = null;
            ESRI.ArcGIS.Geodatabase.IFields validatedFields = null;
            fieldChecker.ValidateWorkspace = (ESRI.ArcGIS.Geodatabase.IWorkspace)workspace;
            fieldChecker.Validate(fields, out enumFieldError, out validatedFields);

            // The enumFieldError enumerator can be inspected at this point to determine 
            // which fields were modified during validation.


            // finally create and return the feature class
            if (featureDataset == null)// if no feature dataset passed in, create at the workspace level
            {
                featureClass = featureWorkspace.CreateFeatureClass(featureClassName, validatedFields, CLSID, CLSEXT, ESRI.ArcGIS.Geodatabase.esriFeatureType.esriFTSimple, strShapeField, strConfigKeyword);
            }
            else
            {
                featureClass = featureDataset.CreateFeatureClass(featureClassName, validatedFields, CLSID, CLSEXT, ESRI.ArcGIS.Geodatabase.esriFeatureType.esriFTSimple, strShapeField, strConfigKeyword);
            }
            return featureClass;
        }
    }
}
