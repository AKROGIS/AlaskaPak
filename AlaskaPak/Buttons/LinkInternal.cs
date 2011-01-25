namespace NPS.AKRO.ArcGIS
{
    public class LinkInternal : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public LinkInternal()
        {
        }

        protected override void OnClick()
        {
            System.Diagnostics.Process.Start("http://165.83.62.205/rgr/akgis/");
        }
    }
}
