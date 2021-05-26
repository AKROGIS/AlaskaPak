namespace NPS.AKRO.ArcGIS.Buttons
{
    public class AnimateFeatures : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private static void MyClick()
        {
            System.Windows.Forms.MessageBox.Show(
                @"Animate Features functionality is now provided by ArcGIS 10.
See 'Using the Time Slider Window' in the ArcGIS help."
                );
        }
    }
}
