using ArcGIS.Desktop.Core.Geoprocessing;
using ArcGIS.Desktop.Framework.Contracts;
using System.IO;

namespace AlaskaPak.Buttons
{
    internal class PolygonFromPoint : Button
    {
        protected override void OnClick()
        {
            string toolpath = Path.Combine(AlaskaPakModule.ToolboxPath, "PolygonFromPoint");
            Geoprocessing.OpenToolDialog(toolpath, null);
        }
    }
}
