namespace NPS.AKRO.ArcGIS
{
    public class RandomPoints : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public RandomPoints()
        {
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            Common.ArcToolBox.Invoke("CreateRandomPoints_management");
        }
    }
}
