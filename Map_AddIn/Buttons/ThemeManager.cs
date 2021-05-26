using System;
using System.IO;
using System.Diagnostics;
using System.Windows.Forms;

namespace NPS.AKRO.ArcGIS.Buttons
{
    public class ThemeManager : ESRI.ArcGIS.Desktop.AddIns.Button
    {
        protected override void OnClick()
        {
            AlaskaPak.RunProtected(GetType(), MyClick);
        }

        private static void MyClick()
        {
            string exe = Common.Settings.Get("PathToThemeManager");
            if (exe == null)
            {
                MessageBox.Show(@"Can't find the data file with the path to Theme Manager.",
                                @"Internal Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                return;
            }
            if (File.Exists(exe))
            {
                try
                {
                    string directory = Path.GetDirectoryName(exe);
                    if (directory == null)
                        return;
                    var startInfo = new ProcessStartInfo(exe) { WorkingDirectory = directory };
                    Process.Start(startInfo);
                }
                catch (System.ComponentModel.Win32Exception ex)
                {
                    if (ex.NativeErrorCode == 1223) //User canceled
                        return;
                    throw;
                }
                catch (Exception ex) //everything else
                {
                    MessageBox.Show(
                        @"Unable to start Theme Manager." + Environment.NewLine + exe + Environment.NewLine + @"Cause: " +
                        ex.Message,
                        @"Configuration Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
            }
            else
                MessageBox.Show(@"Path to Theme Manager is not valid." + Environment.NewLine + exe,
                                @"Configuration Error", MessageBoxButtons.OK, MessageBoxIcon.Error);
        }
    }
}
