using ArcGIS.Desktop.Core.Geoprocessing;
using ArcGIS.Desktop.Framework.Contracts;
using System.IO;

namespace AlaskaPak.Buttons
{
    internal class PolygonToPoints : Button
    {
        protected override void OnClick()
        {
            Geoprocessing.OpenToolDialog("management.FeatureVerticesToPoints", null);
        }
    }
}
