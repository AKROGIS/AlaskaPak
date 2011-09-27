namespace NPS.AKRO.ArcGIS.Buttons
{
    public class LinkInternal : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private static void MyClick()
        {
            System.Diagnostics.Process.Start("http://165.83.62.205/rgr/akgis/");
        }
    }
}
