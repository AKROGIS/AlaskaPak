﻿namespace NPS.AKRO.ArcGIS
{
    public class AddUniqueID : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        public AddUniqueID()
        {
        }

        protected override void OnClick()
        {
            System.Windows.Forms.MessageBox.Show(this.GetType().ToString() + " Not Available");
        }

        protected override void OnUpdate()
        {
            Enabled = false;
        }
    }
}
