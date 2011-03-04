using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;
using NPS.AKRO.ArcGIS.Grids;

namespace NPS.AKRO.ArcGIS.Forms
{
    public partial class GenerateGridForm : Form
    {
        public Grid Grid { get; set; }

        public GenerateGridForm()
        {
            InitializeComponent();
            unitsComboBox.Items.AddRange(LinearUnitsConverter.KnownUnits.ToArray());
        }

        private void PreviewButton_Click(object sender, EventArgs e)
        {
            if (!_updating)
            {
                Grid.Extents.XMin = Convert.ToDouble(xMinTextBox.Text);
                Grid.Extents.XMax = Convert.ToDouble(xMaxTextBox.Text);
                Grid.Extents.YMin = Convert.ToDouble(yMinTextBox.Text);
                Grid.Extents.YMax = Convert.ToDouble(yMaxTextBox.Text);
                Grid.RowHeight = LinearUnitsConverter.ToMeters(Convert.ToDouble(heightTextBox.Text), unitsComboBox.Text);
                Grid.ColumnWidth = LinearUnitsConverter.ToMeters(Convert.ToDouble(widthTextBox.Text), unitsComboBox.Text);
                Grid.RowCount = Convert.ToInt32(yCountTextBox.Text);
                Grid.ColumnCount = Convert.ToInt32(xCountTextBox.Text);

                Grid.Delimiter = delimiterTextBox.Text;
                Grid.Prefix = prefixTextBox.Text;
                Grid.Suffix = suffixTextBox.Text;
                // This requires me to keep the combo box text and ordering in sync with my enums
                // but it allows me to be more descriptive in my combo box text
                Grid.RowLabelStyle = (GridLabelStyle)rowStyleComboBox.SelectedIndex;
                Grid.ColumnLabelStyle = (GridLabelStyle)columnStyleComboBox.SelectedIndex;
                Grid.LabelOrder = (GridLabelOrder)conventionComboBox.SelectedIndex;
                Grid.PageNumbering = (GridPageNumbering)pageNumberComboBox.SelectedIndex;

                Grid.Draw();
            }
        }

        private void OptionalPreviewButton_Click(object sender, EventArgs e)
        {
            if (Grid.ColumnCount * Grid.RowCount <= 250)
                PreviewButton_Click(sender, e);
        }

        private void saveButton_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Tool is not fully functional yet");
        }

