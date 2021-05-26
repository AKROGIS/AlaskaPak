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
    internal class AboutAlaskaPak : Button
    {

        private AboutAlaskaPakWindow _aboutalaskapakwindow = null;

        protected override void OnClick()
        {
            //already open?
            if (_aboutalaskapakwindow != null)
                return;
            _aboutalaskapakwindow = new AboutAlaskaPakWindow
            {
                Owner = FrameworkApplication.Current.MainWindow
            };
            _aboutalaskapakwindow.Closed += (o, e) => { _aboutalaskapakwindow = null; };
            _aboutalaskapakwindow.Show();
            //uncomment for modal
            //_aboutalaskapakwindow.ShowDialog();
        }

    }
}
