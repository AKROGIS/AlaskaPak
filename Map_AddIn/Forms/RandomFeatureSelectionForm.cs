﻿using System;
using System.Collections.Generic;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;
using NPS.AKRO.ArcGIS.Common;

namespace NPS.AKRO.ArcGIS.Forms
{
    internal partial class RandomFeatureSelectionForm : Form
    {
        private int _quantity;
        private int _total;

        internal RandomFeatureSelectionForm()
        {
            InitializeComponent();
        }

        /// <summary>
        /// Fired when the user is ready to process the layer
        /// </summary>
        internal event RandomSelectEventHandler SelectedLayer;

        internal void LoadList(IEnumerable<Tuple<string, int>> layerinfo)
        {
            layerComboBox.DataSource = layerinfo.ToList();
            layerComboBox.DisplayMember = "Item1";
            if (layerComboBox.Items.Count <= 0)
                return;
            layerComboBox.SelectedIndex = 0;
            selectButton.Focus();
        }

        private void selectButton_Click(object sender, EventArgs e)
        {
            OnRandomSelect();
        }

        private void cancelButton_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void layerComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            _total = ((Tuple<string, int>)layerComboBox.SelectedItem).Item2;
            UpdateQuantity();
            UpdateForm();
        }

        private void percentRadioButton_CheckedChanged(object sender, EventArgs e)
        {
            if (percentRadioButton.Checked)
            {
                percentTextBox.Enabled = true;
                numberTextBox.Enabled = false;
            }
            else
            {
                percentTextBox.Enabled = false;
                numberTextBox.Enabled = true;
            }
            UpdateQuantity();
            UpdateForm();
        }

        private void textBox_TextChanged(object sender, EventArgs e)
        {
            UpdateQuantity();
            UpdateForm();
        }

        private void UpdateQuantity()
        {
            int q;
            int t = _total;
            if (percentRadioButton.Checked)
            {
                double n;
                if (Double.TryParse(percentTextBox.Text, out n))
                {
                    if (n < 0 || 100 < n)
                    {
                        q = -1;
                    }
                    else
                    {
                        q = Convert.ToInt32(n / 100 * t);
                    }
                }
                else
                {
                    q = -1;
                }
            }
            else
            {
                if (Int32.TryParse(numberTextBox.Text, out q))
                {
                    if (q < 0 || t < q)
                    {
                        q = -1;
                    }
                }
                else
                {
                    q = -1;
                }
            }
            _quantity = q;
        }

        private void UpdateForm()
        {
            int q = _quantity;
            int t = _total;
            if (q == -1)
            {
                descriptionTextBox.ForeColor = Color.Red;
                selectButton.Enabled = false;
                if (percentRadioButton.Checked)
                {
                    percentTextBox.ForeColor = Color.Red;
                    descriptionTextBox.Text = @"Enter a percentage from 0 to 100";
                }
                else
                {
                    numberTextBox.ForeColor = Color.Red;
                    descriptionTextBox.Text = @"Enter an integer between 0 and " + t;
                }
            }
            else
            {
                selectButton.Enabled = true;
                numberTextBox.ForeColor = Color.Black;
                percentTextBox.ForeColor = Color.Black;
                descriptionTextBox.ForeColor = Color.Black;
                descriptionTextBox.Text = string.Format("Randomly select {0} of {1} features", q, t);
            }
        }

        private void OnRandomSelect()
        {
            RandomSelectEventHandler handle = SelectedLayer;
            if (handle != null)
                handle(this, new RandomSelectEventArgs
                {
                    LayerIndex = layerComboBox.SelectedIndex,
                    Count = _quantity
                });
        }
    }

    internal delegate void RandomSelectEventHandler(object sender, RandomSelectEventArgs e);

    internal class RandomSelectEventArgs : EventArgs
    {
        internal int LayerIndex { get; set; }
        internal int Count { get; set; }
    }
}
