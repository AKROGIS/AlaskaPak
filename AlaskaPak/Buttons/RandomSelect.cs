using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.Geodatabase;
using NPS.AKRO.ArcGIS.Forms;
using NPS.AKRO.ArcGIS.Common;

namespace NPS.AKRO.ArcGIS.Buttons
{
    public class RandomSelect : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        private AlaskaPak _controller;
        private RandomFeatureSelectionForm _form;
        private List<NamedLayer> _selectableLayers;

        public RandomSelect()
        {
            AlaskaPak.RunProtected(GetType(), MyConstructor);
        }

        private void MyConstructor()
        {
            _controller = AlaskaPak.Controller;
            _controller.LayersChanged += Controller_LayersChanged;
            _selectableLayers = _controller.GetSelectableLayers();
            Enabled = MapHasSelectableLayer;
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            if (Enabled)
            {
                if (_form != null) //User may click when form is already loaded.
                {
                    _form.Activate();
                }
                else
                {
                    _form = new RandomFeatureSelectionForm();
                    _form.SelectedLayer += Form_SelectedLayer;
                    _form.FormClosed += Form_Closed;
                    LoadFormList();
                    _form.Show();
                }
            }
            else
            {
                MessageBox.Show(@"You must have one or more selectable feature layers in your map to use this command.",
                                @"For this command...", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private bool MapHasSelectableLayer
        {
            get { return _selectableLayers.Count > 0; }
        }

        private void LoadFormList()
        {
            _form.LoadList(_selectableLayers.Select(sl => new Tuple<string, int>
            {
                Item1 = sl.Name,
                Item2 = FeatureCount(sl.Layer)
            }));
        }

        #region Event Handlers

        //What we will do when the controller says the layers have changed
        private void Controller_LayersChanged()
        {
            _selectableLayers = _controller.GetSelectableLayers();
            Enabled = MapHasSelectableLayer;
            if (_form != null)
                LoadFormList();
        }

        //What we will do when the form says it has closed
        internal void Form_Closed(object sender, FormClosedEventArgs e)
        {
            _form = null;
        }

        //What we will do when the form says it has selected a layer
        internal void Form_SelectedLayer(object sender, RandomSelectEventArgs e)
        {
            RandomSelection(e.LayerIndex, e.Count);
            _form.Close();
        }

        #endregion

        #region Helper Functions (Tool Specific Logic)

        private static int FeatureCount(ILayer layer)
        {
            //casting the layer to ITable gets only the features in the
            //layer's query definition (i.e. those being shown
            var table = layer as ITable;
            if (table != null)
            {
                ISelectionSet oids = table.Select(null,
                                                            esriSelectionType.esriSelectionTypeHybrid,
                                                            esriSelectionOption.esriSelectionOptionNormal, null);
                return oids.Count;
            }
            return 0;
        }

        private void RandomSelection(int layerIndex, int count)
        {
            var layer = _selectableLayers[layerIndex].Layer as IFeatureLayer;
            //Debug.Assert(layer != null, "Selection layer not found");
            if (layer == null)
                return;

            //IFeatureSelection controls which features in a layer are selected
            var selectionLayer = layer as IFeatureSelection;
            if (selectionLayer == null)
                return;

            selectionLayer.Clear();
            //get the oids of just the features in the definition query
            //Don't query the feature class, because it returns all features
            ISelectionSet oids = ((ITable)layer).Select(null,
                                                        esriSelectionType.esriSelectionTypeHybrid,
                                                        esriSelectionOption.esriSelectionOptionNormal, null);
            IGeoDatabaseBridge2 helper = new GeoDatabaseHelperClass();

            if (count < oids.Count - count)
            {
                int[] oidsToAdd = BuildOidArray(oids, count);
                helper.AddList(selectionLayer.SelectionSet, oidsToAdd);
            }
            else
            {
                int[] oidsToRemove = BuildOidArray(oids, oids.Count - count);
                helper.RemoveList(oids, oidsToRemove);
                selectionLayer.SelectionSet = oids;
            }

            ArcMap.Document.UpdateContents();
            ArcMap.Document.ActiveView.Refresh();
        }

        private static int[] BuildOidArray(ISelectionSet set, int size)
        {
            if (size > set.Count)
                size = set.Count;
            if (size < 1)
                return new int[0];
            //int[] oids = new int[size];
            var oids = new HashSet<int>();

            var rand = new Random();
            IEnumIDs ids = set.IDs;
            while (oids.Count < size)
            {
                int oid = ids.Next();
                // If we get to the end of the list start over
                // If we start over, we need to be sure to not add the same item twice.
                // luckily we are using a Hashset.
                if (oid == -1)
                {
                    ids.Reset();
                    oid = ids.Next();
                    // I made sure ids has at least one member at the start of this method
                }
                // flip a coin - heads it goes in the list, tails it stays out.
                // this trick coin will land heads just the right percent of the time. 
                if (rand.Next(set.Count) <= size)
                    oids.Add(oid);
            }
            return oids.ToArray();
        }

        #endregion
    }
}
