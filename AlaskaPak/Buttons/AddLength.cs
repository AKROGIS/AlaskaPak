namespace NPS.AKRO.ArcGIS
{
    public class AddLength : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AddLength()
        {
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "AddLength");
        }
    }
}
