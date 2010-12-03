namespace NPS.AKRO.ArcGIS
{
    public class RandomPoints : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public RandomPoints()
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
