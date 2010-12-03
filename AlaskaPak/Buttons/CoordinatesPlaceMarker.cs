namespace NPS.AKRO.ArcGIS
{
    public class CoordinatesPlaceMarker : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public CoordinatesPlaceMarker()
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
