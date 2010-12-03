namespace NPS.AKRO.ArcGIS
{
    public class CoordinatesSetModeInteractive : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public CoordinatesSetModeInteractive()
        {
        }

        protected override void OnClick()
        {
            System.Windows.Forms.MessageBox.Show(this.GetType().Name + " Not Available");
        }

        protected override void OnUpdate()
        {
            Enabled = false;
        }
    }
}
