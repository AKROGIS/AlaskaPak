namespace NPS.AKRO.ArcGIS
{
    public class SetExtents : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public SetExtents()
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
