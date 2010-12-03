namespace NPS.AKRO.ArcGIS
{
    public class CoordinatesZoomToMarker : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public CoordinatesZoomToMarker()
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
