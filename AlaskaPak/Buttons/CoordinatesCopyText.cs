namespace NPS.AKRO.ArcGIS
{
    public class CoordinatesCopyText : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public CoordinatesCopyText()
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
