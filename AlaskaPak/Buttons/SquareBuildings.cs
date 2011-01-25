namespace NPS.AKRO.ArcGIS
{
    public class SquareBuildings : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public SquareBuildings()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "SquareBuildings");
        }
    }
}
