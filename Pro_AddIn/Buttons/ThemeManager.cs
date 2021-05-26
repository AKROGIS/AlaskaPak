using ArcGIS.Desktop.Framework.Contracts;
using ArcGIS.Desktop.Framework.Dialogs;
using System.Diagnostics;

namespace AlaskaPak.Buttons
{
    internal class ThemeManager : Button
    {
        protected override void OnClick()
        {
            //TODO: protect from file not found, etc
            Process.Start(AlaskaPakModule.ThemeManagerPath);
        }
    }
}
