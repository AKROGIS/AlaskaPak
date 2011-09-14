namespace NPS.AKRO.ArcGIS
{
    public class PointToPolyline : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public PointToPolyline()
        {
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            Common.ArcToolBox.Invoke("PointsToLine_management");
        }
    }
}
