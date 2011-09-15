namespace NPS.AKRO.ArcGIS
{
    public class ResizeGrid : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public ResizeGrid()
        {
            Enabled = false;
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            System.Windows.Forms.MessageBox.Show(GetType() + @" Not Available");
        }
    }
}
