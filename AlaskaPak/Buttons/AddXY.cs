namespace NPS.AKRO.ArcGIS
{
    public class AddXY : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AddXY()
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
