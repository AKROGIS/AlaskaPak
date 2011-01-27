namespace NPS.AKRO.ArcGIS
{
    public class AddArea : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AddArea()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "AddArea");
        }
    }
}
