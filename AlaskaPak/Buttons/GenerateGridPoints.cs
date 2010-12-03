namespace NPS.AKRO.ArcGIS
{
    public class GenerateGridPoints : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public GenerateGridPoints()
        {
        }

        protected override void OnClick()
        {
            System.Windows.Forms.MessageBox.Show("Another Bad Change");
        }

        protected override void OnUpdate()
        {
            Enabled = false;
        }
    }
}
