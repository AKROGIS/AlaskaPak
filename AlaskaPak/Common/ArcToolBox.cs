using System;
using System.IO;
using System.Runtime.InteropServices;
using System.Windows.Forms;
using ESRI.ArcGIS.esriSystem;
using ESRI.ArcGIS.Geoprocessing;
using ESRI.ArcGIS.GeoprocessingUI;
using ESRI.ArcGIS.Geodatabase;

namespace NPS.AKRO.ArcGIS.Common
{
    internal class ArcToolBox
    {
        internal static void Invoke(string tool)
        {
            UID uniqueId = new UIDClass();
            uniqueId.Value = "esriGeoprocessingUI.ArcToolboxExtension";

            var arcToolboxExtension = ArcMap.Application.FindExtensionByCLSID(uniqueId) as IArcToolboxExtension;
            if (arcToolboxExtension == null)
                return;

            IGPTool gpTool = null;
            try
            {
                gpTool = arcToolboxExtension.ArcToolbox.GetToolbyNameString(tool);
            }
            catch (COMException)
            {
                MessageBox.Show(@"Unable to find tool: " + tool + Environment.NewLine + @"in the system toolbox.",
                                @"Configuration Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            if (gpTool == null)
                return;

            IGPToolCommandHelper gpCommandHelper = new GPToolCommandHelper();
            gpCommandHelper.SetTool(gpTool);
            gpCommandHelper.Invoke(null);
        }

        internal static void Invoke(string toolboxPath, string tool)
        {
            if (toolboxPath == null)
            {
                MessageBox.Show(@"Can't find the Setting 'PathToToolbox'.",
                                @"Internal Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            if (File.Exists(toolboxPath))
            {
                string directory = Path.GetDirectoryName(toolboxPath);
                string toolbox = Path.GetFileNameWithoutExtension(toolboxPath);
                try
                {
                    Invoke(directory, toolbox, tool);
                }
                catch (COMException)
                {
                    MessageBox.Show(
                        @"Unable to find tool: " + tool + Environment.NewLine + @"in toolbox: " + toolboxPath,
                        @"Configuration Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            else
                MessageBox.Show(@"Path to Alaska Pak Toolbox is not valid." + Environment.NewLine + toolboxPath,
                                @"Configuration Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

        private static void Invoke(string workspace, string toolbox, string tool)
        {
            IWorkspaceFactory factory = new ToolboxWorkspaceFactoryClass();
            var toolboxWorkspace = (IToolboxWorkspace)factory.OpenFromFile(workspace, 0);
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
