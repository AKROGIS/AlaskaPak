namespace NPS.AKRO.ArcGIS.Forms
{
    partial class AddXyForm
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
            this.components = new System.ComponentModel.Container();
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(AddXyForm));
            this.formatStyleComboBox = new System.Windows.Forms.ComboBox();
            this.sampleInput = new System.Windows.Forms.TextBox();
            this.showTrailingZerosCheckBox = new System.Windows.Forms.CheckBox();
            this.showDirectionCheckBox = new System.Windows.Forms.CheckBox();
            this.isLatitudeCheckBox = new System.Windows.Forms.CheckBox();
            this.showSpacesCheckBox = new System.Windows.Forms.CheckBox();
            this.numericUpDown1 = new System.Windows.Forms.NumericUpDown();
            this.label1 = new System.Windows.Forms.Label();
            this.sampleOutput = new System.Windows.Forms.TextBox();
            this.cancelButton = new System.Windows.Forms.Button();
            this.formattingOptionsButton = new System.Windows.Forms.Button();
            this.imageList1 = new System.Windows.Forms.ImageList(this.components);
            this.panel1 = new System.Windows.Forms.Panel();
            this.label2 = new System.Windows.Forms.Label();
            this.okButton = new System.Windows.Forms.Button();
            this.xFieldComboBox = new System.Windows.Forms.ComboBox();
            this.yFieldComboBox = new System.Windows.Forms.ComboBox();
            this.browseButton = new System.Windows.Forms.Button();
            this.featureClassComboBox = new System.Windows.Forms.ComboBox();
            this.label3 = new System.Windows.Forms.Label();
            this.label4 = new System.Windows.Forms.Label();
            this.label5 = new System.Windows.Forms.Label();
            this.label6 = new System.Windows.Forms.Label();
            this.overwriteWarning = new System.Windows.Forms.ErrorProvider(this.components);
            this.invalidEntry = new System.Windows.Forms.ErrorProvider(this.components);
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown1)).BeginInit();
            this.panel1.SuspendLayout();
            ((System.ComponentModel.ISupportInitialize)(this.overwriteWarning)).BeginInit();
            ((System.ComponentModel.ISupportInitialize)(this.invalidEntry)).BeginInit();
            this.SuspendLayout();
            // 
            // formatStyleComboBox
            // 
            this.formatStyleComboBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.formatStyleComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.formatStyleComboBox.FormattingEnabled = true;
            this.formatStyleComboBox.Location = new System.Drawing.Point(166, 114);
            this.formatStyleComboBox.Name = "formatStyleComboBox";
            this.formatStyleComboBox.Size = new System.Drawing.Size(239, 23);
            this.formatStyleComboBox.TabIndex = 0;
            this.formatStyleComboBox.SelectedIndexChanged += new System.EventHandler(this.formatStyleComboBox_SelectedIndexChanged);
            // 
            // sampleInput
            // 
            this.sampleInput.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.sampleInput.Location = new System.Drawing.Point(231, 32);
            this.sampleInput.Name = "sampleInput";
            this.sampleInput.Size = new System.Drawing.Size(90, 23);
            this.sampleInput.TabIndex = 1;
            this.sampleInput.Text = "-35.012345";
            this.sampleInput.TextChanged += new System.EventHandler(this.input_TextChanged);
            // 
            // showTrailingZerosCheckBox
            // 
            this.showTrailingZerosCheckBox.AutoSize = true;
            this.showTrailingZerosCheckBox.Location = new System.Drawing.Point(11, 86);
            this.showTrailingZerosCheckBox.Name = "showTrailingZerosCheckBox";
            this.showTrailingZerosCheckBox.Size = new System.Drawing.Size(174, 19);
            this.showTrailingZerosCheckBox.TabIndex = 2;
            this.showTrailingZerosCheckBox.Text = "Show zero minutes/seconds";
            this.showTrailingZerosCheckBox.UseVisualStyleBackColor = true;
            this.showTrailingZerosCheckBox.CheckedChanged += new System.EventHandler(this.checkBox_CheckedChanged);
            // 
            // showDirectionCheckBox
            // 
            this.showDirectionCheckBox.AutoSize = true;
            this.showDirectionCheckBox.Checked = true;
            this.showDirectionCheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.showDirectionCheckBox.Location = new System.Drawing.Point(11, 61);
            this.showDirectionCheckBox.Name = "showDirectionCheckBox";
            this.showDirectionCheckBox.Size = new System.Drawing.Size(157, 19);
            this.showDirectionCheckBox.TabIndex = 3;
            this.showDirectionCheckBox.Text = "Show direction (N,S,E,W)";
            this.showDirectionCheckBox.UseVisualStyleBackColor = true;
            this.showDirectionCheckBox.CheckedChanged += new System.EventHandler(this.ShowDirectionCheckBox_CheckedChanged);
            // 
            // isLatitudeCheckBox
            // 
            this.isLatitudeCheckBox.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.isLatitudeCheckBox.AutoSize = true;
            this.isLatitudeCheckBox.Location = new System.Drawing.Point(231, 61);
            this.isLatitudeCheckBox.Name = "isLatitudeCheckBox";
            this.isLatitudeCheckBox.Size = new System.Drawing.Size(85, 19);
            this.isLatitudeCheckBox.TabIndex = 8;
            this.isLatitudeCheckBox.Text = "As Latitude";
            this.isLatitudeCheckBox.UseVisualStyleBackColor = true;
            this.isLatitudeCheckBox.CheckedChanged += new System.EventHandler(this.isLatitudeCheckBox_CheckedChanged);
            // 
            // showSpacesCheckBox
            // 
            this.showSpacesCheckBox.AutoSize = true;
            this.showSpacesCheckBox.Checked = true;
            this.showSpacesCheckBox.CheckState = System.Windows.Forms.CheckState.Checked;
            this.showSpacesCheckBox.Location = new System.Drawing.Point(11, 38);
            this.showSpacesCheckBox.Name = "showSpacesCheckBox";
            this.showSpacesCheckBox.Size = new System.Drawing.Size(170, 19);
            this.showSpacesCheckBox.TabIndex = 7;
            this.showSpacesCheckBox.Text = "Show spaces between parts";
            this.showSpacesCheckBox.UseVisualStyleBackColor = true;
            this.showSpacesCheckBox.CheckedChanged += new System.EventHandler(this.checkBox_CheckedChanged);
            // 
            // numericUpDown1
            // 
            this.numericUpDown1.Location = new System.Drawing.Point(10, 12);
            this.numericUpDown1.Maximum = new decimal(new int[] {
            9,
            0,
            0,
            0});
            this.numericUpDown1.Name = "numericUpDown1";
            this.numericUpDown1.Size = new System.Drawing.Size(31, 23);
            this.numericUpDown1.TabIndex = 6;
            this.numericUpDown1.TextAlign = System.Windows.Forms.HorizontalAlignment.Center;
            this.numericUpDown1.Value = new decimal(new int[] {
            2,
            0,
            0,
            0});
            this.numericUpDown1.ValueChanged += new System.EventHandler(this.numericUpDown1_ValueChanged);
            // 
            // label1
            // 
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(47, 14);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(129, 15);
            this.label1.TabIndex = 5;
            this.label1.Text = "Digits after the decimal";
            // 
            // sampleOutput
            // 
            this.sampleOutput.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.sampleOutput.Location = new System.Drawing.Point(231, 86);
            this.sampleOutput.Name = "sampleOutput";
            this.sampleOutput.ReadOnly = true;
            this.sampleOutput.Size = new System.Drawing.Size(122, 23);
            this.sampleOutput.TabIndex = 5;
            // 
            // cancelButton
            // 
            this.cancelButton.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.cancelButton.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.cancelButton.Location = new System.Drawing.Point(349, 167);
            this.cancelButton.Name = "cancelButton";
            this.cancelButton.Size = new System.Drawing.Size(62, 23);
            this.cancelButton.TabIndex = 6;
            this.cancelButton.Text = "Cancel";
            this.cancelButton.UseVisualStyleBackColor = true;
            this.cancelButton.Click += new System.EventHandler(this.cancelButton_Click);
            // 
            // formattingOptionsButton
            // 
            this.formattingOptionsButton.FlatAppearance.BorderColor = System.Drawing.SystemColors.Control;
            this.formattingOptionsButton.FlatAppearance.BorderSize = 0;
            this.formattingOptionsButton.FlatAppearance.MouseDownBackColor = System.Drawing.SystemColors.Control;
            this.formattingOptionsButton.FlatAppearance.MouseOverBackColor = System.Drawing.SystemColors.Control;
            this.formattingOptionsButton.FlatStyle = System.Windows.Forms.FlatStyle.Flat;
            this.formattingOptionsButton.ImageAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.formattingOptionsButton.ImageIndex = 1;
            this.formattingOptionsButton.ImageList = this.imageList1;
            this.formattingOptionsButton.Location = new System.Drawing.Point(9, 145);
            this.formattingOptionsButton.Name = "formattingOptionsButton";
            this.formattingOptionsButton.Size = new System.Drawing.Size(143, 23);
            this.formattingOptionsButton.TabIndex = 7;
            this.formattingOptionsButton.Text = "Formatting options";
            this.formattingOptionsButton.TextAlign = System.Drawing.ContentAlignment.MiddleLeft;
            this.formattingOptionsButton.TextImageRelation = System.Windows.Forms.TextImageRelation.ImageBeforeText;
            this.formattingOptionsButton.UseVisualStyleBackColor = true;
            this.formattingOptionsButton.Click += new System.EventHandler(this.formattingOptionsButton_Click);
            // 
            // imageList1
            // 
            this.imageList1.ImageStream = ((System.Windows.Forms.ImageListStreamer)(resources.GetObject("imageList1.ImageStream")));
            this.imageList1.TransparentColor = System.Drawing.Color.Fuchsia;
            this.imageList1.Images.SetKeyName(0, "Collapse_small.bmp");
            this.imageList1.Images.SetKeyName(1, "Expand_small.bmp");
            // 
            // panel1
            // 
            this.panel1.Controls.Add(this.label2);
            this.panel1.Controls.Add(this.isLatitudeCheckBox);
            this.panel1.Controls.Add(this.showDirectionCheckBox);
            this.panel1.Controls.Add(this.showSpacesCheckBox);
            this.panel1.Controls.Add(this.showTrailingZerosCheckBox);
            this.panel1.Controls.Add(this.sampleOutput);
            this.panel1.Controls.Add(this.sampleInput);
            this.panel1.Controls.Add(this.numericUpDown1);
            this.panel1.Controls.Add(this.label1);
            this.panel1.Location = new System.Drawing.Point(25, 167);
            this.panel1.Name = "panel1";
            this.panel1.Size = new System.Drawing.Size(356, 117);
            this.panel1.TabIndex = 8;
            this.panel1.Visible = false;
            // 
            // label2
            // 
            this.label2.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(228, 14);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(60, 15);
            this.label2.TabIndex = 9;
            this.label2.Text = "Test value";
            // 
            // okButton
            // 
            this.okButton.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.okButton.Enabled = false;
            this.okButton.Location = new System.Drawing.Point(281, 167);
            this.okButton.Name = "okButton";
            this.okButton.Size = new System.Drawing.Size(62, 23);
            this.okButton.TabIndex = 9;
            this.okButton.Text = "Ok";
            this.okButton.UseVisualStyleBackColor = true;
            this.okButton.Click += new System.EventHandler(this.okButton_Click);
            // 
            // xFieldComboBox
            // 
            this.xFieldComboBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.xFieldComboBox.FormattingEnabled = true;
            this.xFieldComboBox.Location = new System.Drawing.Point(166, 56);
            this.xFieldComboBox.Name = "xFieldComboBox";
            this.xFieldComboBox.Size = new System.Drawing.Size(162, 23);
            this.xFieldComboBox.TabIndex = 11;
            this.xFieldComboBox.SelectedIndexChanged += new System.EventHandler(this.fieldNameComboBox_SelectedIndexChanged);
            this.xFieldComboBox.TextUpdate += new System.EventHandler(this.fieldNameComboBox_TextChanged);
            this.xFieldComboBox.TextChanged += new System.EventHandler(this.fieldNameComboBox_TextChanged);
            // 
            // yFieldComboBox
            // 
            this.yFieldComboBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.yFieldComboBox.FormattingEnabled = true;
            this.yFieldComboBox.Location = new System.Drawing.Point(166, 85);
            this.yFieldComboBox.Name = "yFieldComboBox";
            this.yFieldComboBox.Size = new System.Drawing.Size(162, 23);
            this.yFieldComboBox.TabIndex = 12;
            this.yFieldComboBox.SelectedIndexChanged += new System.EventHandler(this.fieldNameComboBox_SelectedIndexChanged);
            this.yFieldComboBox.TextUpdate += new System.EventHandler(this.fieldNameComboBox_TextChanged);
            this.yFieldComboBox.TextChanged += new System.EventHandler(this.fieldNameComboBox_TextChanged);
            // 
            // browseButton
            // 
            this.browseButton.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Right)));
            this.browseButton.Enabled = false;
            this.browseButton.Location = new System.Drawing.Point(334, 26);
            this.browseButton.Name = "browseButton";
            this.browseButton.Size = new System.Drawing.Size(75, 23);
            this.browseButton.TabIndex = 13;
            this.browseButton.Text = "Browse...";
            this.browseButton.UseVisualStyleBackColor = true;
            this.browseButton.Click += new System.EventHandler(this.browseButton_Click);
            // 
            // featureClassComboBox
            // 
            this.featureClassComboBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Left) 
            | System.Windows.Forms.AnchorStyles.Right)));
            this.featureClassComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.featureClassComboBox.FormattingEnabled = true;
            this.featureClassComboBox.Location = new System.Drawing.Point(12, 27);
            this.featureClassComboBox.Name = "featureClassComboBox";
            this.featureClassComboBox.Size = new System.Drawing.Size(316, 23);
            this.featureClassComboBox.TabIndex = 14;
            this.featureClassComboBox.SelectedIndexChanged += new System.EventHandler(this.featureClassComboBox_SelectedIndexChanged);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(12, 9);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(106, 15);
            this.label3.TabIndex = 15;
            this.label3.Text = "Point feature class:";
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(12, 59);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(138, 15);
            this.label4.TabIndex = 16;
            this.label4.Text = "X (Longitude) field name";
            // 
            // label5
            // 
            this.label5.AutoSize = true;
            this.label5.Location = new System.Drawing.Point(12, 88);
            this.label5.Name = "label5";
            this.label5.Size = new System.Drawing.Size(127, 15);
            this.label5.TabIndex = 17;
            this.label5.Text = "Y (Latitude) field name";
            // 
            // label6
            // 
            this.label6.AutoSize = true;
            this.label6.Location = new System.Drawing.Point(12, 117);
            this.label6.Name = "label6";
            this.label6.Size = new System.Drawing.Size(108, 15);
            this.label6.TabIndex = 18;
            this.label6.Text = "Coordinate format:";
            // 
            // overwriteWarning
            // 
            this.overwriteWarning.BlinkStyle = System.Windows.Forms.ErrorBlinkStyle.NeverBlink;
            this.overwriteWarning.ContainerControl = this;
            this.overwriteWarning.Icon = ((System.Drawing.Icon)(resources.GetObject("overwriteWarning.Icon")));
            // 
            // invalidEntry
            // 
            this.invalidEntry.ContainerControl = this;
            // 
            // AddXYForm
            // 
            this.AcceptButton = this.okButton;
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.cancelButton;
            this.ClientSize = new System.Drawing.Size(419, 202);
            this.Controls.Add(this.label6);
            this.Controls.Add(this.label5);
            this.Controls.Add(this.label4);
            this.Controls.Add(this.featureClassComboBox);
            this.Controls.Add(this.browseButton);
            this.Controls.Add(this.yFieldComboBox);
            this.Controls.Add(this.xFieldComboBox);
            this.Controls.Add(this.cancelButton);
            this.Controls.Add(this.okButton);
            this.Controls.Add(this.formattingOptionsButton);
            this.Controls.Add(this.formatStyleComboBox);
            this.Controls.Add(this.panel1);
            this.Controls.Add(this.label3);
            this.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.MaximumSize = new System.Drawing.Size(800, 240);
            this.MinimumSize = new System.Drawing.Size(400, 240);
            this.Name = "AddXyForm";
            this.Text = "Add Coordinates";
            ((System.ComponentModel.ISupportInitialize)(this.numericUpDown1)).EndInit();
            this.panel1.ResumeLayout(false);
            this.panel1.PerformLayout();
            ((System.ComponentModel.ISupportInitialize)(this.overwriteWarning)).EndInit();
            ((System.ComponentModel.ISupportInitialize)(this.invalidEntry)).EndInit();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.ComboBox formatStyleComboBox;
        private System.Windows.Forms.TextBox sampleInput;
        private System.Windows.Forms.CheckBox showTrailingZerosCheckBox;
        private System.Windows.Forms.CheckBox showDirectionCheckBox;
        private System.Windows.Forms.NumericUpDown numericUpDown1;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.CheckBox showSpacesCheckBox;
        private System.Windows.Forms.TextBox sampleOutput;
        private System.Windows.Forms.Button cancelButton;
        private System.Windows.Forms.CheckBox isLatitudeCheckBox;
        private System.Windows.Forms.Button formattingOptionsButton;
        private System.Windows.Forms.ImageList imageList1;
        private System.Windows.Forms.Panel panel1;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.ComboBox xFieldComboBox;
        private System.Windows.Forms.ComboBox yFieldComboBox;
        private System.Windows.Forms.Button browseButton;
        private System.Windows.Forms.ComboBox featureClassComboBox;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label5;
        private System.Windows.Forms.Label label6;
        private System.Windows.Forms.ErrorProvider overwriteWarning;
        private System.Windows.Forms.ErrorProvider invalidEntry;
        internal System.Windows.Forms.Button okButton;
    }
}