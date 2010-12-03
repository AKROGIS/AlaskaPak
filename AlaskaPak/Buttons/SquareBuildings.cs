namespace NPS.AKRO.ArcGIS
{
    public class SquareBuildings : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public SquareBuildings()
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
