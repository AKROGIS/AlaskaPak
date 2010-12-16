using System.Collections.Generic;
using NPS.AKRO.ArcGIS.Forms;
using System.Windows.Forms;
using ESRI.ArcGIS.Carto;
using System.Linq;
using ESRI.ArcGIS.Framework;
using ESRI.ArcGIS.esriSystem;
using ESRI.ArcGIS.ArcMapUI;

namespace NPS.AKRO.ArcGIS
{
    public class CopyRasterLegend : ESRI.ArcGIS.Desktop.AddIns.Button
    {

        private CopyRasterLegendForm form;

        public CopyRasterLegend()
        {
            Enabled = CheckForTwoRasterLayers();
            IActiveViewEvents_Event ev = (IActiveViewEvents_Event)ArcMap.Document.FocusMap;
            ev.ItemAdded += new IActiveViewEvents_ItemAddedEventHandler(MapEvents_ContentsChanged);
            ev.ItemDeleted += new  IActiveViewEvents_ItemDeletedEventHandler(MapEvents_ContentsChanged);
        }

        protected override void OnClick()
        {
            if (Enabled)
            {
                form = new CopyRasterLegendForm();
                form.CopyHandler += CopyHandler;
                form.LoadLists(GetRasterLayerList());
                form.Show();
            }
            else
            {
                MessageBox.Show("You must have two or more raster layers in your map to use this command.",
                    "For this command...", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        internal void CopyHandler(object sender, Forms.CopyRasterEventArgs e)
        {
            Copy(e.SourceName, e.DestinationNames);
            form.Close();
            form = null;
        }

        private void Copy(string sourceLayerName, IEnumerable<string> destinationLayerNames)
        {
            //FIXME - implement copy()
            MessageBox.Show("Copy " + sourceLayerName + " to " + destinationLayerNames.ToString());
        }
        
        /// <summary>
        /// Check the map for two or more raster layers 
        /// </summary>
        /// <returns>True if map has two or more raster layers; false otherwise</returns>
        private bool CheckForTwoRasterLayers()
        {
            return GetRasterLayerList().Count() > 1;
        }

        void MapEvents_ContentsChanged(object item)
        {
            Enabled = CheckForTwoRasterLayers();
            if (Enabled && form != null)
                form.LoadLists(GetRasterLayerList());
        }

        private IEnumerable<string> GetRasterLayerList()
        {
            UID uid = new UIDClass();
            uid.Value = "{D02371C7-35F7-11D2-B1F2-00C04F8EDEFF}";  // IRasterLayer
            List<string> names = new List<string>();
            IMaps maps = ArcMap.Document.Maps;
            for (int i = 0; i < maps.Count; i++)
            {
                IMap map =  maps.Item[i];
                IEnumLayer layers = map.get_Layers(uid);
                ILayer layer = layers.Next();
                while (layer != null)
                {
                    names.Add(map.Name + "::" + GetFullName(map,layer));
                    layer = layers.Next();
                }
            }
            return names;
        }

        private string GetFullName(IMap map, ILayer layer, string separator = @"//")
        {
            for (int i = 0; i < map.LayerCount; i++)
            {
                if (map.Layer[i] == layer)
                {
                    return layer.Name;
                }
                else
                {
                    if (map.Layer[i] is ICompositeLayer)
                    {
                        string name = GetFullName((ICompositeLayer)map.Layer[i], layer, separator);
                        if (name != null)
                        {
                            return map.Layer[i].Name + separator + name;
                        }
                    }
                }
            }
            return null;
        }

        private string GetFullName(ICompositeLayer parent, ILayer layer, string separator = @"//")
        {
            for (int i = 0; i < parent.Count; i++)
            {
                if (parent.Layer[i] == layer)
                {
                    return layer.Name;
                }
                else
                {
                    if (parent.Layer[i] is ICompositeLayer)
                    {
                        string name = GetFullName((ICompositeLayer)parent.Layer[i], layer, separator);
                        if (name != null)
                        {
                            return parent.Layer[i].Name + separator + name;
                        }
                    }
                }
            }
            return null;
        }

    }
}
