namespace NPS.AKRO.ArcGIS
{
    public class RandomTransects : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public RandomTransects()
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
