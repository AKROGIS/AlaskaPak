namespace NPS.AKRO.ArcGIS
{
    public class LineToRectangle : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public LineToRectangle()
        {
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "Line2Rect");
        }
    }
}
