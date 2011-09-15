namespace NPS.AKRO.ArcGIS
{
    public class PointToPolygon : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private static void MyClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "Point2Poly");
        }
    }
}
