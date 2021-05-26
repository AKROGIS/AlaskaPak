using System;
using System.Globalization;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.Geometry;
using System.Collections.Generic;

namespace NPS.AKRO.ArcGIS.Grids
{
    internal class Grid
    {
        //row name style
        //column name style
        //feature class (for existing)
        //spatial reference (for new)
        //need spatial ref of display
        //need draw method

        //If map's spatial reference changes, then we need to reproject extents, and scale sizes, then redraw

        internal Grid()
        {
            RowCount = 10;
            ColumnCount = 10;
            RowHeight = 1000;
            ColumnWidth = 1000;
            Suffix = "";
            Prefix = "";
            Delimiter = "-";
            LabelOrder = GridLabelOrder.RowFirst;
            RowLabelStyle = GridLabelStyle.UpperCaseAlphabetic;
            ColumnLabelStyle = GridLabelStyle.NumericWithZeroPadding;
            PageNumbering = GridPageNumbering.LeftToRightThenTopToBottom;
        }

        internal Grid(IEnvelope env)
            : this()
        {
            Extents = env;
            AdjustSize();
            ColumnWidth = Math.Round(ColumnWidth / 10.0) * 10;
            RowHeight = Math.Round(RowHeight / 10.0) * 10;
            AdjustExtents();
        }

        /// <summary>
        /// Extents (envelope) of the grid in map display units
        /// </summary>
        internal IEnvelope Extents { get; set; }

        /// <summary>
        /// Total number of rows in grid. Rows are indexed in the direction of the Y-axis, starting with zero.
        /// </summary>
        internal int RowCount { get; set; }

        /// <summary>
        /// Total number of columns in grid. Columns are indexed in the direction of the X-axis, starting with zero.
        /// </summary>
        internal int ColumnCount { get; set; }

        /// <summary>
        /// Height of each cell and each rows in map display units
        /// </summary>
        internal double RowHeight { get; set; }

        /// <summary>
        /// Width of each cells and each columns in map display units
        /// </summary>
        internal double ColumnWidth { get; set; }

        internal double MetersPerUnit
        {
            get
            {
                //ConversionFactor and MeterPerUnit are synonyms.
                return ((IProjectedCoordinateSystem)Map.SpatialReference).CoordinateUnit.ConversionFactor;
            }
        }

        internal string Prefix { get; set; }
        internal string Suffix { get; set; }
        internal string Delimiter { get; set; }
        internal GridLabelOrder LabelOrder { get; set; }
        internal GridLabelStyle RowLabelStyle { get; set; }
        internal GridLabelStyle ColumnLabelStyle { get; set; }
        internal GridPageNumbering PageNumbering { get; set; }

        internal IMap Map
        {
            get { return _map; }
            set
            {
                if (_map == value)
                    return;
                if (_map != null)
                    ((IGraphicsContainer)_map).DeleteElement(_group as IElement);
                _map = value;
                ((IGraphicsContainer)_map).AddElement(_group as IElement, 0);
            }
        }

        private IMap _map;


        //static Grid From(IFeatureLayer fl)
        //{
        //    throw new NotImplementedException();
        //}

        internal void SaveAs(ESRI.ArcGIS.Geodatabase.IFeatureClass fc)
        {
            throw new NotImplementedException();
        }

        internal void Save()
        {
            throw new NotImplementedException();
        }


        internal bool IsValid
        {
            get
            {
                if (ColumnCount < 1 || RowCount < 1)
                    return false;
                if (ColumnWidth < 0 || RowHeight < 0)
                    return false;
                if (Extents.IsEmpty)
                    return false;
                return Math.Abs(ColumnCount * ColumnWidth - Extents.Width) < EPSILON &&
                       Math.Abs(RowCount * RowHeight - Extents.Height) < EPSILON;
            }
        }

        internal void AdjustSize()
        {
            ColumnWidth = Extents.Width / ColumnCount;
            RowHeight = Extents.Height / RowCount;
        }

        internal void AdjustExtents()
        {
            if (Extents == null)
                return;
            double widthDiff = ((ColumnWidth * ColumnCount) - Extents.Width) / 2.0;
            double heightDiff = ((RowHeight * RowCount) - Extents.Height) / 2.0;
            Extents.Expand(widthDiff, heightDiff, false);
        }

