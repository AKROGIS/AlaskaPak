namespace NPS.AKRO.ArcGIS
{
    public class RandomTransects : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public RandomTransects()
        {
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "RandomTransects");
        }
    }
}
