using System;
using System.Collections.Generic;

namespace NPS.AKRO.ArcGIS.Coordinates
{
    class Formatter
    {
        public Formatter() :
            this(FormatterOutputFormat.DegreesMinutesSeconds, 2, true, true, true)
        { }

        public Formatter(FormatterOutputFormat outputFormat, int decimals, bool showDirection, bool showZeroParts, bool showSpaces)
        {
            OutputFormat = outputFormat;
            Decimals = decimals;
            ShowDirection = showDirection;
            ShowZeroParts = showZeroParts;
            ShowSpaces = showSpaces;
        }


        // be sure to sync changes here with the AddXYOutputFormat enum.
        public IEnumerable<string> Names
        {
            get
            {
                return new string[] {
                    "Data Source Coordinates",
                    "Data Frame Coordinates",
                    "Decimal Degrees (formated)",
                    "Degrees Decimal Minutes (formated)",
                    "Degrees Minutes Seconds (formated)",
                };
            }
        }

        /// <param name="ShowDirection">if true, then alphabetic direction (N-S-E-W) is appended, if false, sign (-) is used for direction</param>
        public bool ShowDirection { get; set; }
        /// <param name="ShowZeroParts">if true, then zero minutes and zero seconds are shown, if false, they are hidden</param>
        public bool ShowZeroParts { get; set; }
        /// <param name="ShowSpaces">if true, then spaces are added between parts, if false all spaces are removed</param>
        public bool ShowSpaces { get; set; }
        /// <param name="outputFormat">The format of the result</param>
        public FormatterOutputFormat OutputFormat { get; set; }
        /// <param name="decimals">Number of decimals to use in the last number</param>
        public int Decimals
        {
            get { return _decimals; }
            set
            {
                if (value != _decimals)
                {
                    if (value < 0 || value > 9)
                        throw new ArgumentOutOfRangeException("decimals", "decimal precision must be within (0..9)");
                    _decimals = value;
                }
            }
        }
        private int _decimals;

        public int DefaultDecimals
        {
            get
            {
                switch (OutputFormat)
                {
                    default:
                    case FormatterOutputFormat.DataSource:
                    case FormatterOutputFormat.DataFrame:
                        return 6;
                    case FormatterOutputFormat.DecimalDegress:
                        return 6;
                    case FormatterOutputFormat.DegreesDecimalMinutes:
                        return 4;
                    case FormatterOutputFormat.DegreesMinutesSeconds:
                        return 2;
                }
            }
        }

        public bool Formattable
        {
            get
            {
                return OutputFormat == FormatterOutputFormat.DecimalDegress ||
                    OutputFormat == FormatterOutputFormat.DegreesDecimalMinutes ||
                    OutputFormat == FormatterOutputFormat.DegreesMinutesSeconds;
            }
        }

        /// <summary>
        /// Formats a decimal degree number
        /// </summary>
        /// <remarks>
        /// If the seconds or minutes rounds up to 60, it does not increment the preceeding unit.
        /// This is a function of the user not choosing a display precision that captures the
        /// precision in the input value.  This should be corrected, but in order to do it, the input
        /// decimal degrees would need to be rounded appropriately before the components are
        /// extracted.
        /// Similarly, a number may round to zero and then not disappear when showZeroParts is false
        /// because it is not really zero, it is only the precision that makes it appear as zero.
        /// </remarks>
        /// <param name="decimalDegrees">The real number value for the degrees to format</param>
        /// <param name="isLatitude">true if this is latitude, false if this is longitude</param>
        /// <returns>The formatted string</returns>
        public string Format(double decimalDegrees, bool isLatitude)
        {
            if (isLatitude && (decimalDegrees < -90 || decimalDegrees > 90))
                throw new ArgumentOutOfRangeException("decimalDegrees", "Latitude must be within (-90..90)");
            if (!isLatitude && (decimalDegrees < -360 || decimalDegrees > 360))
                throw new ArgumentOutOfRangeException("decimalDegrees", "Longititude must be within (-360..360)");

            //normalize the longitude within -180..180
            if (decimalDegrees < -180)
                decimalDegrees = decimalDegrees + 360;
            if (decimalDegrees > 180)
                decimalDegrees = decimalDegrees - 360;

            //set sign and direction
            string sign = "-";
            if (ShowDirection || 0 < decimalDegrees)
                sign = "";
            string direction = "";
            if (ShowDirection)
                if (isLatitude)
                    direction = decimalDegrees < 0 ? "S" : "N";
                else
                    direction = decimalDegrees < 0 ? "W" : "E";

            //get components
            decimalDegrees = Math.Abs(decimalDegrees);
            int degrees = (int)decimalDegrees;
            double decimalMinutes = (decimalDegrees - degrees) * 60.0;
            int minutes = (int)(decimalMinutes);
            double seconds = (decimalDegrees - (degrees + minutes / 60.0)) * 3600.0;

            // create format string
            string decimalFormat = "F" + Decimals.ToString();
            string format;
            object[] args;
            switch (OutputFormat)
            {
                case FormatterOutputFormat.DecimalDegress:
                    format = "{0}{1:" + decimalFormat + "}° {2}";
                    args = new object[] { sign, decimalDegrees, direction };
                    break;
                case FormatterOutputFormat.DegreesDecimalMinutes:
                    format = "{0}{1}° ";
                    if (ShowZeroParts || decimalMinutes != 0.0)
                        format = format + "{2:" + decimalFormat + "}' ";
                    format = format + "{3}";
                    args = new object[] { sign, degrees, decimalMinutes, direction };
                    break;
                case FormatterOutputFormat.DegreesMinutesSeconds:
                    format = "{0}{1}° ";
                    if (ShowZeroParts || minutes != 0)
                        format = format + "{2}' ";
                    if (ShowZeroParts || seconds != 0.0)
                        format = format + "{3:" + decimalFormat + "}\" ";
                    format = format + "{4}";
                    args = new object[] { sign, degrees, minutes, seconds, direction };
                    break;
                default:
                    throw new ArgumentOutOfRangeException("outputFormat", "Invalid output format requested");
            }

            //remove spaces
            if (!ShowSpaces)
                format = format.Replace(" ", "");

            return string.Format(format, args);
        }
    }
}
