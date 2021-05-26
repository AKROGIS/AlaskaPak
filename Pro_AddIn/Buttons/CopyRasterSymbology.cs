using ArcGIS.Core.CIM;
using ArcGIS.Core.Data;
using ArcGIS.Core.Geometry;
using ArcGIS.Desktop.Catalog;
using ArcGIS.Desktop.Core;
using ArcGIS.Desktop.Editing;
using ArcGIS.Desktop.Extensions;
using ArcGIS.Desktop.Framework;
using ArcGIS.Desktop.Framework.Contracts;
using ArcGIS.Desktop.Framework.Dialogs;
using ArcGIS.Desktop.Framework.Threading.Tasks;
using ArcGIS.Desktop.Layouts;
using ArcGIS.Desktop.Mapping;
using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using AlaskaPak.UI;

namespace AlaskaPak.Buttons

{
    internal class CopyRasterSymbology : Button
    {

        private CopyRasterSymbologyWindow _copyrastersymbologywindow = null;

        protected override void OnClick()
        {
            //already open?
            if (_copyrastersymbologywindow != null)
                return;
            _copyrastersymbologywindow = new CopyRasterSymbologyWindow
            {
                Owner = FrameworkApplication.Current.MainWindow
            };
            _copyrastersymbologywindow.Closed += (o, e) => { _copyrastersymbologywindow = null; };
            _copyrastersymbologywindow.Show();
            //uncomment for modal
            //_copyrastersymbologywindow.ShowDialog();
        }

    }
}
