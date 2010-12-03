namespace NPS.AKRO.ArcGIS
{
    public class ObscurePoints : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public ObscurePoints()
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
