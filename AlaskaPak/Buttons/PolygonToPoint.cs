namespace NPS.AKRO.ArcGIS
{
    public class PolygonToPoint : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private static void MyClick()
        {
            Common.ArcToolBox.Invoke("FeatureVerticesToPoints_management");
        }
    }
}
