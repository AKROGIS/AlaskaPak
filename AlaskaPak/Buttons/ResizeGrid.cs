namespace NPS.AKRO.ArcGIS
{
    public class ResizeGrid : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            Enabled = false;
            System.Windows.Forms.MessageBox.Show(GetType() + @" Not Available");
        }
    }
}
