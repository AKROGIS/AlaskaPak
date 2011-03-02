using System;
using System.Drawing;
using System.Linq;
using System.Windows.Forms;
using ESRI.ArcGIS.Geodatabase;  // for esriFieldNameErrorType
using NPS.AKRO.ArcGIS.AddCoordinates;

namespace NPS.AKRO.ArcGIS.Forms
{
    public partial class AddXYForm : Form
    {
        internal AddXYForm(FormData data)
        {
            InitializeComponent();
            Data = data;
        }

        internal FormData Data
        { 
            get
            {
                return _data;
            } 
            set
            {
                if (value != _data)
                {
                    _data = value;
                    formatStyleComboBox.Items.AddRange(_data.Format.Names.ToArray());
                    formatStyleComboBox.SelectedIndex = (int)_data.Format.OutputFormat;
                    PointLayersChanged();
                    xFieldComboBox.Text = _data.DefaultXFieldName;
                    yFieldComboBox.Text = _data.DefaultYFieldName;
                }
            }
        }
        private FormData _data;

        public void PointLayersChanged()
        {
            featureClassComboBox.Items.Clear();
            featureClassComboBox.Items.AddRange(Data.PointLayerNames.ToArray());
            if (Data.LayerIndex == -1)
            {
                featureClassComboBox.SelectedText = Data.FeatureClassPath;
            }
            else
                featureClassComboBox.SelectedIndex = Data.LayerIndex;
            UpdateOkButton();
        }


        private void featureClassComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            if (featureClassComboBox.SelectedIndex == -1)
                Data.FeatureClassPath = featureClassComboBox.SelectedText;
            else
                Data.LayerIndex = featureClassComboBox.SelectedIndex;
            UpdateFieldNameComboBoxes();
            UpdateOkButton();
        }

