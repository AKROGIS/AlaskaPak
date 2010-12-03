namespace NPS.AKRO.ArcGIS
{
    public class SquareBuildings : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public SquareBuildings()
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
