using System;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;
using NPS.AKRO.ArcGIS.Grids;

namespace NPS.AKRO.ArcGIS.Forms
{
    internal partial class GenerateGridForm : Form
    {
        internal Grid Grid { get; set; }
        internal ESRI.ArcGIS.Geodatabase.IFeatureWorkspace Workspace { get; set; }
        internal ESRI.ArcGIS.Geodatabase.IFeatureDataset Dataset { get; set; }
        internal string FeatureClassName { get; set; }

        internal GenerateGridForm()
        {
            InitializeComponent();
            unitsComboBox.Items.AddRange(LinearUnitsConverter.KnownUnits.ToArray());
        }

        private void cancelButton_Click(object sender, EventArgs e)
        {
            Close();
        }

        private void browseButton_Click(object sender, EventArgs e)
        {
            ESRI.ArcGIS.CatalogUI.IGxDialog browser = new ESRI.ArcGIS.CatalogUI.GxDialog();
            browser.ObjectFilter = new ESRI.ArcGIS.Catalog.GxFilterFeatureClassesClass();
            browser.Title = "Name of Feature Class to Create";

            if (!browser.DoModalSave((int)Handle))
                return;

            if (browser.ReplacingObject)
            {
                MessageBox.Show(@"Cannot overwrite an existing feature class.", @"Error", MessageBoxButtons.OK,
                                MessageBoxIcon.Error);
            }
            else
            {
                // shapefile folder
                if (browser.FinalLocation is ESRI.ArcGIS.Catalog.IGxFolder)
                {
                    Dataset = null;
                    ESRI.ArcGIS.Geodatabase.IWorkspaceFactory wsf =
                        new ESRI.ArcGIS.DataSourcesFile.ShapefileWorkspaceFactory();
                    Workspace =
                        wsf.OpenFromFile(browser.FinalLocation.FullName, 0) as ESRI.ArcGIS.Geodatabase.IFeatureWorkspace;
                }

                // geodatabase (root level)
                if (browser.FinalLocation is ESRI.ArcGIS.Catalog.IGxDatabase)
                {
                    Dataset = null;
                    Workspace =
                        ((ESRI.ArcGIS.Catalog.IGxDatabase)browser.FinalLocation).Workspace as
                        ESRI.ArcGIS.Geodatabase.IFeatureWorkspace;
                }

                // feature dataset in a geodatabase
                if (browser.FinalLocation is ESRI.ArcGIS.Catalog.IGxDataset)
                {
                    Dataset =
                        ((ESRI.ArcGIS.Catalog.IGxDataset)browser.FinalLocation).Dataset as
                        ESRI.ArcGIS.Geodatabase.IFeatureDataset;
                    Workspace =
                        ((ESRI.ArcGIS.Catalog.IGxDataset)browser.FinalLocation).Dataset.Workspace as
                        ESRI.ArcGIS.Geodatabase.IFeatureWorkspace;
                    var geoDataset = (ESRI.ArcGIS.Geodatabase.IGeoDataset)Dataset;
                    if (geoDataset != null)
                        spatialReferenceTextBox.Text = geoDataset.SpatialReference.Name;
                }

                if (Workspace == null)
                {
                    MessageBox.Show(@"Location is not a valid feature workspace.", @"Error", MessageBoxButtons.OK,
                                    MessageBoxIcon.Error);
                    outputPathTextBox.Text = "";
                    saveButton.Enabled = false;
                }
                else
                {
                    FeatureClassName = browser.Name;
                    outputPathTextBox.Text = browser.FinalLocation.FullName + @"\" + FeatureClassName;
                    saveButton.Enabled = true;
                }
                spatialReferenceTextBox.Text = (Dataset == null)
                                                   ? @"Unknown"
                                                   : ((ESRI.ArcGIS.Geodatabase.IGeoDataset)Dataset).SpatialReference.
                                                         Name;
            }
        }

