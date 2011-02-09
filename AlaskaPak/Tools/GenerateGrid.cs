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
                    UpdateForm(env);
                    _form.Activate();
                }
                else
                {
                    IndexGrid grid = new IndexGrid(env);
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

    public enum IndexGridLabelOrder
    {
        RowFirst,
        ColumnFirst,
    }
    public enum IndexGridLabelStyle
    {
        UpperCaseAlphabetic,
        LowerCaseAlphabetic,
        NumericWithoutZeroPadding,
        NumericWithZeroPadding,
    }

    public enum IndexGridPageNumbering
    {
        LeftToRightThenTopToBottom,
        LeftToRightThenBottomToTop,
        TopToBottomThenLeftToRight,
        BottomToTopThenLeftToRight,
    }

    public class IndexGrid
    {
        public IndexGrid()
        {
            RowCount = 18;
            ColumnCount = 22;
            RowHeight = 1000;
            ColumnWidth = 1000;
            Suffix = "";
            Prefix = "";
            Delimiter = "-";
            LabelOrder = IndexGridLabelOrder.RowFirst;
            RowLabelStyle = IndexGridLabelStyle.UpperCaseAlphabetic;
            ColumnLabelStyle = IndexGridLabelStyle.NumericWithZeroPadding;
            PageNumbering = IndexGridPageNumbering.LeftToRightThenTopToBottom;
        }

        public IndexGrid(IEnvelope env):this()
        {
            Extents = env;
            AdjustSize();
        }

        public IEnvelope Extents { get; set; }

        public int RowCount { get; set; }
        public int ColumnCount { get; set; }
        public double RowHeight { get; set; }
        public double ColumnWidth { get; set; }
        public string Prefix { get; set; }
        public string Suffix { get; set; }
        public string Delimiter { get; set; }
        public IndexGridLabelOrder LabelOrder { get; set; }
        public IndexGridLabelStyle RowLabelStyle { get; set; }
        public IndexGridLabelStyle ColumnLabelStyle { get; set; }
        public IndexGridPageNumbering PageNumbering { get; set; }



        //row name style
        //column name style
        //feature class (for existing)
        //spatial reference (for new)
        //need spatial ref of display
        //need draw method


        public IMap Map
        {
            get
            {
                return _map;
            }
            set
            {
                if (_map != value)
                {
                    if (_map != null)
                        ((IGraphicsContainer)_map).DeleteElement(_group as IElement);
                    _map = value;
                    ((IGraphicsContainer)_map).AddElement(_group as IElement, 0);
                }
            }
        }
        private IMap _map;


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



        public bool isValid
        {
            get
            {
                if (ColumnCount < 1 || RowCount < 1)
                    return false;
                if (ColumnWidth < 0 || RowHeight < 0)
                    return false;
                if (Extents.IsEmpty)
                    return false;
                if (ColumnCount * ColumnWidth == Extents.Width ||
                    RowCount * RowHeight == Extents.Height)
                    return true;
                else
                    return false;
            }
        }

        public void AdjustSize()
        {
            ColumnWidth = Extents.Width / ColumnCount;
            RowHeight = Extents.Height / RowCount;
        }

        public void AdjustExtents()
        {
            if (Extents == null)
                return;
            double widthDiff = ((ColumnWidth * ColumnCount) - Extents.Width) / 2.0;
            double heightDiff = ((RowHeight * RowCount) - Extents.Height) / 2.0;
            Extents.Expand(widthDiff, heightDiff, false);
        }

        public void AdjustCountThenSize()
        {
            AdjustCount();
            AdjustSize();
        }

        public void AdjustCountThenExtents()
        {
            AdjustCount();
            AdjustExtents();
        }

        private void AdjustCount()
        {
            ColumnCount = (int)(Extents.Width / ColumnWidth);
            RowCount = (int)(Extents.Height / RowHeight);
        }

        public string GetLabel(int row, int column)
        {
            if (LabelOrder == IndexGridLabelOrder.RowFirst)
                return Prefix + GetLabel(RowCount - 1 - row, RowLabelStyle, RowCount) + Delimiter + GetLabel(column, ColumnLabelStyle, ColumnCount) + Suffix;
            if (LabelOrder == IndexGridLabelOrder.ColumnFirst)
                return Prefix + GetLabel(column, ColumnLabelStyle, ColumnCount) + Delimiter + GetLabel(RowCount - 1 - row, RowLabelStyle, RowCount) + Suffix;
            throw new ArgumentException("LabelOrder");
        }

        private string GetLabel(int index, IndexGridLabelStyle labelStyle, int max)
        {
            switch (labelStyle)
            {
                case IndexGridLabelStyle.LowerCaseAlphabetic:
                    //Express in base 26: a..z,aa..az,ba..bz...  bc = 2*26 + 2
                    //Assume less than 26^2 (676) cells
                    if (index < 26)
                        return string.Format("{0}", Convert.ToChar(97 + index));
                    if (index < 26 * 26)
                        return string.Format("{0}{1}", Convert.ToChar(97 + (index / 26)), Convert.ToChar(97 + (index % 26)));
                    if (index < 26 * 26 * 26)
                    {
                        int basis = 26 * 26;
                        return string.Format("{0}{1}{2}", Convert.ToChar(97 + (index / basis)), Convert.ToChar(97 + ((index % basis) / 26)), Convert.ToChar(97 + (index % 26)));
                    }
                    return "OutOfBounds";
                case IndexGridLabelStyle.UpperCaseAlphabetic:
                    //Express in base 26: A..Z,AA..AZ,BA..BZ...  BC = 2*26 + 2
                    //Assume less than 26^2 (676) cells
                    if (index < 26)
                        return string.Format("{0}", Convert.ToChar(65 + index));
                    if (index < 26 * 26)
                        return string.Format("{0}{1}", Convert.ToChar(65 + (index / 26)), Convert.ToChar(65 + (index % 26)));
                    if (index < 26 * 26 * 26)
                    {
                        int basis = 26 * 26;
                        return string.Format("{0}{1}{2}", Convert.ToChar(65 + (index / basis)), Convert.ToChar(65 + ((index % basis) / 26)), Convert.ToChar(65 + (index % 26)));
                    }
                    return "OutOfBounds";
                case IndexGridLabelStyle.NumericWithZeroPadding:
                    //FIXME Column or Row - How do I know
                    if (max < 10)
                        return (index + 1).ToString("D1");
                    if (max < 100)
                        return (index + 1).ToString("D2");
                    if (max < 1000)
                        return (index + 1).ToString("D3");
                    if (max < 10000)
                        return (index + 1).ToString("D4");
                    return "OutOfBounds";
                case IndexGridLabelStyle.NumericWithoutZeroPadding:
                    return (index + 1).ToString();
                default:
                    throw new ArgumentException("labelStyle");
            }
        }

        public void Draw()
        {
            if (Map == null)
                return;
            var view = Map as IActiveView;
            if (view == null)
                return;
            var container = Map as IGraphicsContainer;
            if (container == null)
                return;

            IPoint point1 = new PointClass();
            IPoint point2 = new PointClass();
            IPolyline line = new PolylineClass();
            //erase all elements in the group.
            _group.ClearElements();

            //add vertical lines to the group
            point1.Y = Extents.YMin;
            point2.Y = Extents.YMax;
            for (int i = 0; i <= ColumnCount; i++)
            {
                point1.X = Extents.XMin + ColumnWidth * i;
                point2.X = point1.X;
                line.SetEmpty();
                ((IPointCollection)line).AddPoint(point1);
                ((IPointCollection)line).AddPoint(point2);
                DrawLine(_group, line);
            }

            //add horizontal lines to the group
            point1.X = Extents.XMin;
            point2.X = Extents.XMax;
            for (int j = 0; j <= RowCount; j++)
            {
                point1.Y = Extents.YMin + RowHeight * j;
                point2.Y = point1.Y;
                line.SetEmpty();
                ((IPointCollection)line).AddPoint(point1);
                ((IPointCollection)line).AddPoint(point2);
                DrawLine(_group, line);
            }

            //Add labels to the group
            for (int row = 0; row < RowCount; row++)
            {
                for (int column = 0; column < ColumnCount; column++)
                {
                    point1.X = Extents.XMin + ColumnWidth * (column + 0.5f);
                    point1.Y = Extents.YMin + RowHeight * (row + 0.5f);
                    string label = GetLabel(row, column);
                    DrawLabel(_group, label, point1);
                }
            }
            //refresh the display
            container.UpdateElement(_group as IElement);
            view.ScreenDisplay.FinishDrawing();
            view.Refresh();
        }
        private IGroupElement3 _group = new GroupElementClass();

        private void DrawLabel(IGroupElement3 group, string label, IPoint point)
        {
            var text = new TextElementClass();
            text.AnchorPoint = esriAnchorPointEnum.esriCenterPoint;
            text.Text = label;
            text.Geometry = point as IGeometry;
            group.AddElement(text);
        }

        private void DrawLine(IGroupElement3 group, IPolyline line)
        {
            //LineGraphics (LineElementClass) will only accept IPolyline (not ILine)
            var element = new LineElementClass();
            element.Geometry = line;
            group.AddElement(element);
        }
        // as ESRI.ArcGIS.Carto.IElement;
        //IGeometry geom = line as IGeometry;
        //((IElement)element).Geometry = geom; // line as IGeometry;

    }

}
