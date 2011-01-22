using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Windows.Forms;
using ESRI.ArcGIS.ArcMapUI;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.Geodatabase;
using ESRI.ArcGIS.esriSystem;
using NPS.AKRO.ArcGIS.Forms;
using NPS.AKRO.ArcGIS.Common;


namespace NPS.AKRO.ArcGIS
{
    public class RandomSelect : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        private RandomFeatureSelectionForm _form;
        private List<NamedSelectableLayer> _selectableLayers;
        private struct NamedSelectableLayer
        {
            internal IFeatureLayer Layer;
            internal string Name;
        }

        public RandomSelect()
        {
            _selectableLayers = new List<NamedSelectableLayer>();
            GetSelectableLayers();
            Enabled = MapHasSelectableLayer;
            //wire up event handlers to keep track of raster layers
            //(for maintaining state of Enabled and for form updates, if it is being displayed)
            //AttachEventHandlersToMapDocument();
            //AttachEventHandlersToActiveView();
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
                    _form = new RandomFeatureSelectionForm();
                    _form.RandomSelectEvent += FormEvent_Select;
                    _form.FormClosed += FormEvent_Release;
                    _form.LoadList(_selectableLayers.Select(sl => sl.Name));
                    _form.Show();
                }
            }
            else
            {
                MessageBox.Show("You must have one or more selectable feature layers in your map to use this command.",
                    "For this command...", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private void GetSelectableLayers()
        {
            _selectableLayers.Clear();
            string type = "{40A9E885-5533-11d0-98BE-00805F7CED21}"; // IFeatureLayer
            foreach (IFeatureLayer layer in LayerUtils.GetAllLayers(ArcMap.Document, type))
            {
                if (layer.Selectable)
                {
                    string name = null;
                    if (ArcMap.Document.Maps.Count > 1)
                    {
                        name = LayerUtils.GetFullName(ArcMap.Document, layer);
                    }
                    else
                    {
                        name = LayerUtils.GetFullName(ArcMap.Document.Maps.Item[0], layer);
                    }
                    _selectableLayers.Add(new NamedSelectableLayer
                    {
                        Name = name,
                        Layer = (IFeatureLayer)layer
                    });
                }
            }
        }

        private bool MapHasSelectableLayer
        {
            get { return _selectableLayers.Count > 0; }
        }

        #region Form Event Handlers

        internal void FormEvent_Release(object sender, FormClosedEventArgs e)
        {
            _form = null;
        }

        internal void FormEvent_Select(object sender, RandomSelectEventArgs e)
        {
            RandomSelection(e.LayerIndex, e.Count);
            _form.Close();
        }

        private void RandomSelection(int layerIndex, int count)
        {
            IFeatureLayer layer = _selectableLayers[layerIndex].Layer as IFeatureLayer;
            Debug.Assert(layer != null, "Selection layer not found");
            if (layer != null)
            {
                //IFeatureSelection controls which features in a layer are selected
                IFeatureSelection selectionLayer = layer as IFeatureSelection;
                selectionLayer.Clear();

                //get the oids of just the features in the definition query
                //Don't query the feature class, because it returns all features
                ISelectionSet oids = ((ITable)layer).Select(null,
                    esriSelectionType.esriSelectionTypeHybrid,
                    esriSelectionOption.esriSelectionOptionNormal, null);
                IGeoDatabaseBridge2 helper = new GeoDatabaseHelperClass();

                if (count < oids.Count - count)
                {
                    int[] oidsToAdd = BuildOidArray(oids, count); ;
                    helper.AddList(selectionLayer.SelectionSet, oidsToAdd);
                }
                else
                {
                    int[] oidsToRemove = BuildOidArray(oids, oids.Count - count); ;
                    helper.RemoveList(oids, oidsToRemove);
                    selectionLayer.SelectionSet = oids;
                }
            }
            ArcMap.Document.UpdateContents();
            ArcMap.Document.ActiveView.Refresh();
        }

        private int[] BuildOidArray(ISelectionSet set, int size)
        {
            if (size > set.Count)
                size = set.Count;
            if (size < 1)
                return new int[0];
            //int[] oids = new int[size];
            HashSet<int> oids = new HashSet<int>();

            Random rand = new Random();
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
