namespace NPS.AKRO.ArcGIS
{
    public class RandomSelect : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public RandomSelect()
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
