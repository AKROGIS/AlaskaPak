namespace NPS.AKRO.ArcGIS
{
    public class AddID : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AddID()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "AddID");
        }
    }
}
