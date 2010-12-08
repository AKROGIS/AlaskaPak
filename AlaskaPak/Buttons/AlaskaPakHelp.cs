using System;
using System.IO;
using System.Diagnostics;
using System.Windows.Forms;

namespace NPS.AKRO.ArcGIS
{
    public class AlaskaPakHelp : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AlaskaPakHelp()
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

        protected override void OnClick()
        {
            string file = Path.Combine(AssemblyDirectory, Path.Combine("Help", "help.html"));
            if (File.Exists(file))
            {
                Process.Start(file);
            }
            else
            {
                MessageBox.Show("Unable to find the help files.\n",
                    "Internal Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        protected override void OnUpdate()
        {
            Enabled = true;
        }
    }
}
