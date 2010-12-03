namespace NPS.AKRO.ArcGIS
{
    public class PointToPolygon : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public PointToPolygon()
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
