namespace NPS.AKRO.ArcGIS
{
    public class ObscurePoints : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private static void MyClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "ObscurePoints");
        }
    }
}
