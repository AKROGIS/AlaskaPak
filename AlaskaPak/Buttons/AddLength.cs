namespace NPS.AKRO.ArcGIS
{
    public class AddLength : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AddLength()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "AddLength");
        }
    }
}
