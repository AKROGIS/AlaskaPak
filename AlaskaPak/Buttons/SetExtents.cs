using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.Geometry;
using System.Windows.Forms;

namespace NPS.AKRO.ArcGIS
{
    public class SetExtents : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private static void MyClick()
        {
            int mapCount = ArcMap.Document.Maps.Count;
            if (mapCount <= 1)
            {
                MessageBox.Show(@"You must have more than 1 data frame in the current map document.",
                                @"For this command...", MessageBoxButtons.OK, MessageBoxIcon.Information);
                return;
            }

            string warning = null;
            for (int i = 0; i < mapCount; ++i)
            {
                if (ArcMap.Document.Maps.Item[i].SpatialReference == null ||
                    ArcMap.Document.Maps.Item[i].SpatialReference is IUnknownCoordinateSystem)
                {
                    warning = "One or more data frames do not have a well known coordinate system."
                              + System.Environment.NewLine + "Results will be undefined.";
                    break;
                }
            }
            if (warning != null)
            {
                DialogResult answer = MessageBox.Show(warning, @"Warning", MessageBoxButtons.OKCancel,
                                                      MessageBoxIcon.Warning);
                if (answer == DialogResult.Cancel)
                    return;
            }

            IMap focusMap = ArcMap.Document.FocusMap;
            IEnvelope extents = ((IActiveView)focusMap).Extent;
            string msg = "The following data frames";
            for (int i = 0; i < mapCount; ++i)
            {
                IMap currentMap = ArcMap.Document.Maps.Item[i];
                if (currentMap == focusMap)
                    continue;
                if (currentMap.SpatialReference != null && extents.SpatialReference != null &&
                    !(currentMap.SpatialReference is IUnknownCoordinateSystem) &&
                    !(extents.SpatialReference is IUnknownCoordinateSystem))
                    //results of project are undefined if either SR is null or unknown, so don't do it.
                    extents.Project(currentMap.SpatialReference);
                ((IActiveView)currentMap).Extent = extents;
                ((IActiveView)currentMap).Refresh();
                msg = msg + System.Environment.NewLine + "\t" + currentMap.Name;
            }
            msg = msg + System.Environment.NewLine + "were adjusted to match the extents of" +
                  System.Environment.NewLine + "\t" + focusMap.Name;
            MessageBox.Show(msg, @"Extents changed", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        protected override void OnUpdate()
        {
            Enabled = (ArcMap.Document.Maps.Count > 1);
        }
    }
}
