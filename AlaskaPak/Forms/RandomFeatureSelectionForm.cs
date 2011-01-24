﻿using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using NPS.AKRO.ArcGIS.Common;

namespace NPS.AKRO.ArcGIS.Forms
{
    public partial class RandomFeatureSelectionForm : Form
    {
        private int _quantity;
        private int _total;

        public RandomFeatureSelectionForm()
        {
            InitializeComponent();
        }

        /// <summary>
        /// Fired when the user is ready to process the layer
        /// </summary>
        public event RandomSelectEventHandler SelectedLayer;

        public void LoadList(IEnumerable<Tuple<string, int>> layerinfo)
        {
            layerComboBox.DataSource = layerinfo.ToList();
            layerComboBox.DisplayMember = "Item1";
            if (layerComboBox.Items.Count > 0)
            {
                layerComboBox.SelectedIndex = 0;
                selectButton.Focus();
            }
        }

        private void selectButton_Click(object sender, EventArgs e)
        {
            OnRandomSelect();
        }

        private void cancelButton_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void layerComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            _total = ((Tuple<string, int>)layerComboBox.SelectedItem).Item2;
            UpdateQuantity();
            UpdateDescription();
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
            UpdateDescription();
        }

        private void UpdateQuantity()
        {
            double n;
            int q;
            int t = _total;
            if (percentRadioButton.Checked)
            {
                if (Double.TryParse(percentTextBox.Text, out n))
                {
                    q = Convert.ToInt32(n/100*t);
                }
                else
                {
                    q = -1;
                }
            }
            else
            {
                if (!Int32.TryParse(numberTextBox.Text, out q))
                {
                    q = -1;
                }
            }
            _quantity = q;
        }

        private void UpdateDescription()
        {
            int q = _quantity;
            int t = _total;
            if (q < 0 || q > t)
                descriptionTextBox.Text = "Invalid input, unable to compute quantity.";
            else
                descriptionTextBox.Text = string.Format("Randomly select {0} of {1} features",q,t);
        }

        private void percentTextBox_Validating(object sender, CancelEventArgs e)
        {
            double n;
            if (Double.TryParse(percentTextBox.Text, out n))
            {
                if (n < 0 || 100 < n)
                    e.Cancel = true;
            }
            else
                e.Cancel = true;
            if (e.Cancel)
                descriptionTextBox.Text = "Enter a number between 0 and 100";
        }

        private void numberTextBox_Validating(object sender, CancelEventArgs e)
        {
            int q;
            int t = _total;
            if (Int32.TryParse(numberTextBox.Text, out q))
            {
                if ( q < 0 || t < q)
                    e.Cancel = true;
            }
            else
                e.Cancel = true;
            if (e.Cancel)
                descriptionTextBox.Text = "Enter an integer between 0 and " + t;
            
        }

        private void textBox_Validated(object sender, EventArgs e)
        {
            UpdateQuantity();
            UpdateDescription();
        }

        [Obsolete]
        private void percentTextBox_KeyDown(object sender, KeyEventArgs e)
        {
            //add delete keys and arrow and enter and tab and ....
            if ((e.KeyData <= Keys.D9 && e.KeyData >= Keys.D0) || e.KeyData == Keys.Decimal)
            {
                UpdateQuantity();
                UpdateDescription();
            }
            else
            {
                descriptionTextBox.Text = "Invalid Input";
                e.SuppressKeyPress = true;
            }
        }

        private void textBox_KeyPress(object sender, KeyPressEventArgs e)
        {
            textBox_Validated(null, null);
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

    public delegate void RandomSelectEventHandler(object sender, RandomSelectEventArgs e);

    public class RandomSelectEventArgs : EventArgs
    {
        public int LayerIndex { get; set; }
        public int Count { get; set; }
    }

}
