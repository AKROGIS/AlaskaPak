namespace NPS.AKRO.ArcGIS
{
    public class LinkExternal : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private static void MyClick()
        {
            System.Diagnostics.Process.Start("http://www.nps.gov/akso/gis/");
        }
    }
}
