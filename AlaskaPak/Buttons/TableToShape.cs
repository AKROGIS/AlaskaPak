namespace NPS.AKRO.ArcGIS
{
    public class TableToShape : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public TableToShape()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "Table2Shape");
        }
    }
}
