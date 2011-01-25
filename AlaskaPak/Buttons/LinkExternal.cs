namespace NPS.AKRO.ArcGIS
{
    public class LinkExternal : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public LinkExternal()
        {
        }

        protected override void OnClick()
        {
            System.Diagnostics.Process.Start("http://www.nps.gov/akso/gis/");
        }
    }
}
