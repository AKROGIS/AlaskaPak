namespace NPS.AKRO.ArcGIS
{
    public class AddAcres : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AddAcres()
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
