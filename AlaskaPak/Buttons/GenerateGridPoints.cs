namespace NPS.AKRO.ArcGIS
{
    public class GenerateGridPoints : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public GenerateGridPoints()
        {
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            Common.ArcToolBox.Invoke("FeatureToPoint_management");
        }
    }
}
