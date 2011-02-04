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
                    _form.Activate();
                    UpdateForm(env);
                }
                else
                {
                    _form = new GenerateGridForm();
                    //_form.SelectedLayer += Form_SelectedLayer;
                    _form.FormClosed += Form_Closed;
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
            _form.UpdateExtents(env.XMin, env.YMin, env.XMax, env.YMax);
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
            //if (sr is IGeographicCoordinateSystem || sr is IProjectedCoordinateSystem)
            if (sr is IProjectedCoordinateSystem)
                    return true;
            return false;
        }
    }

    enum HowToFix
    {
        AdjustExtents,
        AdjustSize,
        AdjustCountThenAdjustExtents,
        AdjustCountThenAdjustSize
    }

    class IndexGrid
    {
        public IndexGrid()
        {
            CellSize = new SizeF(1000f, 1000f);
            CellCount = new Size(10,10);
            Extents = new RectangleF(0f,0f,10000f,10000f);
        }

        static IndexGrid From(IFeatureLayer fl)
        {
            throw new NotImplementedException();
        }

        public void SaveAs(ESRI.ArcGIS.Geodatabase.IFeatureClass fc)
        {
            throw new NotImplementedException();
        }

        public void Save()
        {
            throw new NotImplementedException();
        }

        //row name style
        //column name style
        //feature class (for existing)
        //spatial reference (for new)
        //need spatial ref of display
        //need draw method

        public RectangleF Extents { get; set; }

        public Size CellCount { get; set; }

        public SizeF CellSize { get; set; }

        public Size CalcCount()
        {
            int x = (int)(Extents.Width / CellSize.Width);
            int y = (int)(Extents.Height / CellSize.Height);
            return new Size(x, y);
        }

        public SizeF CalcSize()
        {
            float w = Extents.Width / CellCount.Width;
            float h = Extents.Height / CellCount.Height;
            return new SizeF(w, h);
        }

        public RectangleF CalcExtents()
        {
            float widthDiff = (CellSize.Width * CellCount.Width) - Extents.Width;
            float heightDiff = CellSize.Height * CellCount.Height;
            return RectangleF.Inflate(Extents, widthDiff, heightDiff);
        }

        public bool isValid
        {
            get
            {
                if (CellCount.Width < 1 || CellCount.Height < 1)
                    return false;
                if (CellSize.Width < 0 || CellSize.Height < 0)
                    return false;
                if (Extents.IsEmpty)
                    return false;
                if (CellCount.Width * CellSize.Width == Extents.Size.Width ||
                    CellCount.Height * CellSize.Height == Extents.Size.Height)
                    return true;
                else
                    return false;
            }
        }

        void AdjustSize()
        {
            CellSize = CalcSize();
        }

        void AdjustExtents()
        {
            Extents = CalcExtents();
        }

        void AdjustCountThenSize()
        {
            CellCount = CalcCount();
            CellSize = CalcSize();
        }

        void AdjustCountThenExtents()
        {
            CellCount = CalcCount();
            Extents = CalcExtents();
        }

    }

}
