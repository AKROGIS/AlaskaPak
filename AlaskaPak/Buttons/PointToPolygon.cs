namespace NPS.AKRO.ArcGIS
{
    public class PointToPolygon : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public PointToPolygon()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "Point2Poly");
        }
    }
}
