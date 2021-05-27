using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows;
using System.Windows.Controls;
using System.Windows.Data;
using System.Windows.Documents;
using System.Windows.Input;
using System.Windows.Media;
using System.Windows.Media.Imaging;
using System.Windows.Navigation;
using System.Windows.Shapes;

namespace AlaskaPak.UI
{
    /// <summary>
    /// Interaction logic for CopyRasterSymbologyWindow.xaml
    /// </summary>
    public partial class CopyRasterSymbologyWindow : ArcGIS.Desktop.Framework.Controls.ProWindow
    {
        public CopyRasterSymbologyWindow()
        {
            InitializeComponent();
        }

        #region internal methods

        /// <summary>
        /// Loads the pick lists with a list of strings
        /// The client should call this when the loading the form,
        /// and whenever the list of layers changes
        /// </summary>
        /// <remarks>
        /// Names are not guaranteed to be unique.
        /// Form should not change the ordering of the names
        /// form will return the indicies of the selected names, so the
        /// caller knows which items to act on.
        /// </remarks>
        /// <param name="layernames">List of layer names (not necessarily unique)</param>
        internal void LoadLists(IEnumerable<string> layernames)
        {
            sourceComboBox.Items.Clear();
            targetsListBox.Items.Clear();
            object[] items = layernames.Cast<object>().ToArray();
            if (items.Length <= 0)
                return;
            //sourceComboBox.Items.AddRange(items);
            //targetsListBox.Items.AddRange(items);
            sourceComboBox.SelectedIndex = 0;
            selectAllButton_Click(null, null);
            copyButton.Focus();
        }

        /// <summary>
        /// Fired when the user wants to initiate a copy
        /// </summary>
        internal event CopyRasterEventHandler CopyRasterEvent;

        #endregion

        #region private control events

        private void copyButton_Click(object sender, RoutedEventArgs e)
        {
            OnCopy();
            Close();
        }

        private void cancelButton_Click(object sender, RoutedEventArgs e)
        {
            Close();
        }

        private void unselectAllButton_Click(object sender, RoutedEventArgs e)
        {
            //for (int i = 0; i < targetsListBox.Items.Count; i++)
            //    targetsListBox.SetItemChecked(i, false);
        }

        private void selectAllButton_Click(object sender, RoutedEventArgs e)
        {
            //for (int i = 0; i < targetsListBox.Items.Count; i++)
            //    targetsListBox.SetItemChecked(i, true);
            //if (sourceComboBox.SelectedIndex != -1)
            //    targetsListBox.SetItemChecked(sourceComboBox.SelectedIndex, false);
        }

        private void sourceComboBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            //targetsListBox.SetItemChecked(sourceComboBox.SelectedIndex, false);
            //copyButton.IsEnabled = targetsListBox.CheckedItems.Count > 0;
        }

        private void targetsListBox_SelectionChanged(object sender, SelectionChangedEventArgs e)
        {
            //if (e.Index == sourceComboBox.SelectedIndex)
            //    e.NewValue = CheckState.Unchecked;
            // ItemCheck event is called before item state has changed.  need to delay counting until later.
            // BeginInvoke() runs as soon as all events are dispatched, side-effects are complete and the UI thread goes idle again.
            // but it cannot be called until the window has a handle (has been shown).
            // see http://stackoverflow.com/questions/4454058/no-itemchecked-event-in-a-checkedlistbox/4454304#4454304
            //if (IsHandleCreated)
            //{
            //    BeginInvoke((MethodInvoker)delegate { copyButton.Enabled = targetsListBox.CheckedItems.Count > 0; });
            //}
        }

        private void copyRasterSymbologyWindow_Loaded(object sender, RoutedEventArgs e)
        {
            //copyButton.IsEnabled = targetsListBox.CheckedItems.Count > 0;
        }

        #endregion

        private void OnCopy()
        {
            CopyRasterEventHandler handle = CopyRasterEvent;
            if (handle != null)
                handle(this, new CopyRasterEventArgs
                {
                    Source = sourceComboBox.SelectedIndex,
                    //Targets = targetsListBox.CheckedIndices.Cast<int>()
                });
        }

    }

    internal delegate void CopyRasterEventHandler(object sender, CopyRasterEventArgs e);

    internal class CopyRasterEventArgs : EventArgs
    {
        internal int Source { get; set; }
        internal IEnumerable<int> Targets { get; set; }
    }
}
