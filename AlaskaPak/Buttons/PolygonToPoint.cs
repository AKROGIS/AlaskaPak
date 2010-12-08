namespace NPS.AKRO.ArcGIS
{
    public class PolygonToPoint : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public PolygonToPoint()
        {
        }

        protected override void OnClick()
        {
           Common.ArcToolBox.Invoke("FeatureVerticesToPoints_management");
        }

        protected override void OnUpdate()
        {
            Enabled = true;
        }

    }
}
