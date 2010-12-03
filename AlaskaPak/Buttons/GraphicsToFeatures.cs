namespace NPS.AKRO.ArcGIS
{
    public class GraphicsToFeatures : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public GraphicsToFeatures()
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
