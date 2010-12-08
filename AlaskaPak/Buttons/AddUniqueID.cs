namespace NPS.AKRO.ArcGIS
{
    public class AddUniqueID : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AddUniqueID()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke("AddGlobalIDs_management");
        }

        protected override void OnUpdate()
        {
            Enabled = false;
        }
    }
}
