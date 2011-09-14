namespace NPS.AKRO.ArcGIS
{
    public class AddArea : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AddArea()
        {
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "AddArea");
        }
    }
}
