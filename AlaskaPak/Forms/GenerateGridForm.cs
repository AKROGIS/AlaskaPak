using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Windows.Forms;

namespace NPS.AKRO.ArcGIS.Forms
{
    public partial class GenerateGridForm : Form
    {
        public GenerateGridForm()
        {
            InitializeComponent();
        }

        private void generateButton_Click(object sender, EventArgs e)
        {

        }

        private void cancelButton_Click(object sender, EventArgs e)
        {

        }

        private void browseButton_Click(object sender, EventArgs e)
        {

        }

        private void radioButton_CheckedChanged(object sender, EventArgs e)
        {

        }

        private void numericTextBox_TextChanged(object sender, EventArgs e)
        {

        }

        public void UpdateExtents(double x1, double y1, double x2, double y2)
        {
            xMinTextBox.Text = x1.ToString();
            xMaxTextBox.Text = x2.ToString();
            yMinTextBox.Text = y1.ToString();
            yMaxTextBox.Text = y2.ToString();
        }
    }
}
