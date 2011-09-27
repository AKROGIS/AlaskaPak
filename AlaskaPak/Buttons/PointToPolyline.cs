namespace NPS.AKRO.ArcGIS.Buttons
{
    public class PointToPolyline : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private static void MyClick()
        {
            Common.ArcToolBox.Invoke("PointsToLine_management");
        }
    }
}
