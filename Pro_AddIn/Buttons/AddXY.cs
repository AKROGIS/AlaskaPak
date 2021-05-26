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
    internal class AddXY : Button
    {

        private AddXYWindow _addxywindow = null;

        protected override void OnClick()
        {
            //already open?
            if (_addxywindow != null)
                return;
            _addxywindow = new AddXYWindow
            {
                Owner = FrameworkApplication.Current.MainWindow
            };
            _addxywindow.Closed += (o, e) => { _addxywindow = null; };
            _addxywindow.Show();
            //uncomment for modal
            //_addxywindows.ShowDialog();
        }

    }
}