        private void formatStyleComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            Data.Format.OutputFormat = (FormatterOutputFormat)formatStyleComboBox.SelectedIndex;
            UpdateFieldNameComboBoxes();
            UpdateOkButton();
            if (Data.Format.Formattable)
            {
                formattingOptionsButton.Enabled = true;
                if (_showAdvanced == true && !panel1.Visible)
                    formattingOptionsButton_Click(sender, e);
                if (panel1.Visible)
                {
                    ValidateFormatOptions();
                    DoSafePreview();
                }
            }
            else
            {
                if (panel1.Visible)
                {
                    _showAdvanced = true;
                    formattingOptionsButton_Click(sender, e);
                }
                else
                {
                    _showAdvanced = false;
                }
                formattingOptionsButton.Enabled = false;
            }
        }
        private bool _showAdvanced = false;


        private void UpdateFieldNameComboBoxes()
        {
            if (xFieldComboBox.Items.IndexOf(xFieldComboBox.Text) == xFieldComboBox.Items.Count - 1)
                xFieldComboBox.Text = Data.DefaultXFieldName;
            xFieldComboBox.Items.Clear();
            xFieldComboBox.Items.AddRange(Data.GetAppropriateFieldNames().ToArray());
            if (!xFieldComboBox.Items.Contains(Data.DefaultXFieldName))
                xFieldComboBox.Items.Add(Data.DefaultXFieldName);

            if (yFieldComboBox.Items.IndexOf(yFieldComboBox.Text) == yFieldComboBox.Items.Count - 1)
                yFieldComboBox.Text = Data.DefaultYFieldName;
            yFieldComboBox.Items.Clear();
            yFieldComboBox.Items.AddRange(Data.GetAppropriateFieldNames().ToArray());
            if (!yFieldComboBox.Items.Contains(Data.DefaultYFieldName))
                yFieldComboBox.Items.Add(Data.DefaultYFieldName);

            CheckFieldNames();
        }

        private void fieldNameComboBox_SelectedIndexChanged(object sender, EventArgs e)
        {
            CheckFieldNames();
            UpdateOkButton();
        }

        private void fieldNameComboBox_TextChanged(object sender, EventArgs e)
        {
            CheckFieldNames();
            UpdateOkButton();
        }

        private void CheckFieldNames()
        {
            if (xFieldComboBox.Text == yFieldComboBox.Text &&
                !string.IsNullOrEmpty(xFieldComboBox.Text))
            {
                string msg = "Cannot use the same field name for both coordinates.";
                invalidEntry.SetError(xFieldComboBox, msg);
                overwriteWarning.SetError(xFieldComboBox, "");
                invalidEntry.SetError(yFieldComboBox, msg);
                overwriteWarning.SetError(yFieldComboBox, "");
            }
            else
            {
                var validFieldNames = Data.GetAppropriateFieldNames();
                foreach (ComboBox cb in new ComboBox[] { xFieldComboBox, yFieldComboBox })
                {
                    esriFieldNameErrorType err = Data.ValidateFieldName(cb.Text);
                    switch (err)
                    {
                        case esriFieldNameErrorType.esriDuplicatedFieldName:
                            if (validFieldNames.Select(n => n.ToLower()).Contains(cb.Text.ToLower()))
                            {
                                overwriteWarning.SetError(cb, "Existing values in this field will be overwritten");
                                invalidEntry.SetError(cb, "");
                            }
                            else
                            {
                                overwriteWarning.SetError(cb, "");
                                invalidEntry.SetError(cb, "An incompatible field already exists with this name.\nSelect a different field\nor enter a new field name.");
                            }
                            break;
                        case esriFieldNameErrorType.esriInvalidCharacter:
                            overwriteWarning.SetError(cb, "");
                            invalidEntry.SetError(cb, "New field name has unacceptable characters.\nChange the field name.");
                            break;
                        case esriFieldNameErrorType.esriInvalidFieldNameLength:
                            overwriteWarning.SetError(cb, "");
                            invalidEntry.SetError(cb, "New field name is too long.\nShorten the field name.");
                            break;
                        default:
                        case esriFieldNameErrorType.esriNoFieldError:
                            overwriteWarning.SetError(cb, "");
                            invalidEntry.SetError(cb, "");
                            break;
                        case esriFieldNameErrorType.esriSQLReservedWord:
                            overwriteWarning.SetError(cb, "");
                            invalidEntry.SetError(cb, "New field name is a reserved word.\nChange the field name.");
                            break;
                    }
                }
            }
            if (string.IsNullOrEmpty(invalidEntry.GetError(xFieldComboBox)))
                Data.XFieldName = xFieldComboBox.Text;
            else
                Data.XFieldName = string.Empty;
            if (string.IsNullOrEmpty(invalidEntry.GetError(yFieldComboBox)))
                Data.YFieldName = yFieldComboBox.Text;
            else
                Data.YFieldName = string.Empty;
        }

        private void UpdateOkButton()
        {
            okButton.Enabled = Data.IsReady;
        }

        private void browseButton_Click(object sender, EventArgs e)
        {
            MessageBox.Show("Browse not available yet.");
        }

        private void cancelButton_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void okButton_Click(object sender, EventArgs e)
        {

        }

        #region  Lat/Lon formatting/preview

        private void formattingOptionsButton_Click(object sender, EventArgs e)
        {
            if (formattingOptionsButton.ImageIndex == 0)
            {
                formattingOptionsButton.ImageIndex = 1;
                panel1.Visible = false;
                int newHeight = 240;
                this.MinimumSize = new Size(this.MinimumSize.Width, newHeight);
                this.MaximumSize = new Size(this.MaximumSize.Width, newHeight);
                this.Height = newHeight;
            }
            else
            {
                formattingOptionsButton.ImageIndex = 0;
                panel1.Visible = true;
                int newHeight = 360;
                this.MinimumSize = new Size(this.MinimumSize.Width, newHeight);
                this.MaximumSize = new Size(this.MaximumSize.Width, newHeight);
                this.Height = newHeight;

                ValidateFormatOptions();
                DoSafePreview();
            }
        }

        private void DoSafePreview()
        {
            double decimalDegrees = 0;
            if (panel1.Visible && Double.TryParse(sampleInput.Text, out decimalDegrees))
            {
                try
                {
                    DoPreview(decimalDegrees);
                }
                catch (ArgumentOutOfRangeException ex)
                {
                    sampleOutput.Text = "Error";
                    MessageBox.Show(ex.Message, "Invalid Input");
                }
            }
        }

        private void DoPreview(double decimalDegrees)
        {
            Data.Format.OutputFormat = (FormatterOutputFormat)formatStyleComboBox.SelectedIndex;
            Data.Format.Decimals = (int)numericUpDown1.Value;
            Data.Format.ShowDirection = showDirectionCheckBox.Checked;
            Data.Format.ShowSpaces = showSpacesCheckBox.Checked;
            Data.Format.ShowZeroParts = showTrailingZerosCheckBox.Checked;

            sampleOutput.Text = Data.Format.Format(decimalDegrees, isLatitudeCheckBox.Checked);
        }


        private void ValidateFormatOptions()
        {
            showTrailingZerosCheckBox.Enabled = true;
            showSpacesCheckBox.Enabled = true;
            numericUpDown1.Value = Data.Format.DefaultDecimals;
            if (formatStyleComboBox.SelectedIndex == (int)FormatterOutputFormat.DecimalDegress)
            {
                showTrailingZerosCheckBox.Enabled = false;
                if (!showDirectionCheckBox.Checked)
                    showSpacesCheckBox.Enabled = false;
            }
        }

        private void ShowDirectionCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            //no possible space with signed decimal degrees
            if (formatStyleComboBox.SelectedIndex == (int)FormatterOutputFormat.DecimalDegress &&
                !showDirectionCheckBox.Checked)
                showSpacesCheckBox.Enabled = false;
            else
                showSpacesCheckBox.Enabled = true;
            DoSafePreview();
        }


        private void checkBox_CheckedChanged(object sender, EventArgs e)
        {
            DoSafePreview();
        }


        private void numericUpDown1_ValueChanged(object sender, EventArgs e)
        {
            DoSafePreview();
        }


        private void isLatitudeCheckBox_CheckedChanged(object sender, EventArgs e)
        {
            input_TextChanged(sender, e);
        }

        private void input_TextChanged(object sender, EventArgs e)
        {
            double decimalDegrees = 0;
            if (Double.TryParse(sampleInput.Text, out decimalDegrees))
            {
                sampleInput.ForeColor = Color.Black;
                try
                {
                    DoPreview(decimalDegrees);
                }
                catch
                {
                    sampleInput.ForeColor = Color.Red;
                    sampleOutput.Text = "Out of range";
                }
            }
            else
            {
                sampleInput.ForeColor = Color.Red;
                sampleOutput.Text = "N/A";
            }

        }

        #endregion

    }

}