        internal void AdjustCountThenSize()
        {
            AdjustCount();
            AdjustSize();
        }

        internal void AdjustCountThenExtents()
        {
            AdjustCount();
            AdjustExtents();
        }

        private void AdjustCount()
        {
            ColumnCount = (int)(Extents.Width / ColumnWidth);
            RowCount = (int)(Extents.Height / RowHeight);
        }

        private string GetRowLabel(int row)
        {
            switch (PageNumbering)
            {
                case GridPageNumbering.LeftToRightThenTopToBottom:
                case GridPageNumbering.TopToBottomThenLeftToRight:
                    return GetLabel(RowCount - 1 - row, RowLabelStyle, RowCount);
                case GridPageNumbering.LeftToRightThenBottomToTop:
                case GridPageNumbering.BottomToTopThenLeftToRight:
                    return GetLabel(row, RowLabelStyle, RowCount);
                default:
                    throw new ArgumentException("GridPageNumbering");
            }
        }

        private string GetColumnLabel(int column)
        {
            return GetLabel(column, ColumnLabelStyle, ColumnCount);
        }

        private string GetLabel(int row, int column)
        {
            if (LabelOrder == GridLabelOrder.RowFirst)
                return Prefix + GetRowLabel(row) + Delimiter + GetColumnLabel(column) + Suffix;
            if (LabelOrder == GridLabelOrder.ColumnFirst)
                return Prefix + GetColumnLabel(column) + Delimiter + GetRowLabel(row) + Suffix;
            throw new ArgumentException("LabelOrder");
        }

        private static string GetLabel(int index, GridLabelStyle labelStyle, int max)
        {
            switch (labelStyle)
            {
                case GridLabelStyle.LowerCaseAlphabetic:
                    //Express in base 26: a..z,aa..az,ba..bz...  bc = 2*26 + 2
                    //Assume less than 26^3 (17576) cells
                    if (index < 26)
                        return string.Format("{0}", Convert.ToChar(97 + index));
                    if (index < 26 * 26)
                        return string.Format("{0}{1}", Convert.ToChar(97 + (index / 26)), Convert.ToChar(97 + (index % 26)));
                    if (index < 26 * 26 * 26)
                    {
                        const int basis = 26 * 26;
                        return string.Format("{0}{1}{2}", Convert.ToChar(97 + (index / basis)),
                                             Convert.ToChar(97 + ((index % basis) / 26)), Convert.ToChar(97 + (index % 26)));
                    }
                    return "OutOfBounds";
                case GridLabelStyle.UpperCaseAlphabetic:
                    //Express in base 26: A..Z,AA..AZ,BA..BZ...  BC = 2*26 + 2
                    //Assume less than 26^3 (17576) cells
                    if (index < 26)
                        return string.Format("{0}", Convert.ToChar(65 + index));
                    if (index < 26 * 26)
                        return string.Format("{0}{1}", Convert.ToChar(65 + (index / 26)), Convert.ToChar(65 + (index % 26)));
                    if (index < 26 * 26 * 26)
                    {
                        const int basis = 26 * 26;
                        return string.Format("{0}{1}{2}", Convert.ToChar(65 + (index / basis)),
                                             Convert.ToChar(65 + ((index % basis) / 26)), Convert.ToChar(65 + (index % 26)));
                    }
                    return "OutOfBounds";
                case GridLabelStyle.NumericWithZeroPadding:
                    // assume less than 10000
                    if (max < 10)
                        return (index + 1).ToString("D1");
                    if (max < 100)
                        return (index + 1).ToString("D2");
                    if (max < 1000)
                        return (index + 1).ToString("D3");
                    if (max < 10000)
                        return (index + 1).ToString("D4");
                    return "OutOfBounds";
                case GridLabelStyle.NumericWithoutZeroPadding:
                    return (index + 1).ToString(CultureInfo.InvariantCulture);
                default:
                    throw new ArgumentException("labelStyle");
            }
        }

