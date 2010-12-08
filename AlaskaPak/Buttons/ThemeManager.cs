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

        private string AssemblyDirectory
        {
            get
            {
                string codeBase = System.Reflection.Assembly.GetExecutingAssembly().CodeBase;
                UriBuilder uri = new UriBuilder(codeBase);
                string path = Uri.UnescapeDataString(uri.Path);
                return Path.GetDirectoryName(path);
            }
        }

        private string GetExecutable()
        {
            string datafile = Path.Combine(AssemblyDirectory, "PathToThemeManager.txt");
            try
            {
                using (var file = File.OpenText(datafile))
                {
                    return file.ReadToEnd();
                }
            }
            catch
            {
                return null;
            }
        }

        protected override void OnClick()
        {
            string exe = GetExecutable();
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

        protected override void OnUpdate()
        {
            Enabled = (ArcMap.Application != null);
        }

    }
}