        private void PreviewButton_Click(object sender, EventArgs e)
        {
            if (_updating)
                return;
            Grid.RowHeight = LinearUnitsConverter.ToMeters(Convert.ToDouble(heightTextBox.Text), unitsComboBox.Text)/
                             Grid.MetersPerUnit;
            Grid.ColumnWidth = LinearUnitsConverter.ToMeters(Convert.ToDouble(widthTextBox.Text), unitsComboBox.Text)/
                               Grid.MetersPerUnit;
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

        private void OptionalPreviewButton_Click(object sender, EventArgs e)
        {
            if (Grid.ColumnCount*Grid.RowCount <= 250)
                PreviewButton_Click(sender, e);
        }

        private void unitsComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            //don't do anything if we are called while updating.
            if (_updating)
                return;

            //Turn off redraws triggered by changes in the form.
            _updating = true;

            double metersPerUserUnit = LinearUnitsConverter.ToMeters(1, unitsComboBox.Text);
            //RowHeight and ColumnWidth are in Grid units, convert to meters to convert to user units
            heightTextBox.Text = (Grid.RowHeight*Grid.MetersPerUnit/metersPerUserUnit).ToString();
            widthTextBox.Text = (Grid.ColumnWidth*Grid.MetersPerUnit/metersPerUserUnit).ToString();

            _updating = false;
        }

        //private void radioButton_CheckedChanged(object sender, EventArgs e)
        //{

        //}

        //private void sizeRadioButton_CheckedChanged(object sender, EventArgs e)
        //{
        //    if (((RadioButton)sender).Checked)
        //    {
        //        xCountTextBox.Enabled = true;
        //        yCountTextBox.Enabled = true;
        //    }
        //}

        private void DoubleTextBox_TextChanged(object sender, EventArgs e)
        {
            var textBox = sender as TextBox;
            //Debug.Assert(textBox != null, "non TextBox object hooked up to DoubleTextBox_TextChanged()");
            if (textBox == null)
                return;
            double number;
            if (Double.TryParse(textBox.Text, out number))
                textBox.ForeColor = Color.Black;
            else
            {
                textBox.ForeColor = Color.Red;
                textBox.Focus();
            }
        }

        private void IntegerTextBox_TextChanged(object sender, EventArgs e)
        {
            var textBox = sender as TextBox;
            //Debug.Assert(textBox != null, "non TextBox object hooked up to IntTextBox_TextChanged()");
            if (textBox == null)
                return;
            int number;
            if (Int32.TryParse(textBox.Text, out number))
                textBox.ForeColor = Color.Black;
            else
            {
                textBox.ForeColor = Color.Red;
                textBox.Focus();
            }
        }

        private void SizeTextBox_Leave(object sender, EventArgs e)
        {
            if (!AllInputIsValid)
                return;
            double w = Convert.ToDouble(widthTextBox.Text);
            double h = Convert.ToDouble(heightTextBox.Text);
            if (Math.Abs(Grid.ColumnWidth - w) > EPSILON || Math.Abs(Grid.RowHeight - h) > EPSILON)
            {
                Grid.RowHeight = LinearUnitsConverter.ToMeters(h, unitsComboBox.Text)/Grid.MetersPerUnit;
                Grid.ColumnWidth = LinearUnitsConverter.ToMeters(w, unitsComboBox.Text)/Grid.MetersPerUnit;
                if (!Grid.IsValid)
                {
                    //make it valid
                    Grid.AdjustExtents();
                    UpdateFormFromGrid();
                }
                OptionalPreviewButton_Click(sender, e);
            }
        }

        private void CountTextBox_Leave(object sender, EventArgs e)
        {
            if (!AllInputIsValid)
                return;
            int x = Convert.ToInt32(xCountTextBox.Text);
            int y = Convert.ToInt32(yCountTextBox.Text);
            if (Grid.ColumnCount != x || Grid.RowCount != y)
            {
                Grid.ColumnCount = x;
                Grid.RowCount = y;
                if (!Grid.IsValid)
                {
                    //make it valid
                    Grid.AdjustExtents();
                    UpdateFormFromGrid();
                }
                OptionalPreviewButton_Click(sender, e);
            }
        }

        internal void UpdateFormFromGrid()
        {
            _updating = true;
            //Set the default units to the map units, if that fails use meters.
            if (unitsComboBox.SelectedIndex == -1)
                unitsComboBox.SelectedItem = LinearUnitsConverter.Key(Grid.Map.MapUnits);

            //RowHeight and ColumnWidth are in Grid units, convert to meters to convert to user units
            double metersPerUserUnit = LinearUnitsConverter.ToMeters(1, unitsComboBox.Text);
            heightTextBox.Text = (Grid.RowHeight*Grid.MetersPerUnit/metersPerUserUnit).ToString();
            widthTextBox.Text = (Grid.ColumnWidth*Grid.MetersPerUnit/metersPerUserUnit).ToString();

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
        private const double EPSILON = 1e-14;

        internal bool AllInputIsValid
        {
            get
            {
                //FIXME - do something intelligent
                return true;
            }
        }
    }
}
