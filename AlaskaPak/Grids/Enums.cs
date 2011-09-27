namespace NPS.AKRO.ArcGIS.Grids
{
    internal enum GridLabelOrder
    {
        RowFirst,
        ColumnFirst,
    }

    internal enum GridLabelStyle
    {
        UpperCaseAlphabetic,
        LowerCaseAlphabetic,
        NumericWithoutZeroPadding,
        NumericWithZeroPadding,
    }

    internal enum GridPageNumbering
    {
        LeftToRightThenTopToBottom,
        LeftToRightThenBottomToTop,
        TopToBottomThenLeftToRight,
        BottomToTopThenLeftToRight,
    }
}
