using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;

namespace NPS.AKRO.ArcGIS.Forms
{
    public partial class CopyRasterSymbologyForm : Form
    {
        #region public methods

        public CopyRasterSymbologyForm()
        {
            InitializeComponent();
        }

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
        public void LoadLists(IEnumerable<string> layernames)
        {
            sourceComboBox.Items.Clear();
            sourceComboBox.Items.AddRange(layernames.ToArray());
            targetsListBox.Items.Clear();
            targetsListBox.Items.AddRange(layernames.ToArray());
            if (sourceComboBox.Items.Count > 0)
            {
                sourceComboBox.SelectedIndex = 0;
                selectAllButton_Click(null, null);
                copyButton.Focus();
            }
        }

        /// <summary>
        /// Fired when the user wants to initiate a copy
        /// </summary>
        public event CopyRasterEventHandler CopyRasterEvent;

        #endregion

        #region private control events

        private void selectAllButton_Click(object sender, EventArgs e)
        {
            for (int i = 0; i < targetsListBox.Items.Count; i++)
                targetsListBox.SetItemChecked(i,true);
            if (sourceComboBox.SelectedIndex != -1)
                targetsListBox.SetItemChecked(sourceComboBox.SelectedIndex, false);
        }

        private void unselectAllButton_Click(object sender, EventArgs e)
        {
            for (int i = 0; i < targetsListBox.Items.Count; i++)
                targetsListBox.SetItemChecked(i, false);
        }

        private void copyButton_Click(object sender, EventArgs e)
        {
            OnCopy();
        }

        private void cancelButton_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void sourceComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            targetsListBox.SetItemChecked(sourceComboBox.SelectedIndex, false);
            copyButton.Enabled = targetsListBox.CheckedItems.Count > 0;
        }

        private void destinationListBox_ItemCheck(object sender, ItemCheckEventArgs e)
        {
            if (e.Index == sourceComboBox.SelectedIndex)
                e.NewValue = CheckState.Unchecked;
            // ItemCheck event is called before item state has changed.  need to delay counting until later.
            // BeginInvoke() runs as soon as all events are dispatched, side-effects are complete and the UI thread goes idle again.
            // but it cannot be called until the window has a handle (has been shown).
            // see http://stackoverflow.com/questions/4454058/no-itemchecked-event-in-a-checkedlistbox/4454304#4454304
            if (this.IsHandleCreated)
            {
                this.BeginInvoke((MethodInvoker)delegate
                {
                    copyButton.Enabled = targetsListBox.CheckedItems.Count > 0;
                });
            }
        }

        protected override void OnLoad(EventArgs e)
        {
            base.OnLoad(e);
            copyButton.Enabled = targetsListBox.CheckedItems.Count > 0;
        }

        #endregion

        private void OnCopy()
        {
            CopyRasterEventHandler handle = CopyRasterEvent;
            if (handle != null)
                handle(this, new CopyRasterEventArgs {
                    Source = sourceComboBox.SelectedIndex, 
                    Targets = targetsListBox.CheckedIndices.Cast<int>()
                });
        }

    }


    public delegate void CopyRasterEventHandler(object sender, CopyRasterEventArgs e);

    public class CopyRasterEventArgs : EventArgs
    {
        public int Source { get; set; }
        public IEnumerable<int> Targets { get; set; }
    }

}