        private void cancelButton_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void browseButton_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Function not implemented yet");
        }

        private void radioButton_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void sizeRadioButton_CheckedChanged(object sender, EventArgs e)
        {
            if (((RadioButton)sender).Checked)
            {
                xCountTextBox.Enabled = true;
                yCountTextBox.Enabled = true;
            }
        }

        private void doubleTextBox_TextChanged(object sender, EventArgs e)
        {
            double number;
            TextBox textBox = sender as TextBox;
            if (Double.TryParse(textBox.Text, out number))
                textBox.ForeColor = Color.Black;
            else
            {
                textBox.ForeColor = Color.Red;
                textBox.Focus();
            }
        }

        private void integerTextBox_TextChanged(object sender, EventArgs e)
        {
            int number;
            TextBox textBox = sender as TextBox;
            if (Int32.TryParse(textBox.Text, out number))
                textBox.ForeColor = Color.Black;
            else
            {
                textBox.ForeColor = Color.Red;
                textBox.Focus();
            }
        }

        private void sizeTextBox_Leave(object sender, EventArgs e)
        {
            if (AllInputIsValid)
            {
                Grid.ColumnWidth = Convert.ToDouble(widthTextBox.Text);
                Grid.RowHeight = Convert.ToDouble(heightTextBox.Text);
                if (!Grid.isValid)
                    Grid.AdjustCountThenExtents();
                OptionalPreviewButton_Click(sender, e);
            }
        }

        private void countTextBox_Leave(object sender, EventArgs e)
        {
            if (AllInputIsValid)
            {
                Grid.ColumnCount = Convert.ToInt32(xCountTextBox.Text);
                Grid.RowCount = Convert.ToInt32(yCountTextBox.Text);
                if (!Grid.isValid)
                    Grid.AdjustSize();
                OptionalPreviewButton_Click(sender, e);
            }
        }

        private void extentTextBox_Leave(object sender, EventArgs e)
        {
            if (AllInputIsValid)
            {
                Grid.Extents.XMin = Convert.ToDouble(xMinTextBox.Text);
                Grid.Extents.XMax = Convert.ToDouble(xMaxTextBox.Text);
                Grid.Extents.YMin = Convert.ToDouble(yMinTextBox.Text);
                Grid.Extents.YMax = Convert.ToDouble(yMaxTextBox.Text);
                if (!Grid.isValid)
                    Grid.AdjustCountThenSize();
                OptionalPreviewButton_Click(sender, e);
            }
        }

        private void xTextBox_TextChanged(object sender, EventArgs e)
        {
            double number;
            if (Double.TryParse(xMinTextBox.Text, out number))
            {
                Grid.Extents.XMin = Convert.ToDouble(xMinTextBox.Text);
                Grid.AdjustCountThenSize();
                Grid.Draw();
            }
            else
            {
                xMinTextBox.ForeColor = Color.Red;
                xMinTextBox.Focus();
                return;
            }

            if (Double.TryParse(xMaxTextBox.Text, out number))
            {
                Grid.Extents.XMax = Convert.ToDouble(xMaxTextBox.Text);
                Grid.AdjustCountThenSize();
                Grid.Draw();
            }
            else
            {
                xMaxTextBox.ForeColor = Color.Red;
                xMaxTextBox.Focus();
                return;
            }

            if (Double.TryParse(yMinTextBox.Text, out number))
            {
                Grid.Extents.YMin = Convert.ToDouble(yMinTextBox.Text);
                Grid.AdjustCountThenSize();
                Grid.Draw();
            }
            else
            {
                yMinTextBox.ForeColor = Color.Red;
                yMinTextBox.Focus();
                return;
            }

            if (Double.TryParse(yMaxTextBox.Text, out number))
            {
                Grid.Extents.YMax = Convert.ToDouble(yMaxTextBox.Text);
                Grid.AdjustCountThenSize();
                Grid.Draw();
            }
            else
            {
                yMaxTextBox.ForeColor = Color.Red;
                yMaxTextBox.Focus();
                return;
            }

            if (Double.TryParse(heightTextBox.Text, out number))
            {
                Grid.RowHeight = Convert.ToDouble(heightTextBox.Text);
                Grid.AdjustCountThenExtents();
                Grid.Draw();
            }
            else
            {
                heightTextBox.ForeColor = Color.Red;
                heightTextBox.Focus();
                return;
            }
            if (Double.TryParse(widthTextBox.Text, out number))
            {
                Grid.ColumnWidth = Convert.ToDouble(widthTextBox.Text);
                Grid.AdjustCountThenExtents();
                Grid.Draw();
            }
            else
            {
                widthTextBox.ForeColor = Color.Red;
                widthTextBox.Focus();
                return;
            }

            int count;
            if (Int32.TryParse(xCountTextBox.Text, out count))
            {
                Grid.ColumnCount = Convert.ToInt32(xCountTextBox.Text);
                Grid.AdjustSize();
                Grid.Draw();
            }
            else
            {
                xCountTextBox.ForeColor = Color.Red;
                xCountTextBox.Focus();
                return;
            }

            if (Int32.TryParse(yCountTextBox.Text, out count))
            {
                Grid.RowCount = Convert.ToInt32(yCountTextBox.Text);
                Grid.AdjustSize();
                Grid.Draw();
            }
            else
            {
                yCountTextBox.ForeColor = Color.Red;
                yCountTextBox.Focus();
                return;
            }
        }

        public void UpdateFromGrid()
        {
            _updating = true;
            xMinTextBox.Text = Grid.Extents.XMin.ToString();
            xMaxTextBox.Text = Grid.Extents.XMax.ToString();
            yMinTextBox.Text = Grid.Extents.YMin.ToString();
            yMaxTextBox.Text = Grid.Extents.YMax.ToString();
            heightTextBox.Text = Grid.RowHeight.ToString();
            widthTextBox.Text = Grid.ColumnWidth.ToString();
            yCountTextBox.Text = Grid.RowCount.ToString();
            xCountTextBox.Text = Grid.ColumnCount.ToString();

            delimiterTextBox.Text = Grid.Delimiter;
            prefixTextBox.Text = Grid.Prefix;
            suffixTextBox.Text = Grid.Suffix;
            // The requires me to keep the combo box text and ordering in sync with my enums
            // but it allows me to be more descriptive in my combo box text
            rowStyleComboBox.SelectedIndex = (int)Grid.RowLabelStyle;
            columnStyleComboBox.SelectedIndex = (int)Grid.ColumnLabelStyle;
            conventionComboBox.SelectedIndex = (int)Grid.LabelOrder;
            pageNumberComboBox.SelectedIndex = (int)Grid.PageNumbering;
            _updating = false;
        }
        private bool _updating;


        public bool AllInputIsValid
        {
            get
            {
                //FIXME - do something intelligent
                return true;
            }
        }

    }
}
