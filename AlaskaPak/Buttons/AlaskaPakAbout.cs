namespace NPS.AKRO.ArcGIS
{
    public class AlaskaPakAbout : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AlaskaPakAbout()
        {
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            Forms.AboutAlaskaPak _form = new Forms.AboutAlaskaPak();
            _form.ShowDialog();
        }
    }
}
