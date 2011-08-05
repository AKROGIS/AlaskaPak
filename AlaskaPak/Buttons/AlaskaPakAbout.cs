namespace NPS.AKRO.ArcGIS
{
    public class AlaskaPakAbout : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AlaskaPakAbout()
        {
        }

        protected override void OnClick()
        {
            //X:\GIS\Toolboxes\10.0\Alaska Pak Development.tbx
            if (Common.Settings.IsEditable("PathToToolbox"))
                Common.Settings.Set("PathToToolbox", @"C:\tmp");
            //Forms.AboutAlaskaPak _form = new Forms.AboutAlaskaPak();
            //_form.ShowDialog();
        }

    }
}
