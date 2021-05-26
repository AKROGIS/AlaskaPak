using ArcGIS.Desktop.Core.Geoprocessing;
using ArcGIS.Desktop.Framework.Contracts;
using System.IO;

namespace AlaskaPak.Buttons
{
    internal class AddGuid : Button
    {
        protected override void OnClick()
        {
            Geoprocessing.OpenToolDialog("management.AddGlobalIDs", null);
        }
    }
}
