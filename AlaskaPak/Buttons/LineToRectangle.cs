namespace NPS.AKRO.ArcGIS
{
    public class LineToRectangle : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public LineToRectangle()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "Line2Rect");
        }
    }
}
