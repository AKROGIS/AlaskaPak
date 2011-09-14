namespace NPS.AKRO.ArcGIS
{
    public class SquareBuildings : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public SquareBuildings()
        {
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "SquareBuildings");
        }
    }
}
