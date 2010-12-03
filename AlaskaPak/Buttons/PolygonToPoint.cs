using ESRI.ArcGIS.Geoprocessing;
using ESRI.ArcGIS.GeoprocessingUI;
using ESRI.ArcGIS.esriSystem;

namespace NPS.AKRO.ArcGIS
{
    public class PolygonToPoint : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public PolygonToPoint()
        {
        }

        protected override void OnClick()
        {
            UID uID = new UIDClass();
            uID.Value = "esriGeoprocessingUI.ArcToolboxExtension";

            IArcToolboxExtension arcToolboxExtension = ArcMap.Application.FindExtensionByCLSID(uID) as IArcToolboxExtension;
            if (arcToolboxExtension == null)
                return;

            IGPTool gpTool = arcToolboxExtension.ArcToolbox.GetToolbyNameString("FeatureVerticesToPoints_management");

            IGPToolCommandHelper gpCommandHelper = new GPToolCommandHelper();
            gpCommandHelper.SetTool(gpTool);
            gpCommandHelper.Invoke(null);
        }

        protected override void OnUpdate()
        {
            Enabled = true;
        }

    }
}
