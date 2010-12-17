using System;
using System.IO;
using System.Diagnostics;
using System.Windows.Forms;

namespace NPS.AKRO.ArcGIS
{
    public class ThemeManager : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public ThemeManager()
        {
        }

        protected override void OnClick()
        {
            string exe = Common.Settings.Get("PathToThemeManager");
            if (exe == null)
            {
                MessageBox.Show("Can't find the data file with the path to Theme Manager.",
                    "Internal Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            if (File.Exists(exe))
            {
                string directory = Path.GetDirectoryName(exe);
                ProcessStartInfo startInfo = new ProcessStartInfo(exe);
                startInfo.WorkingDirectory = directory;
                Process.Start(startInfo);
            }
            else
                MessageBox.Show("Path to Theme Manager is not valid.\n" + exe, 
                    "Configuration Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }

    }
}
