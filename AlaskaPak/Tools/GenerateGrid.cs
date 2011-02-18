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
using System.Drawing;
using NPS.AKRO.ArcGIS.Grids;

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
                IEnvelope env = GetExtents();
                if (_form != null) //User may click when form is already loaded.
                {
                    UpdateForm(env);
                    _form.Activate();
                }
                else
                {
                    Grid grid = new Grid(env);
                    _form = new GenerateGridForm();
                    //_form.SelectedLayer += Form_SelectedLayer;
                    _form.FormClosed += Form_Closed;
                    _form.Grid = grid;
                    UpdateForm(env);
                    _form.Show();
                }
            }
            else
            {
                MessageBox.Show("The active data frame must be in a projected coordinate system.",
                    "For this command...", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        #region Event Handlers

        //What we will do when the form says it has closed
        internal void Form_Closed(object sender, FormClosedEventArgs e)
        {
            _form = null;
        }
        #endregion

        private void UpdateForm(IEnvelope env)
        {
            //_form.UpdateExtents(env.XMin, env.YMin, env.XMax, env.YMax);
            _form.Grid.Map = ArcMap.Document.ActiveView.FocusMap;
            _form.Grid.Extents = env;
            _form.Grid.AdjustSize();
            _form.Grid.Draw();
            _form.UpdateFromGrid();
        }

        private IEnvelope GetExtents()
        {
            IScreenDisplay screenDisplay = ((IActiveView)ArcMap.Document.ActiveView.FocusMap).ScreenDisplay;
            IRubberBand rubberEnv = new RubberEnvelope();
            IEnvelope envelope = rubberEnv.TrackNew(screenDisplay, null) as IEnvelope;
            return envelope;
            //if (envelope.IsEmpty)
            //    return;
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
            if (sr is IProjectedCoordinateSystem)
                    return true;
            return false;
        }
    }
}
