using System;
using System.Reflection;
using System.Windows;

namespace ConfigurationEditor
{
    public class App : Application
    {
        public void InitializeComponent()
        {
            StartupUri = new Uri("MainWindow.xaml", UriKind.Relative);
        }

        [STAThreadAttribute]
        public static void Main()
        {
            var app = new App();
            app.InitializeComponent();
            AppDomain.CurrentDomain.AssemblyResolve += (sender, args) =>
            {
                String resourceName = "ConfigurationEditor." +
                                      new AssemblyName(args.Name).Name +
                                      ".dll";
                using (var stream = Assembly.GetExecutingAssembly().
                                             GetManifestResourceStream(resourceName))
                {
                    if (stream == null)
                        return null;
                    var assemblyData = new Byte[stream.Length];
                    stream.Read(assemblyData, 0, assemblyData.Length);
                    return Assembly.Load(assemblyData);
                }
            };
            app.Run();
        }
    }
}
