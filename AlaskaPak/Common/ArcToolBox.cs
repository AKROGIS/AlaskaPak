using ESRI.ArcGIS.esriSystem;
using ESRI.ArcGIS.Geoprocessing;
using ESRI.ArcGIS.GeoprocessingUI;
using ESRI.ArcGIS.Geodatabase;

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
            if (gpTool == null)
                return;

            IGPToolCommandHelper gpCommandHelper = new GPToolCommandHelper();
            gpCommandHelper.SetTool(gpTool);
            gpCommandHelper.Invoke(null);
        }

        public static void Invoke(string workspace, string toolbox, string tool)
        {
            IWorkspaceFactory factory = new ToolboxWorkspaceFactoryClass();
            IToolboxWorkspace toolboxWorkspace = (IToolboxWorkspace)factory.OpenFromFile(workspace, 0);
            if (toolboxWorkspace == null)
                return;

            IGPToolbox gpToolbox = toolboxWorkspace.OpenToolbox(toolbox);
            if (gpToolbox == null)
                return;

            IGPTool gpTool = gpToolbox.OpenTool(tool);
            if (gpTool == null)
                return;

            IGPToolCommandHelper gpCommandHelper = new GPToolCommandHelper();
            gpCommandHelper.SetTool(gpTool);
            gpCommandHelper.Invoke(null);
        }
    }
}
