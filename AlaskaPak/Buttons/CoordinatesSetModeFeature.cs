namespace NPS.AKRO.ArcGIS
{
    public class CoordinatesSetModeFeature : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public CoordinatesSetModeFeature()
        {
        }

        protected override void OnClick()
        {
            System.Windows.Forms.MessageBox.Show(this.GetType().ToString() + " Not Available");
        }

        protected override void OnUpdate()
        {
            Enabled = false;
        }
    }
}
