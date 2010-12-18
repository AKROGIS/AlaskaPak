namespace NPS.AKRO.ArcGIS.Forms
{
    partial class RandomFeatureSelectionForm
    {
        /// <summary>
        /// Required designer variable.
        /// </summary>
        private System.ComponentModel.IContainer components = null;

        /// <summary>
        /// Clean up any resources being used.
        /// </summary>
        /// <param name="disposing">true if managed resources should be disposed; otherwise, false.</param>
        protected override void Dispose(bool disposing)
        {
            if (disposing && (components != null))
            {
                components.Dispose();
            }
            base.Dispose(disposing);
        }

        #region Windows Form Designer generated code

        /// <summary>
        /// Required method for Designer support - do not modify
        /// the contents of this method with the code editor.
        /// </summary>
        private void InitializeComponent()
        {
            this.layerComboBox = new System.Windows.Forms.ComboBox();
            this.layerLabel = new System.Windows.Forms.Label();
            this.selectionMethodGroupBox = new System.Windows.Forms.GroupBox();
            this.descriptionTextBox = new System.Windows.Forms.TextBox();
            this.numberTextBox = new System.Windows.Forms.TextBox();
            this.percentTextBox = new System.Windows.Forms.TextBox();
            this.numberRadioButton = new System.Windows.Forms.RadioButton();
            this.percentRadioButton = new System.Windows.Forms.RadioButton();
            this.cancelButton = new System.Windows.Forms.Button();
            this.selectButton = new System.Windows.Forms.Button();
            this.selectionMethodGroupBox.SuspendLayout();
            this.SuspendLayout();
            // 
            // layerComboBox
            // 
            this.layerComboBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.layerComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.layerComboBox.FormattingEnabled = true;
            this.layerComboBox.Location = new System.Drawing.Point(98, 14);
            this.layerComboBox.Name = "layerComboBox";
            this.layerComboBox.Size = new System.Drawing.Size(249, 23);
            this.layerComboBox.TabIndex = 0;
            // 
            // layerLabel
            // 
            this.layerLabel.AutoSize = true;
            this.layerLabel.Location = new System.Drawing.Point(12, 17);
            this.layerLabel.Name = "layerLabel";
            this.layerLabel.Size = new System.Drawing.Size(80, 15);
            this.layerLabel.TabIndex = 1;
            this.layerLabel.Text = "Feature Layer:";
            // 
            // selectionMethodGroupBox
            // 
            this.selectionMethodGroupBox.Controls.Add(this.descriptionTextBox);
            this.selectionMethodGroupBox.Controls.Add(this.numberTextBox);
            this.selectionMethodGroupBox.Controls.Add(this.percentTextBox);
            this.selectionMethodGroupBox.Controls.Add(this.numberRadioButton);
            this.selectionMethodGroupBox.Controls.Add(this.percentRadioButton);
            this.selectionMethodGroupBox.Location = new System.Drawing.Point(12, 43);
            this.selectionMethodGroupBox.Name = "selectionMethodGroupBox";
            this.selectionMethodGroupBox.Size = new System.Drawing.Size(147, 126);
            this.selectionMethodGroupBox.TabIndex = 2;
            this.selectionMethodGroupBox.TabStop = false;
            this.selectionMethodGroupBox.Text = "Selection Method";
            // 
            // descriptionTextBox
            // 
            this.descriptionTextBox.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
                        | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.descriptionTextBox.BackColor = System.Drawing.SystemColors.Info;
            this.descriptionTextBox.BorderStyle = System.Windows.Forms.BorderStyle.FixedSingle;
            this.descriptionTextBox.ForeColor = System.Drawing.SystemColors.InfoText;
            this.descriptionTextBox.Location = new System.Drawing.Point(7, 75);
            this.descriptionTextBox.Multiline = true;
            this.descriptionTextBox.Name = "descriptionTextBox";
            this.descriptionTextBox.ReadOnly = true;
            this.descriptionTextBox.Size = new System.Drawing.Size(131, 43);
            this.descriptionTextBox.TabIndex = 4;
            this.descriptionTextBox.TabStop = false;
            // 
            // numberTextBox
            // 
            this.numberTextBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.numberTextBox.Enabled = false;
            this.numberTextBox.Location = new System.Drawing.Point(93, 46);
            this.numberTextBox.Name = "numberTextBox";
            this.numberTextBox.Size = new System.Drawing.Size(45, 23);
            this.numberTextBox.TabIndex = 3;
            this.numberTextBox.Text = "1";
            this.numberTextBox.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.numberTextBox.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.textBox_KeyPress);
            this.numberTextBox.Validating += new System.ComponentModel.CancelEventHandler(this.numberTextBox_Validating);
            this.numberTextBox.Validated += new System.EventHandler(this.textBox_Validated);
            // 
            // percentTextBox
            // 
            this.percentTextBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.percentTextBox.Location = new System.Drawing.Point(93, 21);
            this.percentTextBox.Name = "percentTextBox";
            this.percentTextBox.Size = new System.Drawing.Size(45, 23);
            this.percentTextBox.TabIndex = 2;
            this.percentTextBox.Text = "75";
            this.percentTextBox.TextAlign = System.Windows.Forms.HorizontalAlignment.Right;
            this.percentTextBox.KeyPress += new System.Windows.Forms.KeyPressEventHandler(this.textBox_KeyPress);
            this.percentTextBox.Validating += new System.ComponentModel.CancelEventHandler(this.percentTextBox_Validating);
            this.percentTextBox.Validated += new System.EventHandler(this.textBox_Validated);
            // 
            // numberRadioButton
            // 
            this.numberRadioButton.AutoSize = true;
            this.numberRadioButton.Location = new System.Drawing.Point(6, 47);
            this.numberRadioButton.Name = "numberRadioButton";
            this.numberRadioButton.Size = new System.Drawing.Size(62, 17);
            this.numberRadioButton.TabIndex = 1;
            this.numberRadioButton.Text = "Number";
            this.numberRadioButton.UseVisualStyleBackColor = true;
            // 
            // percentRadioButton
            // 
            this.percentRadioButton.AutoSize = true;
            this.percentRadioButton.Checked = true;
            this.percentRadioButton.Location = new System.Drawing.Point(6, 22);
            this.percentRadioButton.Name = "percentRadioButton";
            this.percentRadioButton.Size = new System.Drawing.Size(80, 17);
            this.percentRadioButton.TabIndex = 0;
            this.percentRadioButton.TabStop = true;
            this.percentRadioButton.Text = "Percentage";
            this.percentRadioButton.UseVisualStyleBackColor = true;
            this.percentRadioButton.CheckedChanged += new System.EventHandler(this.percentRadioButton_CheckedChanged);
            // 
            // cancelButton
            // 
            this.cancelButton.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.cancelButton.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.cancelButton.Location = new System.Drawing.Point(272, 181);
            this.cancelButton.Name = "cancelButton";
            this.cancelButton.Size = new System.Drawing.Size(75, 23);
            this.cancelButton.TabIndex = 3;
            this.cancelButton.Text = "Cancel";
            this.cancelButton.UseVisualStyleBackColor = true;
            this.cancelButton.Click += new System.EventHandler(this.cancelButton_Click);
            // 
            // selectButton
            // 
            this.selectButton.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.selectButton.Location = new System.Drawing.Point(191, 181);
            this.selectButton.Name = "selectButton";
            this.selectButton.Size = new System.Drawing.Size(75, 23);
            this.selectButton.TabIndex = 4;
            this.selectButton.Text = "Select";
            this.selectButton.UseVisualStyleBackColor = true;
            this.selectButton.Click += new System.EventHandler(this.selectButton_Click);
            // 
            // RandomFeatureSelectionForm
            // 
            this.AcceptButton = this.selectButton;
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.cancelButton;
            this.ClientSize = new System.Drawing.Size(359, 216);
            this.Controls.Add(this.selectButton);
            this.Controls.Add(this.cancelButton);
            this.Controls.Add(this.selectionMethodGroupBox);
            this.Controls.Add(this.layerLabel);
            this.Controls.Add(this.layerComboBox);
            this.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.FormBorderStyle = System.Windows.Forms.FormBorderStyle.SizableToolWindow;
            this.MinimumSize = new System.Drawing.Size(375, 250);
            this.Name = "RandomFeatureSelectionForm";
            this.Text = "Random Feature Selection";
            this.selectionMethodGroupBox.ResumeLayout(false);
            this.selectionMethodGroupBox.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ComboBox layerComboBox;
        private System.Windows.Forms.Label layerLabel;
        private System.Windows.Forms.GroupBox selectionMethodGroupBox;
        private System.Windows.Forms.TextBox descriptionTextBox;
        private System.Windows.Forms.TextBox numberTextBox;
        private System.Windows.Forms.TextBox percentTextBox;
        private System.Windows.Forms.RadioButton numberRadioButton;
        private System.Windows.Forms.RadioButton percentRadioButton;
        private System.Windows.Forms.Button cancelButton;
        private System.Windows.Forms.Button selectButton;
    }
}