using System;
using System.IO;

namespace NPS.AKRO.ArcGIS.Common
{
    class Settings
    {
        public static string Get(string setting)
        {
            string datafile = Path.Combine(AssemblyDirectory, setting + ".txt");
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

        private static string AssemblyDirectory
        {
            get
            {
                string codeBase = System.Reflection.Assembly.GetExecutingAssembly().CodeBase;
                UriBuilder uri = new UriBuilder(codeBase);
                string path = Uri.UnescapeDataString(uri.Path);
                return Path.GetDirectoryName(path);
            }
        }

        public static bool IsEditable (string setting)
        {
            string datafile = Path.Combine(AssemblyDirectory, setting + ".txt");
            try
            {
                using (var s = File.OpenWrite(datafile))
                    return true;
            }
            catch
            {
                return false;
            }
        }

        public static void Set(string name, string setting)
        {
            string datafile = Path.Combine(AssemblyDirectory, name + ".txt");
            try
            {
                File.WriteAllText(datafile, setting);
            }
            catch
            {
                ;
            }
        }


    }
}
