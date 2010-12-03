namespace NPS.AKRO.ArcGIS
{
    public class SetExtents : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public SetExtents()
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
