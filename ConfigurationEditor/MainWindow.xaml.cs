using System;
using System.IO;
using System.Linq;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Media;
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

        private void SetDefaults()
        {
            addinPath.Text = Directory.GetFiles(AssemblyDirectory, "*.esriAddIn").FirstOrDefault();
            ValidateFileName(addinPath);
            ReadAddin();
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
            bool saveIt = true;
            if (!File.Exists(themeManagerPath.Text) || !File.Exists(toolboxPath.Text))
            {
                MessageBoxResult result = MessageBox.Show("Are you sure you want to use an invalid path?",
                                                          "File Not Found",
                                                          MessageBoxButton.YesNo, MessageBoxImage.Question,
                                                          MessageBoxResult.No);
                saveIt = result == MessageBoxResult.Yes;
            }
            if (!saveIt)
                return;
            UpdateArchive(addinPath.Text, themeManagerPath.Text, toolboxPath.Text);
            Close();
        }

        private void Cancel(object sender, RoutedEventArgs e)
        {
            Close();
        }


        private static void UpdateArchive(string archive, string path1, string path2)
        {
            using (var zf = ZipFile.Read(archive))
            {
                //The standard ESRI addin has a '\' path separator, which fails to match in some cases.
                //ReadArchive() and zipFile[name] == "path\\name" work,
                //but RemoveEntry() and UpdateEntry() cannot delete the old entry, resulting in a corrupt archive.
                //Extracting the contents, and creating the zip with Windows creates a zip file that work fine.
                zf.UpdateEntry("Install/PathToThemeManager.txt", path1);
                zf.UpdateEntry("Install/PathToToolBox.txt", path2);
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

        private static string AssemblyDirectory
        {
            get
            {
                string codeBase = System.Reflection.Assembly.GetExecutingAssembly().CodeBase;
                var uri = new UriBuilder(codeBase);
                string path = Uri.UnescapeDataString(uri.Path);
                return Path.GetDirectoryName(path);
            }
        }

        private void ReadAddin()
        {
            try
            {
                themeManagerPath.Text = ReadArchive(addinPath.Text, "Install/PathToThemeManager.txt");
                ValidateFileName(themeManagerPath);
                toolboxPath.Text = ReadArchive(addinPath.Text, "Install/PathToToolbox.txt");
                ValidateFileName(toolboxPath);
                saveButton.IsEnabled = true;
            }
            catch (FileNotFoundException)
            {
                MessageBox.Show("No file at " + addinPath.Text, "File Not Found",
                                MessageBoxButton.OK, MessageBoxImage.Error);
                saveButton.IsEnabled = false;
            }
            catch (Exception)
            {
                MessageBox.Show(addinPath.Text + "\nis not a valid AlaskaPak AddIn.", "Bad AddIn",
                                MessageBoxButton.OK, MessageBoxImage.Error);
                saveButton.IsEnabled = false;
            }
        }

        private static void ValidateFileName(TextBox textBox)
        {
            if (textBox == null)
                return;

            textBox.Foreground = File.Exists(textBox.Text)
                                     ? SystemColors.ControlTextBrush
                                     : Brushes.DarkRed;
        }

        private string ReadArchive(string archive, string path)
        {
            if (!File.Exists(addinPath.Text))
                throw new FileNotFoundException(archive);

            using (var zf = ZipFile.Read(archive))
            {
                var stream = new MemoryStream();
                zf[path].Extract(stream);
                stream.Position = 0;
                var reader = new StreamReader(stream);
                return reader.ReadToEnd();
            }
        }

        private void TextChanged(object sender, TextChangedEventArgs e)
        {
            ValidateFileName(sender as TextBox);
        }

        private void AddInChanged(object sender, RoutedEventArgs e)
        {
            ReadAddin();
        }
    }
}
