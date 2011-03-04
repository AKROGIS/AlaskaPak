﻿using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;

namespace NPS.AKRO.ArcGIS.Grids
{
    class LinearUnitsConverter
    {
        static LinearUnitsConverter()
        {
            _factors["Millimeters"] = 1.0 / 1000.0;
            _factors["Centimeters"] = 1.0 / 100.0;
            _factors["Decimeters"] = 1.0 / 10.0;
            _factors["Meters"] = 1.0;
            _factors["Kilometers"] = 1000.0;

            _factors["Inches (international)"] = 2.54 * _factors["Centimeters"];
            _factors["Feet (International)"] = 12 * _factors["Inches (international)"] ;
            _factors["Yards (International)"] = 3.0 * _factors["Feet (International)"];
            _factors["Chains (international)"] = 66.0 * _factors["Feet (International)"];
            _factors["Miles (international)"] = 5280.0 * _factors["Feet (International)"];

            _factors["Inches (US Survey)"] = 100.0 / 3937.0;
            _factors["Feet (US Survey)"] = 12 * _factors["Inches (US Survey)"];
            _factors["Yards (US Survey)"] = 3.0 * _factors["Feet (US Survey)"];
            _factors["Chains (US Survey)"] = 66.0 * _factors["Feet (US Survey)"];
            _factors["Miles (US Survey)"] = 5280 * _factors["Feet (US Survey)"];

            _factors["Nautical Miles (US)"] = 6080.2 * _factors["Feet (US Survey)"];
            _factors["Nautical Miles (UK)"] = 6080 * _factors["Feet (International)"];
            _factors["Nautical Miles (international)"] = 1852.0;
        }

        static private Dictionary<string, double> _factors = new Dictionary<string, double>();

        static public IEnumerable<string> KnownUnits
        {
            get { return _factors.Keys; }
        }

        static public double ToMeters(double number, string units)
        {
            return number * _factors[units];
        }
    }
}


