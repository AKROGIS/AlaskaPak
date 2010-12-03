namespace NPS.AKRO.ArcGIS
{
    public class PointToPolygon : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public PointToPolygon()
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
