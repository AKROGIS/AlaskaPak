using ArcGIS.Desktop.Framework.Contracts;
using System.Diagnostics;

namespace AlaskaPak.Buttons
{
    internal class WebSite : Button
    {
        protected override void OnClick()
        {
            Process.Start("https://inpakrovmweb.nps.doi.net/rgr/akgis/");
        }
    }
}
