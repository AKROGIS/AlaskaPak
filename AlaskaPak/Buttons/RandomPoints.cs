namespace NPS.AKRO.ArcGIS
{
    public class RandomPoints : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public RandomPoints()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke("CreateRandomPoints_management");
        }
    }
}
