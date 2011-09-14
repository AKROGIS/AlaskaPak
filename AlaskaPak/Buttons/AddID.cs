namespace NPS.AKRO.ArcGIS
{
    public class AddID : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AddID()
        {
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "AddID");
        }
    }
}
