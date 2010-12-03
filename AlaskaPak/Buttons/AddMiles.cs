namespace NPS.AKRO.ArcGIS
{
    public class AddMiles : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AddMiles()
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
