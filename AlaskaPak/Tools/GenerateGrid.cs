using System;
using System.Collections.Generic;
using System.Text;
using System.IO;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.Display;
using ESRI.ArcGIS.Geometry;
using NPS.AKRO.ArcGIS.Forms;
using NPS.AKRO.ArcGIS.Common;
using System.Windows.Forms;

namespace NPS.AKRO.ArcGIS
{
    public class GenerateGrid : ESRI.ArcGIS.Desktop.AddIns.Tool
    {
        private AlaskaPak _controller;
        private GenerateGridForm _form;

        public GenerateGrid()
        {
            _controller = AlaskaPak.Controller;
            //_controller.LayersChanged += Controller_LayersChanged;
            //_selectableLayers = _controller.GetSelectableLayers();
            Enabled = CheckForCoordinateSystem();
        }

        protected override void OnMouseDown(MouseEventArgs arg)
        {
            if (Enabled)
            {
                GetExtents();
                if (_form != null) //User may click when form is already loaded.
                {
                    _form.Activate();
                    //UpdateForm();
                }
                else
                {
                    _form = new GenerateGridForm();
                    //_form.SelectedLayer += Form_SelectedLayer;
                    //_form.FormClosed += Form_Closed;
                    //UpdateForm();
                    _form.Show();
                }
            }
            else
            {
                MessageBox.Show("You must have one or more selectable feature layers in your map to use this command.",
                    "For this command...", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private void GetExtents()
        {
            IScreenDisplay screenDisplay = ((IActiveView)ArcMap.Document.ActiveView.FocusMap).ScreenDisplay;
            IRubberBand rubberEnv = new RubberEnvelope();
            IEnvelope envelope = rubberEnv.TrackNew(screenDisplay, null) as IEnvelope;
            if (envelope.IsEmpty)
                return;
        }

        void MapEvents_ContentsChanged()
        {
            Enabled = CheckForCoordinateSystem();
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
