﻿namespace NPS.AKRO.ArcGIS.Buttons
{
    public class AddLength : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private static void MyClick()
        {
            Common.ArcToolBox.Invoke(Common.Settings.Get("PathToToolbox"), "AddLength");
        }
    }
}
