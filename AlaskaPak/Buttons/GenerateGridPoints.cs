namespace NPS.AKRO.ArcGIS
{
    public class GenerateGridPoints : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public GenerateGridPoints()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke("FeatureToPoint_management");
        }
    }
}
