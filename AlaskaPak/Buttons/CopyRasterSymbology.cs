using System.Collections.Generic;
using System.Diagnostics;
using System.Linq;
using System.Windows.Forms;
using ESRI.ArcGIS.ArcMapUI;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.esriSystem;
using NPS.AKRO.ArcGIS.Forms;
using NPS.AKRO.ArcGIS.Common;

namespace NPS.AKRO.ArcGIS
{
    public class CopyRasterSymbology : ESRI.ArcGIS.Desktop.AddIns.Button
    {

        private CopyRasterSymbologyForm _form;
        private List<NamedRasterLayer> _rasterLayers;
        private struct NamedRasterLayer
        {
            internal IRasterLayer Layer;
            internal string Name;
        }

        //Enabled is defined in the Button base class and defaults to True.
        //This button cannot set its Enabled state until after it is instantiated by the user.
        //This occurs when the user clicks it for the first time in the UI (remember it defaulted to Enabled).
        //In addition to being instantiated, the new object gets the OnClick event.
        //Once this button is instantiated, it can maintain the state of Enabled which will
        //enable/disable the UI (and subsequent OnClick events).
        //We maintain the state of Enabled by monitoring ArcMap events.
        //We do not overrider the OnUpdate() method because the Enabled state is always current.

        public CopyRasterSymbology()
        {
            _rasterLayers = new List<NamedRasterLayer>();
            GetRasterLayers();
            Enabled = MapHasTwoOrMoreRasterLayers;
            //wire up event handlers to keep track of raster layers
            //(for maintaining state of Enabled and for form updates, if it is being displayed)
            AttachEventHandlersToMapDocument();
            AttachEventHandlersToActiveView();
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
                    _form = new CopyRasterSymbologyForm();
                    _form.CopyRasterEvent += FormEvent_Copy;
                    _form.FormClosed += FormEvent_Release;
                    _form.LoadLists(_rasterLayers.Select(rl => rl.Name));
                    _form.Show();
                }
            }
            else
            {
                MessageBox.Show("You must have two or more raster layers in your map to use this command.",
                    "For this command...", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private void GetRasterLayers()
        {
            _rasterLayers.Clear();
            string type = "{D02371C7-35F7-11D2-B1F2-00C04F8EDEFF}"; // IRasterLayer
            foreach (ILayer layer in LayerUtils.GetAllLayers(ArcMap.Document, type))
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
                _rasterLayers.Add(new NamedRasterLayer
                {
                    Name = name,
                    Layer = (IRasterLayer)layer
                });
            }
        }

        private bool MapHasTwoOrMoreRasterLayers
        {
            get { return _rasterLayers.Count > 1; }
        }

        #region Form Event Handlers

        internal void FormEvent_Release(object sender, FormClosedEventArgs e)
        {
            _form = null;
        }

        internal void FormEvent_Copy(object sender, CopyRasterEventArgs e)
        {
            Copy(e.Source, e.Targets);
            _form.Close();
        }

        private void Copy(int sourceLayerIndex, IEnumerable<int> targetLayerIndices)
        {
            IRasterLayer sourceLayer = _rasterLayers[sourceLayerIndex].Layer;
            Debug.Assert(sourceLayer != null, "Source layer not found");
            if (sourceLayer != null)
            {
                IObjectCopy objectCopier = new ObjectCopyClass(); 
                IRasterRenderer sourceRender = sourceLayer.Renderer;
                Debug.Assert(sourceRender != null, "Source layer has no renderer");
                if (sourceRender != null)
                {
                    foreach (int index in targetLayerIndices)
                    {
                        IRasterLayer destLayer = _rasterLayers[index].Layer;
                        Debug.Assert(destLayer != null, "Destination layer not found");
                        if (destLayer != null)
                            //destLayer.Renderer = sourceRender;  //layers share the same renderer
                            destLayer.Renderer = (IRasterRenderer)objectCopier.Copy(sourceRender);
                    }
                }
            }
            ArcMap.Document.UpdateContents();
            ArcMap.Document.ActiveView.Refresh();
        }

        #endregion

        #region Map Event Handlers

        private void AttachEventHandlersToMapDocument()
        {
            IDocumentEvents_Event docEvents = ArcMap.Events;
            docEvents.ActiveViewChanged += new IDocumentEvents_ActiveViewChangedEventHandler(MapEvents_ActiveViewChanged);
            docEvents.MapsChanged += new IDocumentEvents_MapsChangedEventHandler(MapEvents_ContentsChanged);
        }

        private void AttachEventHandlersToActiveView()
        {
            //Note: only the active map fires these events.  It is a COM error to add these events to a non-active map
            //There does not appear to be any way to get item added events from a non-active map
            //If maps are added (MapsChanged event), but FocusMap did not, then we will be adding duplicate events, so
            //we conservatively clear the handler before adding it (it not an error to remove a handler that is not there)
            IActiveViewEvents_Event ev = (IActiveViewEvents_Event)ArcMap.Document.FocusMap;
            ev.ItemAdded -= MapEvents_ItemAdded; //layer added to view/TOC
            ev.ItemAdded += MapEvents_ItemAdded;
            ev.ItemDeleted -= MapEvents_ItemDeleted;  //layer removed from view/TOC
            ev.ItemDeleted += MapEvents_ItemDeleted;
            ev.ItemReordered -= MapEvents_ItemReordered; //layer moved in view/TOC
            ev.ItemReordered += MapEvents_ItemReordered;
            ev.ContentsChanged -= MapEvents_ContentsChanged;  //view changed (fired when layer changes)
            ev.ContentsChanged += MapEvents_ContentsChanged;
        }

        private void MapEvents_ActiveViewChanged()
        {
            AttachEventHandlersToActiveView();
            //Pick up changes that may have occured on the inactive maps
            MapEvents_ContentsChanged();
        }

        private void MapEvents_ItemAdded(object item)
        {
            if (item is IRasterLayer)
                MapEvents_ContentsChanged();
        }

        void MapEvents_ItemDeleted(object item)
        {
            if (item is IRasterLayer) 
                MapEvents_ContentsChanged();
        }

        void MapEvents_ItemReordered(object item, int index)
        {
            if (item is IRasterLayer) 
                MapEvents_ContentsChanged();
        }

        void MapEvents_ContentsChanged()
        {
            GetRasterLayers();
            Enabled = MapHasTwoOrMoreRasterLayers;
            if (_form != null)
                _form.LoadLists(_rasterLayers.Select(rlayer => rlayer.Name));
        }

        #endregion

    }

}
