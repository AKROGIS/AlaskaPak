namespace NPS.AKRO.ArcGIS
{
    public class PolygonToPoint : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public PolygonToPoint()
        {
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            Common.ArcToolBox.Invoke("FeatureVerticesToPoints_management");
        }
    }
}
