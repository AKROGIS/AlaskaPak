using ESRI.ArcGIS.Framework;
using ESRI.ArcGIS.esriSystem;

namespace NPS.AKRO.ArcGIS
{
    public class GraphicsToFeatures : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public GraphicsToFeatures()
        {
        }

        protected override void OnClick()
        {
            UID uid = new UIDClass();
            uid.Value = "esriArcMapUI.GraphicsToFeaturesCommand";
            
            ICommandItem cmd = ArcMap.Application.Document.CommandBars.Find(uid);
            if (cmd == null)
                System.Windows.Forms.MessageBox.Show(this.GetType().Name + " Not Available");
            else
                cmd.Execute();
        }

        protected override void OnUpdate()
        {
            Enabled = true;
        }
    }
}
