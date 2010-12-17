using System;
using System.IO;
using System.Windows.Forms;
using NPS.AKRO.ArcGIS.Common;

namespace NPS.AKRO.ArcGIS
{
    public class ObscurePoints : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        private const string _toolName = "ObscurePoints";

        public ObscurePoints()
        {
        }

        protected override void OnClick()
        {
            string toolboxPath = Settings.Get("PathToToolbox");
            if (toolboxPath == null)
            {
                MessageBox.Show("Can't find the Setting 'PathToToolbox'.",
                    "Internal Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                Enabled = false;
                return;
            }
            if (File.Exists(toolboxPath))
            {
                string directory = Path.GetDirectoryName(toolboxPath);
                string toolbox = Path.GetFileNameWithoutExtension(toolboxPath);
                try
                {
                    ArcToolBox.Invoke(directory, toolbox, _toolName);
                }
                catch
                {
                    MessageBox.Show("Unable to find tool: " + _toolName + Environment.NewLine + "in toolbox: " +  toolboxPath,
                        "Configuration Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }

            }
            else
                MessageBox.Show("Path to Alaska Pak Toolbox is not valid." + Environment.NewLine + toolboxPath,
                    "Configuration Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
}
