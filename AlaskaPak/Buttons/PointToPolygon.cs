namespace NPS.AKRO.ArcGIS
{
    public class PointToPolygon : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public PointToPolygon()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke("PointsToLine_management");
        }

        protected override void OnUpdate()
        {
            Enabled = true;
        }
    }
}
