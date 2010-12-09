namespace NPS.AKRO.ArcGIS
{
    public class ObscurePoints : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public ObscurePoints()
        {
        }

        protected override void OnClick()
        {
            Common.ArcToolBox.Invoke(@"T:\USER\Regan\AlaskaPak Toolbox", "Alaska Pak", "ObscurePoints");
        }

        protected override void OnUpdate()
        {
            Enabled = true;
        }
    }
}
