namespace NPS.AKRO.ArcGIS
{
    public class ResizeGrid : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public ResizeGrid()
        {
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            System.Windows.Forms.MessageBox.Show(this.GetType().Name + " Not Available");
        }

        protected override void OnUpdate()
        {
            Enabled = false;
        }
    }
}
