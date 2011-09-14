namespace NPS.AKRO.ArcGIS
{
    public class TableToShape : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public TableToShape()
        {
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "Table2Shape");
        }
    }
}