        internal void Erase()
        {
            if (_group == null)
                return;
            if (Map == null)
                return;
            var view = Map as IActiveView;
            if (view == null)
                return;
            var container = Map as IGraphicsContainer;
            if (container == null)
                return;
            if (_group.ElementCount != 0)
            {
                _group.ClearElements();
                container.UpdateElement(_group as IElement);
                view.ScreenDisplay.FinishDrawing();
                view.Refresh();
            }
            container.DeleteElement(_group as IElement);
            System.Runtime.InteropServices.Marshal.ReleaseComObject(_group);
            //_group = null;
        }

        internal void Draw()
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

        private readonly IGroupElement3 _group = new GroupElementClass();
        private const double EPSILON = 1e-14;

        private static void DrawLabel(IGroupElement3 group, string label, IPoint point)
        {
            var text = new TextElementClass
            {
                AnchorPoint = esriAnchorPointEnum.esriCenterPoint,
                Text = label,
                Geometry = point
            };
            group.AddElement(text);
        }

        private static void DrawLine(IGroupElement3 group, IPolyline line)
        {
            //LineGraphics (LineElementClass) will only accept IPolyline (not ILine)
            var element = new LineElementClass { Geometry = line };
            group.AddElement(element);
        }

        internal IEnumerable<Cell> Cells
        {
            get
            {
                for (int row = 0; row < RowCount; row++)
                    for (int column = 0; column < ColumnCount; column++)
                        yield return GetCell(row, column);
            }
        }

        internal Cell GetCell(int row, int column)
        {
            return new Cell
            {
                Row = row,
                Column = column,
                Page = GetCellNumber(row, column),
                ColumnLabel = GetColumnLabel(column),
                RowLabel = GetRowLabel(row),
                Label = GetLabel(row, column),
                Shape = GetGeometry(row, column),
            };
        }

        private int GetCellNumber(int row, int column)
        {
            switch (PageNumbering)
            {
                case GridPageNumbering.LeftToRightThenTopToBottom:
                    return (RowCount - row - 1) * RowCount + column + 1;
                case GridPageNumbering.LeftToRightThenBottomToTop:
                    return row * RowCount + column + 1;
                case GridPageNumbering.TopToBottomThenLeftToRight:
                    return column * ColumnCount + (RowCount - row - 1) + 1;
                case GridPageNumbering.BottomToTopThenLeftToRight:
                    return column * ColumnCount + row + 1;
                default:
                    throw new ArgumentException("GridPageNumbering");
            }
        }

        private IGeometry GetGeometry(int row, int column)
        {
            IPointCollection polygon = new Polygon();

            //Clockwise for filled, Counter-clockwise for holes
            polygon.AddPoint(LowerLeftPoint(row, column));
            polygon.AddPoint(UpperLeftPoint(row, column));
            polygon.AddPoint(UpperRightPoint(row, column));
            polygon.AddPoint(LowerRightPoint(row, column));
            polygon.AddPoint(LowerLeftPoint(row, column));

            //coordinates are defined in the map display 
            ((IGeometry)polygon).SpatialReference = Map.SpatialReference;

            return (IGeometry)polygon;
        }

        private IPoint LowerLeftPoint(int row, int column)
        {
            IPoint point = new Point();
            double x = Extents.XMin + column * ColumnWidth;
            double y = Extents.YMin + row * RowHeight;
            point.PutCoords(x, y);
            return point;
        }

        private IPoint LowerRightPoint(int row, int column)
        {
            IPoint point = LowerLeftPoint(row, column);
            point.X = point.X + ColumnWidth;
            return point;
        }

        private IPoint UpperRightPoint(int row, int column)
        {
            IPoint point = LowerRightPoint(row, column);
            point.Y = point.Y + RowHeight;
            return point;
        }

        private IPoint UpperLeftPoint(int row, int column)
        {
            IPoint point = LowerLeftPoint(row, column);
            point.Y = point.Y + RowHeight;
            return point;
        }
    }

    internal class Cell
    {
        internal int Row { get; set; }
        internal int Column { get; set; }
        internal int Page { get; set; }
        internal string ColumnLabel { get; set; }
        internal string RowLabel { get; set; }
        internal string Label { get; set; }
        internal IGeometry Shape { get; set; }
    }
}
