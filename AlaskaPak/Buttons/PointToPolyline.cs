namespace NPS.AKRO.ArcGIS
{
    public class PointToPolyline : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public PointToPolyline()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke("PointsToLine_management");
        }
    }
}
