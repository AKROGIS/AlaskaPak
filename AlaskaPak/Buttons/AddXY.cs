namespace NPS.AKRO.ArcGIS
{
    public class AddXY : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AddXY()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke("AddXY_management");
        }

        protected override void OnUpdate()
        {
            Enabled = false;
        }
    }
}
