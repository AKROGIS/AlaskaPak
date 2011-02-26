namespace NPS.AKRO.ArcGIS
{
    public class AnimateFeatures : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AnimateFeatures()
        {
        }

        protected override void OnClick()
        {
            System.Windows.Forms.MessageBox.Show("Animate Features functionality is now provided by ArcGIS 10\n" +
                "See 'Using the Time Slider Window' in the ArcGIS help.");
        }

    }
}
