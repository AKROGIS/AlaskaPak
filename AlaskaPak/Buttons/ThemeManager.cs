using System.Diagnostics;

namespace NPS.AKRO.ArcGIS
{
    public class ThemeManager : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public ThemeManager()
        {
        }

        protected override void OnClick()
        {
            string directory = @"X:\GIS\ThemeMgrApp\Ver10.x";
            ProcessStartInfo startInfo = new ProcessStartInfo(directory + @"\ThemeManager.exe");
            startInfo.WorkingDirectory = directory;
            Process.Start(startInfo);
        }

        protected override void OnUpdate()
        {
            Enabled = (ArcMap.Application != null);
        }

    }
}
