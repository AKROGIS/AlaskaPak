namespace NPS.AKRO.ArcGIS
{
    public class AddGUID : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AddGUID()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke("AddGlobalIDs_management");
        }
    }
}
