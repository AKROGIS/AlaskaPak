using System;
using System.Collections.Generic;
using ESRI.ArcGIS.esriSystem;

namespace NPS.AKRO.ArcGIS.Grids
{
    internal class LinearUnitsConverter
    {
        static LinearUnitsConverter()
        {
            Factors["Millimeters"] = 1.0 / 1000.0;
            Factors["Centimeters"] = 1.0 / 100.0;
            Factors["Decimeters"] = 1.0 / 10.0;
            Factors["Meters"] = 1.0;
            Factors["Kilometers"] = 1000.0;

            Factors["Inches (International)"] = 2.54 * Factors["Centimeters"];
            Factors["Feet (International)"] = 12 * Factors["Inches (International)"];
            Factors["Yards (International)"] = 3.0 * Factors["Feet (International)"];
            Factors["Chains (International)"] = 66.0 * Factors["Feet (International)"];
            Factors["Miles (International)"] = 5280.0 * Factors["Feet (International)"];

            Factors["Inches (US Survey)"] = 100.0 / 3937.0;
            Factors["Feet (US Survey)"] = 12 * Factors["Inches (US Survey)"];
            Factors["Yards (US Survey)"] = 3.0 * Factors["Feet (US Survey)"];
            Factors["Chains (US Survey)"] = 66.0 * Factors["Feet (US Survey)"];
            Factors["Miles (US Survey)"] = 5280 * Factors["Feet (US Survey)"];

            Factors["Nautical Miles (US)"] = 6080.2 * Factors["Feet (US Survey)"];
            Factors["Nautical Miles (UK)"] = 6080 * Factors["Feet (International)"];
            Factors["Nautical Miles (International)"] = 1852.0;
        }

        private static readonly Dictionary<string, double> Factors = new Dictionary<string, double>();

        internal static IEnumerable<string> KnownUnits
        {
            get { return Factors.Keys; }
        }

        internal static double ToMeters(double number, string units)
        {
            return number * Factors[units];
        }

        internal static string Key(esriUnits units)
        {
            switch (units)
            {
                case esriUnits.esriCentimeters:
                    return "Centimeters";
                case esriUnits.esriDecimalDegrees:
                    throw new InvalidOperationException("DecimalDegrees");
                case esriUnits.esriDecimeters:
                    return "Decimeters";
                case esriUnits.esriFeet:
                    return "Feet (US Survey)";
                case esriUnits.esriInches:
                    return "Inches (US Survey)";
                case esriUnits.esriKilometers:
                    return "Kilometers";
                case esriUnits.esriMeters:
                    return "Meters";
                case esriUnits.esriMiles:
                    return "Miles (US Survey)";
                case esriUnits.esriMillimeters:
                    return "Millimeters";
                case esriUnits.esriNauticalMiles:
                    return "Nautical Miles (US)";
                case esriUnits.esriPoints:
                    throw new InvalidOperationException("Pointss");
                case esriUnits.esriUnitsLast:
                    throw new InvalidOperationException("Last Units");
                case esriUnits.esriUnknownUnits:
                    return "Meters";
                case esriUnits.esriYards:
                    return "Yards (US Survey)";
                default:
                    return "Meters";
            }
        }
    }
}
