using System;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.Display;
using ESRI.ArcGIS.Geometry;
using ESRI.ArcGIS.Geodatabase;
using ESRI.ArcGIS.Catalog;
using NPS.AKRO.ArcGIS.Forms;
using System.Windows.Forms;
using NPS.AKRO.ArcGIS.Grids;
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
        //private AlaskaPak _controller;
        private GenerateGridForm _form;

        public GenerateGrid()
        {
            AlaskaPak.RunProtected(GetType(), MyConstructor);
        }

        private void MyConstructor()
        {
            //_controller = AlaskaPak.Controller;
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
                    MessageBox.Show(@"The active data frame must be in a projected coordinate system.",
                                    @"For this command...", MessageBoxButtons.OK, MessageBoxIcon.Information);
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show(GetType() + @" encountered a problem." +
                                Environment.NewLine + Environment.NewLine + ex.Message,
                                @"Unhandled Exception", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        #region Event Handlers

        //What we will do when the form says it has closed
        internal void Form_CreateGrid(object sender, EventArgs e)
        {
            Grid grid = _form.Grid;
            IFeatureClass gridFeatureClass = CreateGridFeatureClass(grid, _form.Workspace, _form.Dataset,
                                                                    _form.FeatureClassName);
            if (gridFeatureClass == null)
                MessageBox.Show(@"Unable to create " + _form.FeatureClassName, @"Error", MessageBoxButtons.OK,
                                MessageBoxIcon.Error);
            else
            {
                AddFeatureClassToMap(gridFeatureClass);
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

        private static IEnvelope GetExtents()
        {
            IScreenDisplay screenDisplay = ((IActiveView)ArcMap.Document.ActiveView.FocusMap).ScreenDisplay;
            IRubberBand rubberEnv = new RubberEnvelope();
            var envelope = rubberEnv.TrackNew(screenDisplay, null) as IEnvelope;
            return envelope;
            //if (envelope.IsEmpty)
            //    return;
        }

        //void MapEvents_ContentsChanged()
        //{
        //    Enabled = CheckForCoordinateSystem();
        //}

        private static bool CheckForCoordinateSystem()
        {
            ISpatialReference sr = ArcMap.Document.FocusMap.SpatialReference;
            if (sr == null)
                return false;
            return sr is IProjectedCoordinateSystem;
        }

        private IFeatureClass CreateGridFeatureClass(Grid grid, IFeatureWorkspace workspace, IFeatureDataset dataset,
                                                     string featureClassName)
        {
            try
            {
                IFields fields;
                if (workspace is IGxFolder)
                {
                    MessageBox.Show(@"Creating Shapefile " + featureClassName + @" in " +
                                    ((IWorkspace)workspace).PathName);
                    if (!ValidateShapefileName())
                    {
                        MessageBox.Show(@"Shapefile may exist, name may be too long," +
                                        @"folder may not exist, folder may be readonly,", @"Error");
                        return null;
                    }
                    fields = CreateShapefileFields();
                }
                else
                {
                    string msg = dataset == null
                                     ? string.Format("Creating {0} in {1}", featureClassName,
                                                     ((IWorkspace)workspace).PathName)
                                     : string.Format("Creating {0} in {1}\\{2}", featureClassName,
                                                     ((IWorkspace)workspace).PathName, dataset.Name);
                    MessageBox.Show(msg);
                    if (!ValidateGdbfileName())
                        return null;
                    fields = CreateGdbFields();
                }
                IFeatureClass generatedFeatureClass = CreateFeatureClass((IWorkspace2)workspace, dataset,
                                                                         featureClassName, fields, null, null, "");
                if (generatedFeatureClass == null)
                    return null;
                PutGridInFeatureClass(generatedFeatureClass, grid);
                return generatedFeatureClass;
            }
            catch (Exception)
            {
                //Debug.Print("Exception Creating Feature Class: {0}",ex);
                return null;
            }
        }

        private static void PutGridInFeatureClass(IFeatureClass featureClass, Grid grid)
        {
            using (var comReleaser = new ComReleaser())
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
                    featureBuffer.Value[colFieldIndex] = cell.Column;
                    featureBuffer.Value[rowFieldIndex] = cell.Row;
                    featureBuffer.Value[colLabelFieldIndex] = cell.ColumnLabel;
                    featureBuffer.Value[rowLabelFieldIndex] = cell.RowLabel;
                    featureBuffer.Value[cellLabelFieldIndex] = cell.Label;
                    featureBuffer.Value[pageFieldIndex] = cell.Page;
                    insertCursor.InsertFeature(featureBuffer);
                }

                // Flush the buffer to the geodatabase.
                insertCursor.Flush();
            }
        }

        private static IFields CreateGdbFields()
        {
            IObjectClassDescription objectClassDescription = new FeatureClassDescriptionClass();
            // create the required fields
            IFields fields = objectClassDescription.RequiredFields;
            var fieldsEdit = (IFieldsEdit)fields;

            IFieldEdit fieldEdit = new FieldClass();
            fieldEdit.Name_2 = "Col";
            fieldEdit.Type_2 = esriFieldType.esriFieldTypeInteger;
            fieldEdit.AliasName_2 = "Column";
            fieldsEdit.AddField(fieldEdit);

            fieldEdit = new FieldClass();
            fieldEdit.Name_2 = "Row";
            fieldEdit.Type_2 = esriFieldType.esriFieldTypeInteger;
            fieldsEdit.AddField(fieldEdit);

            fieldEdit = new FieldClass();
            fieldEdit.Name_2 = "Col_Label";
            fieldEdit.Type_2 = esriFieldType.esriFieldTypeString;
            fieldEdit.AliasName_2 = "Column Label";
            fieldEdit.Length_2 = 20;
            fieldsEdit.AddField(fieldEdit);

            fieldEdit = new FieldClass();
            fieldEdit.Name_2 = "Row_Label";
            fieldEdit.Type_2 = esriFieldType.esriFieldTypeString;
            fieldEdit.AliasName_2 = "Row Label";
            fieldEdit.Length_2 = 20;
            fieldsEdit.AddField(fieldEdit);

            fieldEdit = new FieldClass();
            fieldEdit.Name_2 = "Cell_Label";
            fieldEdit.Type_2 = esriFieldType.esriFieldTypeString;
            fieldEdit.AliasName_2 = "Cell Label";
            fieldEdit.Length_2 = 20;
            fieldsEdit.AddField(fieldEdit);

            fieldEdit = new FieldClass();
            fieldEdit.Name_2 = "Page";
            fieldEdit.Type_2 = esriFieldType.esriFieldTypeInteger;
            fieldEdit.AliasName_2 = "Page Number";
            fieldsEdit.AddField(fieldEdit);

            return fields;
        }

        private static bool ValidateGdbfileName()
        {
            //FIXME - do something real
            return true;
        }

        private static IFields CreateShapefileFields()
        {
            //FIXME - validate and consolidate
            return CreateGdbFields();
        }

        private static bool ValidateShapefileName()
        {
            //FIXME - do something real
            return true;
        }

        private static void AddFeatureClassToMap(IFeatureClass gridFeatureClass)
        {
            IFeatureLayer featureLayer = new FeatureLayerClass();
            featureLayer.FeatureClass = gridFeatureClass;
            featureLayer.Name = gridFeatureClass.AliasName;
            featureLayer.Visible = true;
            ArcMap.Document.ActiveView.FocusMap.AddLayer(featureLayer);
            FixSymbology(featureLayer);
            ArcMap.Document.UpdateContents();
            //ArcMap.Document.ActiveView.Extent = ((IGeoDataset)featureLayer).Extent;
            ArcMap.Document.ActiveView.PartialRefresh(esriViewDrawPhase.esriViewGeography, null, null);
        }

        private static void FixSymbology(IFeatureLayer featureLayer)
        {
            //Color
            var geoLayer = featureLayer as IGeoFeatureLayer;
            if (geoLayer == null)
                return;
            var renderer = geoLayer.Renderer as ISimpleRenderer;
            if (renderer == null)
                return;
            var symbol = renderer.Symbol as IFillSymbol;
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
        ///<param name="clsid">A UID value or Nothing. Example "esriGeoDatabase.Feature" or Nothing</param>
        ///<param name="clsext">A UID value or Nothing (this is the class extension if you want to reference a class extension when creating the feature class).</param>
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
        internal IFeatureClass CreateFeatureClass(IWorkspace2 workspace, IFeatureDataset featureDataset,
                                                  string featureClassName,
                                                  IFields fields, ESRI.ArcGIS.esriSystem.UID clsid,
                                                  ESRI.ArcGIS.esriSystem.UID clsext, string strConfigKeyword)
        {
            if (string.IsNullOrEmpty(featureClassName))
                return null;

            IFeatureClass featureClass;
            var featureWorkspace = (IFeatureWorkspace)workspace; // Cast may throw exception

            if (workspace.NameExists[esriDatasetType.esriDTFeatureClass, featureClassName])
                //feature class with that name already exists 
            {
                featureClass = featureWorkspace.OpenFeatureClass(featureClassName);
                return featureClass;
            }

            // assign the class id value if not assigned
            if (clsid == null)
            {
                clsid = new ESRI.ArcGIS.esriSystem.UIDClass {Value = "esriGeoDatabase.Feature"};
                //Works for shapefiles as well
            }

            IObjectClassDescription objectClassDescription = new FeatureClassDescriptionClass();

            // if a fields collection is not passed in then supply our own
            if (fields == null)
            {
                // create the fields using the required fields method
                fields = objectClassDescription.RequiredFields;
                var fieldsEdit = (IFieldsEdit)fields; // Explicit Cast
                IField field = new FieldClass();

                // create a user defined text field
                var fieldEdit = (IFieldEdit)field; // Explicit Cast

                // setup field properties
                fieldEdit.Name_2 = "SampleField";
                fieldEdit.Type_2 = esriFieldType.esriFieldTypeString;
                fieldEdit.IsNullable_2 = true;
                fieldEdit.AliasName_2 = "Sample Field Column";
                fieldEdit.DefaultValue_2 = "test";
                fieldEdit.Editable_2 = true;
                fieldEdit.Length_2 = 100;

                // add field to field collection
                fieldsEdit.AddField(field);
                fields = fieldsEdit;
            }

            string strShapeField = "";

            // locate the shape field
            for (int j = 0; j < fields.FieldCount; j++)
            {
                if (fields.Field[j].Type != esriFieldType.esriFieldTypeGeometry)
                    continue;
                strShapeField = fields.Field[j].Name;
                break;
            }

            // Use IFieldChecker to create a validated fields collection.
            IFieldChecker fieldChecker = new FieldCheckerClass();
            IEnumFieldError enumFieldError;
            IFields validatedFields;
            fieldChecker.ValidateWorkspace = (IWorkspace)workspace;
            fieldChecker.Validate(fields, out enumFieldError, out validatedFields);

            // The enumFieldError enumerator can be inspected at this point to determine 
            // which fields were modified during validation.


            // finally create and return the feature class
            featureClass = featureDataset == null
                               ? featureWorkspace.CreateFeatureClass(featureClassName, validatedFields, clsid, clsext,
                                                                     esriFeatureType.esriFTSimple, strShapeField,
                                                                     strConfigKeyword)
                               : featureDataset.CreateFeatureClass(featureClassName, validatedFields, clsid, clsext,
                                                                   esriFeatureType.esriFTSimple, strShapeField,
                                                                   strConfigKeyword);
            return featureClass;
        }
    }
}
