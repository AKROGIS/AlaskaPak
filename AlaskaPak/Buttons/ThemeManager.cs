using System;
using System.IO;
using System.Diagnostics;

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
            //return @"X:\GIS\ThemeMgrApp\Ver10.x\ThemeManager.exe";
            string datafile = Path.Combine(AssemblyDirectory, "PathToThemeManager.txt");
            using (var file = File.OpenText(datafile))
            {
                return file.ReadToEnd();
            }
        }

        protected override void OnClick()
        {
            string exe = GetExecutable();
            if (File.Exists(exe))
            {
                string directory = Path.GetDirectoryName(exe);
                ProcessStartInfo startInfo = new ProcessStartInfo(exe);
                startInfo.WorkingDirectory = directory;
                Process.Start(startInfo);
            }
            else
                System.Windows.Forms.MessageBox.Show("Path to Theme Manager is not valid.\n" + exe);
        }

        protected override void OnUpdate()
        {
            Enabled = (ArcMap.Application != null);
        }

    }
}
