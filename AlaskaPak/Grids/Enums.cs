using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace NPS.AKRO.ArcGIS.Grids
{
    public enum GridLabelOrder
    {
        RowFirst,
        ColumnFirst,
    }

    public enum GridLabelStyle
    {
        UpperCaseAlphabetic,
        LowerCaseAlphabetic,
        NumericWithoutZeroPadding,
        NumericWithZeroPadding,
    }

    public enum GridPageNumbering
    {
        LeftToRightThenTopToBottom,
        LeftToRightThenBottomToTop,
        TopToBottomThenLeftToRight,
        BottomToTopThenLeftToRight,
    }
}
