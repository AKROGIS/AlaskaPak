using System.Windows.Forms;

using NPS.AKRO.ArcGIS.Forms;

namespace NPS.AKRO.ArcGIS
{
    public class RandomSelect : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        private RandomFeatureSelectionForm _form;

        public RandomSelect()
        {
        }

        protected override void OnClick()
        {
            if (Enabled)
            {
                if (_form != null) //User may click when form is already loaded.
                {
                    _form.Activate();
                }
                else
                {
                    _form = new RandomFeatureSelectionForm();
                    //_form.CopyRasterEvent += FormEvent_Copy;
                    //_form.FormClosed += FormEvent_Release;
                    //_form.LoadLists(_rasterLayers.Select(rl => rl.Name));
                    _form.Show();
                }
            }
            else
            {
                MessageBox.Show("You must have one or more feature layers in your map to use this command.",
                    "For this command...", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }
    }
}
