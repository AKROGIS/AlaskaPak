using System;
using System.Collections.Generic;
using System.Linq;
using System.Windows.Forms;

namespace NPS.AKRO.ArcGIS.Forms
{
    public partial class CopyRasterLegendForm : Form
    {
        #region public methods

        public CopyRasterLegendForm()
        {
            InitializeComponent();
        }

        /// <summary>
        /// Loads the pick lists with a list of strings
        /// The client should call this when the loading the form,
        /// and whenever the list of layers changes
        /// </summary>
        /// <param name="layernames">List of layer names</param>
        public void LoadLists(IEnumerable<string> layernames)
        {
            //FIXME- If the client calls this after UI selections have been done
            //by the user, those selections will be lost.
            destinationListBox.Items.Clear();
            destinationListBox.Items.AddRange(layernames.ToArray());
            sourceComboBox.Items.Clear();
            sourceComboBox.Items.AddRange(layernames.ToArray());
            missingItem = null;
            sourceComboBox.SelectedIndex = 0;
            selectAllButton_Click(null, null);
            copyButton.Focus();
        }

        /// <summary>
        /// Fired when the user wants to initiate a copy
        /// </summary>
        public event CopyRasterEventHandler CopyHandler;

        #endregion


        #region private control events

        private void selectAllButton_Click(object sender, EventArgs e)
        {
            for (int i = 0; i < destinationListBox.Items.Count; i++)
                destinationListBox.SetItemChecked(i,true);
        }

        private void unselectAllButton_Click(object sender, EventArgs e)
        {
            for (int i = 0; i < destinationListBox.Items.Count; i++)
                destinationListBox.SetItemChecked(i, false);
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
            if (missingItem != null)
            {
                int newItem = destinationListBox.Items.Add(missingItem);
                destinationListBox.SetItemChecked(newItem, true);
            }
            missingItem = (string)sourceComboBox.SelectedItem;
            destinationListBox.Items.Remove(missingItem);
            copyButton.Enabled = destinationListBox.CheckedItems.Count > 0;
        }
        private string missingItem = null;

        //ItemCheck event is called before item state has changed.
        private void destinationListBox_ItemCheck(object sender, ItemCheckEventArgs e)
        {
            int count = destinationListBox.CheckedItems.Count;
            if (e.CurrentValue != CheckState.Checked && e.NewValue == CheckState.Checked)
            {
                count += 1;
            }
            else if (e.CurrentValue == CheckState.Checked && e.NewValue != CheckState.Checked)
            {
                count -= 1;
            }
            copyButton.Enabled = count > 0;
            // ItemCheck event is called before item state has changed.  need to delay counting until later.
            // BeginInvoke() runs as soon as all events are dispatched, side-effects are complete and the UI thread goes idle again
            // but it cannot be called until the window has a handle (has been shown).
            // see http://stackoverflow.com/questions/4454058/no-itemchecked-event-in-a-checkedlistbox/4454304#4454304
                //this.BeginInvoke((MethodInvoker)delegate
                //{
                //    copyButton.Enabled = destinationListBox.CheckedItems.Count > 0;
                //});
        }

        #endregion

        private void OnCopy()
        {
            CopyRasterEventHandler handle = CopyHandler;
            if (handle != null)
                handle(this, new CopyRasterEventArgs {
                    SourceName = sourceComboBox.Text, 
                    DestinationNames = destinationListBox.Items.Cast<string>()
                });
        }


    }


    public delegate void CopyRasterEventHandler(object sender, CopyRasterEventArgs e);

    public class CopyRasterEventArgs : EventArgs
    {
        public string SourceName { get; set; }
        public IEnumerable<string> DestinationNames { get; set; }
    }

}
