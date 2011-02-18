using System;
using System.Collections.Generic;
using System.Linq;
using ESRI.ArcGIS.ArcMapUI;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.Desktop.AddIns;
using ESRI.ArcGIS.esriSystem;
using ESRI.ArcGIS.Geometry;
using NPS.AKRO.ArcGIS.Common;

namespace NPS.AKRO.ArcGIS
{
    public class AlaskaPak : Extension
    {
        internal static AlaskaPak Controller
        {
            get
            {
                // Instances of this class are created by ArcMap when needed
                // by calling FindExtension. (? assumed behavior)
                // The first instance created will assign to singleton, so we
                // only call FindExtension if we need to create the first instance.
                if (singleton == null)
                {
                    UID extID = new UIDClass();
                    extID.Value = ThisAddIn.IDs.AlaskaPak;
                    ArcMap.Application.FindExtensionByCLSID(extID);
                }
                return singleton;
            }
        }
        private static AlaskaPak singleton;

        //In a real singleton pattern, the constructor would be private.
        //However FindExtension() needs to create the instance, so we rely
        //on the good behavior of FindExtension, and my classes.
        public AlaskaPak()
        {
            singleton = this;
        }

        //My events
        public event Action LayersChanged;


        #region Extension methods
        
        protected override void OnStartup()
        {
            //Wire up event handlers
            AttachEventHandlersToMapDocument();
            AttachEventHandlersToActiveView();
        }

        protected override void OnShutdown()
        {
        }

        #endregion

        #region Map Event Handlers

        private void AttachEventHandlersToMapDocument()
        {
            IDocumentEvents_Event docEvents = ArcMap.Events;
            docEvents.ActiveViewChanged += new IDocumentEvents_ActiveViewChangedEventHandler(MapEvents_ActiveViewChanged);
            docEvents.MapsChanged += new IDocumentEvents_MapsChangedEventHandler(MapEvents_ContentsChanged);
        }

        private void MapEvents_ActiveViewChanged()
        {
            AttachEventHandlersToActiveView();
            //Pick up changes that may have occured on the inactive maps
            MapEvents_ContentsChanged();
        }

        void MapEvents_ContentsChanged()
        {
            //Notify subscribers of changes in map contents.
            OnLayersChanged();
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

        private void MapEvents_ItemAdded(object item)
        {
            if (item is ILayer)
                OnLayersChanged();
        }

        void MapEvents_ItemDeleted(object item)
        {
            if (item is ILayer)
                OnLayersChanged();
        }

        void MapEvents_ItemReordered(object item, int index)
        {
            if (item is ILayer)
                OnLayersChanged();
        }

        private void OnLayersChanged()
        {
            Action handle = LayersChanged;
            if (handle != null)
                handle();
        }

        #endregion

        #region Alaska Pak Logic

        internal List<NamedLayer> GetSelectableLayers()
        {
            return GetFeatureLayers().Where(x => ((IFeatureLayer)x.Layer).Selectable).ToList();
        }

        internal List<NamedLayer> GetPointLayers()
        {
            return GetFeatureLayers().Where(x => 
                ((IFeatureLayer)x.Layer).FeatureClass.ShapeType == esriGeometryType.esriGeometryPoint).ToList();
        }

        internal List<NamedLayer> GetFeatureLayers()
        {
            return GetLayers("{40A9E885-5533-11d0-98BE-00805F7CED21}"); // IFeatureLayer
        }

        internal List<NamedLayer> GetRasterLayers()
        {
            return GetLayers("{D02371C7-35F7-11D2-B1F2-00C04F8EDEFF}"); // IRasterLayer
        }

        internal List<NamedLayer> GetLayers(string type)
        {
            List<NamedLayer> namedNayers = new List<NamedLayer>();
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
                namedNayers.Add(new NamedLayer
                {
                    Name = name,
                    Layer = layer
                });
            }
            return namedNayers;
        }

        #endregion

    }

}
