namespace NPS.AKRO.ArcGIS
{
    public class CopyRasterLegend : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public CopyRasterLegend()
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
