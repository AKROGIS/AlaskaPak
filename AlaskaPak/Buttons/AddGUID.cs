namespace NPS.AKRO.ArcGIS
{
    public class AddGUID : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AddGUID()
        {
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            Common.ArcToolBox.Invoke("AddGlobalIDs_management");
        }
    }
}
