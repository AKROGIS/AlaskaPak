namespace NPS.AKRO.ArcGIS
{
    public class AlaskaPakAbout : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private static void MyClick()
        {
            (new Forms.AboutAlaskaPak()).ShowDialog();
        }
    }
}
