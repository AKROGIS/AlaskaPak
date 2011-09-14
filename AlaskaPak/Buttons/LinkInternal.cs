namespace NPS.AKRO.ArcGIS
{
    public class LinkInternal : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public LinkInternal()
        {
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            System.Diagnostics.Process.Start("http://165.83.62.205/rgr/akgis/");
        }
    }
}
