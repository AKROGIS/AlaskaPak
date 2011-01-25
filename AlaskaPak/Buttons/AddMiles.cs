namespace NPS.AKRO.ArcGIS
{
    public class AddMiles : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AddMiles()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "AddMiles");
        }
    }
}
