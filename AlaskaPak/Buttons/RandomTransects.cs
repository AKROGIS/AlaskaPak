namespace NPS.AKRO.ArcGIS
{
    public class RandomTransects : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public RandomTransects()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "RandomTransects");
        }
    }
}
