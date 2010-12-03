using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.Display;
using ESRI.ArcGIS.Geometry;

namespace NPS.AKRO.ArcGIS
{
    public class GenerateGrid : ESRI.ArcGIS.Desktop.AddIns.Tool
    {
        private bool _enabled;

        public GenerateGrid()
        {
            _enabled = CheckForCoordinateSystem();
        }

        protected override void OnUpdate()
        {
            this.Enabled = _enabled;
        }

        protected override void OnMouseDown(MouseEventArgs arg)
        {
            IScreenDisplay screenDisplay = ((IActiveView)ArcMap.Document.ActiveView.FocusMap).ScreenDisplay;
            IRubberBand rubberEnv = new RubberEnvelope();
            IEnvelope envelope = rubberEnv.TrackNew(screenDisplay, null) as IEnvelope;
            if (envelope.IsEmpty)
                return;
        }

        void MapEvents_ContentsChanged()
        {
            _enabled = CheckForCoordinateSystem();
            string _message;
            if (_enabled)
                //((ESRI.ArcGIS.Desktop.AddIns.Command)this)
                _message = "Generate a Regular Grid";
            else
                _message = "Generate a Regular Grid - The Dataframe must be set to a Projected or Geographic Coordinate System";
        }

        private bool CheckForCoordinateSystem()
        {
            ISpatialReference sr = ArcMap.Document.FocusMap.SpatialReference;
            if (sr == null)
                return false;
            if (sr is IGeographicCoordinateSystem || sr is IProjectedCoordinateSystem)
                return true;
            return false;
        }
    }

}
