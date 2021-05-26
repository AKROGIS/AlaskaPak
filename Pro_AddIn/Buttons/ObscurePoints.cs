using ArcGIS.Desktop.Core.Geoprocessing;
using ArcGIS.Desktop.Framework.Contracts;
using System.IO;

namespace AlaskaPak.Buttons
{
    internal class ObscurePoints : Button
    {
        protected override void OnClick()
        {
            string toolpath = Path.Combine(AlaskaPakModule.ToolboxPath, "ObscurePoints");
            Geoprocessing.OpenToolDialog(toolpath, null);
        }
    }
}
