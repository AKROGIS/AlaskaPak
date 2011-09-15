namespace NPS.AKRO.ArcGIS
{
    public class GenerateGridPoints : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private static void MyClick()
        {
            Common.ArcToolBox.Invoke("FeatureToPoint_management");
        }
    }
}
