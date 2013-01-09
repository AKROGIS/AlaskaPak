namespace NPS.AKRO.ArcGIS.Common
{
    internal struct Tuple<TA, TB>
    {
        //Public properties are needed for datasource
        public TA Item1 { get; set; }
        public TB Item2 { get; set; }
    }
}
