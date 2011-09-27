using System;
using System.IO;
using System.Diagnostics;
using System.Windows.Forms;

namespace NPS.AKRO.ArcGIS.Buttons
{
    public class AlaskaPakHelp : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        private static string AssemblyDirectory
        {
            get
            {
                string codeBase = System.Reflection.Assembly.GetExecutingAssembly().CodeBase;
                var uri = new UriBuilder(codeBase);
                string path = Uri.UnescapeDataString(uri.Path);
                return Path.GetDirectoryName(path);
            }
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private static void MyClick()
        {
            string file = Path.Combine(AssemblyDirectory, Path.Combine("Help", "help.html"));
            if (File.Exists(file))
            {
                Process.Start(file);
            }
            else
            {
                MessageBox.Show(@"Unable to find the help files.",
                                @"Internal Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        protected override void OnUpdate()
        {
            Enabled = true;
        }
    }
}
