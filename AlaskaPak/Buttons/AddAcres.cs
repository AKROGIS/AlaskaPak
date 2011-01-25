namespace NPS.AKRO.ArcGIS
{
    public class AddAcres : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AddAcres()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "AddAcres");
        }
    }
}
