namespace NPS.AKRO.ArcGIS
{
    public class RandomTransects : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private static void MyClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "RandomTransects");
        }
    }
}
