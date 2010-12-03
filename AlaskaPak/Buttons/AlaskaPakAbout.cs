namespace NPS.AKRO.ArcGIS
{
    public class AlaskaPakAbout : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AlaskaPakAbout()
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
