namespace NPS.AKRO.ArcGIS
{
    public class CoordinatesSetModeLocked : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public CoordinatesSetModeLocked()
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
