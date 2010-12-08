using ESRI.ArcGIS.esriSystem;
using ESRI.ArcGIS.Geoprocessing;
using ESRI.ArcGIS.GeoprocessingUI;

namespace NPS.AKRO.ArcGIS.Common
{
    class ArcToolBox
    {
        public static void Invoke(string tool)
        {
            UID uID = new UIDClass();
            uID.Value = "esriGeoprocessingUI.ArcToolboxExtension";

            IArcToolboxExtension arcToolboxExtension = ArcMap.Application.FindExtensionByCLSID(uID) as IArcToolboxExtension;
            if (arcToolboxExtension == null)
                return;

            IGPTool gpTool = arcToolboxExtension.ArcToolbox.GetToolbyNameString(tool);

            IGPToolCommandHelper gpCommandHelper = new GPToolCommandHelper();
            gpCommandHelper.SetTool(gpTool);
            gpCommandHelper.Invoke(null);
        }
    }
}
