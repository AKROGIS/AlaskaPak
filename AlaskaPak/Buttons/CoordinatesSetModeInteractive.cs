namespace NPS.AKRO.ArcGIS
{
    public class CoordinatesSetModeInteractive : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public CoordinatesSetModeInteractive()
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
