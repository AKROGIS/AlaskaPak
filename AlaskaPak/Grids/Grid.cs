using System;
using ESRI.ArcGIS.Carto;
using ESRI.ArcGIS.Geometry;

namespace NPS.AKRO.ArcGIS.Grids
{
    public class Grid
    {
        public Grid()
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

        public Grid(IEnvelope env)
            : this()
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
        public GridLabelOrder LabelOrder { get; set; }
        public GridLabelStyle RowLabelStyle { get; set; }
        public GridLabelStyle ColumnLabelStyle { get; set; }
        public GridPageNumbering PageNumbering { get; set; }



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


        static Grid From(IFeatureLayer fl)
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
            if (LabelOrder == GridLabelOrder.RowFirst)
                return Prefix + GetLabel(RowCount - 1 - row, RowLabelStyle, RowCount) + Delimiter + GetLabel(column, ColumnLabelStyle, ColumnCount) + Suffix;
            if (LabelOrder == GridLabelOrder.ColumnFirst)
                return Prefix + GetLabel(column, ColumnLabelStyle, ColumnCount) + Delimiter + GetLabel(RowCount - 1 - row, RowLabelStyle, RowCount) + Suffix;
            throw new ArgumentException("LabelOrder");
        }

        private string GetLabel(int index, GridLabelStyle labelStyle, int max)
        {
            switch (labelStyle)
            {
                case GridLabelStyle.LowerCaseAlphabetic:
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
                case GridLabelStyle.UpperCaseAlphabetic:
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
                case GridLabelStyle.NumericWithZeroPadding:
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
                case GridLabelStyle.NumericWithoutZeroPadding:
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

    }
}
