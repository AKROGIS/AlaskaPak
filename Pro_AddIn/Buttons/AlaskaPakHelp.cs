using ArcGIS.Desktop.Framework.Contracts;
using System;
using System.Diagnostics;
using System.IO;

namespace AlaskaPak.Buttons
{
    internal class AlaskaPakHelp : Button
    {
        protected override void OnClick()
        {
            var helpPath = Path.Combine(AssemblyDirectory, @"Help", "help.html");
            //TODO: protect from file not found, etc
            Process.Start(helpPath);
        }

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
    }
}
