namespace NPS.AKRO.ArcGIS
{
    public class AnimateFeatures : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AnimateFeatures()
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
