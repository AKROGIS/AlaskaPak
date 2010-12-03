namespace NPS.AKRO.ArcGIS
{
    public class GenerateGridPoints : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public GenerateGridPoints()
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
