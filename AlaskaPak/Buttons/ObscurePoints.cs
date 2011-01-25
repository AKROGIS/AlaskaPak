namespace NPS.AKRO.ArcGIS
{
    public class ObscurePoints : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public ObscurePoints()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "ObscurePoints");
        }
    }
}
