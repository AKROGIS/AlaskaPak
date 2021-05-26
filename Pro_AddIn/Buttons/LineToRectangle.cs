using ArcGIS.Desktop.Core.Geoprocessing;
using ArcGIS.Desktop.Framework.Contracts;
using System.IO;

namespace AlaskaPak.Buttons
{
    internal class LineToRectangle : Button
    {
        protected override void OnClick()
        {
            string toolpath = Path.Combine(AlaskaPakModule.ToolboxPath, "LineToRectangle");
            Geoprocessing.OpenToolDialog(toolpath, null);
        }
    }
}
