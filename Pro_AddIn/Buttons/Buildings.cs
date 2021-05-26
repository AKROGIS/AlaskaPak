using ArcGIS.Desktop.Core.Geoprocessing;
using ArcGIS.Desktop.Framework.Contracts;
using System.IO;

namespace AlaskaPak.Buttons
{
    internal class Buildings : Button
    {
        protected override void OnClick()
        {
            string toolpath = Path.Combine(AlaskaPakModule.ToolboxPath, "Buildings");
            Geoprocessing.OpenToolDialog(toolpath, null);
        }
    }
}
