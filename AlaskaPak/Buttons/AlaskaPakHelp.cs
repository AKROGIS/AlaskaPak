namespace NPS.AKRO.ArcGIS
{
    public class AlaskaPakHelp : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AlaskaPakHelp()
        {
        }

        protected override void OnClick()
        {
            System.Windows.Forms.MessageBox.Show(this.GetType().ToString() + " Not Available");
        }

        protected override void OnUpdate()
        {
            Enabled = true;
        }
    }
}
