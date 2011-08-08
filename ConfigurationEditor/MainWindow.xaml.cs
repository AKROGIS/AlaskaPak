using System.Windows;
using Ionic.Zip;

namespace ConfigurationEditor
{
    public partial class MainWindow
    {
        public MainWindow()
        {
            InitializeComponent();
            SetDefaults();
        }

        //provide validation for all three text boxes
        //provide validation for form
        //disable save button until form validates

        private void SetDefaults()
        {
            //try to find the addin;
            //what about the others??
                //programer defautls?
                //read the addin for defaults?
        }

        private void BrowseForAddinPath(object sender, RoutedEventArgs e)
        {
            string newPath = GetPath("ArcGIS AddIn (.esriAddIn)|*.esriAddIn");
            if (newPath != null)
                addinPath.Text = newPath;
        }

        private void BrowseForThemeManagerPathPath(object sender, RoutedEventArgs e)
        {
            string newPath = GetPath("Application (.exe)|*.exe");
            if (newPath != null)
                themeManagerPath.Text = newPath;
        }

        private void BrowseForToolboxPath(object sender, RoutedEventArgs e)
        {
            string newPath = GetPath("ArcGIS Toolbox (.tbx)|*.tbx");
            if (newPath != null)
                toolboxPath.Text = newPath;
        }

        private void FixArchive(object sender, RoutedEventArgs e)
        {
            UpdateArchive(addinPath.Text, themeManagerPath.Text, toolboxPath.Text);
            Close();
        }

        private void Cancel(object sender, RoutedEventArgs e)
        {
            Close();
        }
        
        private static void UpdateArchive(string archive, string path1, string path2)
        {
            using (var zf = new ZipFile(archive))
            {
                zf.UpdateEntry("Install/PathToThemeManager.txt", path1);
                zf.UpdateEntry("Install/PathToToolbox.txt", path2);
                zf.Save();
            }
        }

        private static string GetPath(string filter)
        {
            var dlg = new Microsoft.Win32.OpenFileDialog
                          {
                              Filter = filter, 
                              CheckFileExists = true
                          };

            return dlg.ShowDialog() == true ? dlg.FileName : null;
        }

    }
}
