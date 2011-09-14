namespace NPS.AKRO.ArcGIS
{
    public class AnimateFeatures : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AnimateFeatures()
        {
        }

        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private void MyClick()
        {
            System.Windows.Forms.MessageBox.Show("Animate Features functionality is now provided by ArcGIS 10" +
                                                 System.Environment.NewLine +
                                                 "See 'Using the Time Slider Window' in the ArcGIS help.");
        }
    }
}
