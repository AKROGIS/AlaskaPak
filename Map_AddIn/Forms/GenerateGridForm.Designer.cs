namespace NPS.AKRO.ArcGIS.Forms
{
    partial class GenerateGridForm
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
            System.ComponentModel.ComponentResourceManager resources = new System.ComponentModel.ComponentResourceManager(typeof(GenerateGridForm));
            this.tabControl1 = new System.Windows.Forms.TabControl();
            this.tabPage2 = new System.Windows.Forms.TabPage();
            this.label2 = new System.Windows.Forms.Label();
            this.quantityBox = new System.Windows.Forms.GroupBox();
            this.yCountTextBox = new System.Windows.Forms.TextBox();
            this.xCountTextBox = new System.Windows.Forms.TextBox();
            this.label11 = new System.Windows.Forms.Label();
            this.label10 = new System.Windows.Forms.Label();
            this.sizeBox = new System.Windows.Forms.GroupBox();
            this.widthTextBox = new System.Windows.Forms.TextBox();
            this.label3 = new System.Windows.Forms.Label();
            this.label9 = new System.Windows.Forms.Label();
            this.heightTextBox = new System.Windows.Forms.TextBox();
            this.unitsComboBox = new System.Windows.Forms.ComboBox();
            this.label4 = new System.Windows.Forms.Label();
            this.browseSpatialRefButton = new System.Windows.Forms.Button();
            this.spatialReferenceTextBox = new System.Windows.Forms.TextBox();
            this.label12 = new System.Windows.Forms.Label();
            this.tabPage3 = new System.Windows.Forms.TabPage();
            this.label20 = new System.Windows.Forms.Label();
            this.pageNumberComboBox = new System.Windows.Forms.ComboBox();
            this.delimiterTextBox = new System.Windows.Forms.TextBox();
            this.conventionComboBox = new System.Windows.Forms.ComboBox();
            this.columnStyleComboBox = new System.Windows.Forms.ComboBox();
            this.suffixTextBox = new System.Windows.Forms.TextBox();
            this.label18 = new System.Windows.Forms.Label();
            this.label17 = new System.Windows.Forms.Label();
            this.label16 = new System.Windows.Forms.Label();
            this.label15 = new System.Windows.Forms.Label();
            this.label14 = new System.Windows.Forms.Label();
            this.label13 = new System.Windows.Forms.Label();
            this.rowStyleComboBox = new System.Windows.Forms.ComboBox();
            this.prefixTextBox = new System.Windows.Forms.TextBox();
            this.applyButton = new System.Windows.Forms.Button();
            this.cancelButton = new System.Windows.Forms.Button();
            this.outputPathTextBox = new System.Windows.Forms.TextBox();
            this.label1 = new System.Windows.Forms.Label();
            this.browseButton = new System.Windows.Forms.Button();
            this.saveButton = new System.Windows.Forms.Button();
            this.toolTip1 = new System.Windows.Forms.ToolTip(this.components);
            this.tabControl1.SuspendLayout();
            this.tabPage2.SuspendLayout();
            this.quantityBox.SuspendLayout();
            this.sizeBox.SuspendLayout();
            this.tabPage3.SuspendLayout();
            this.SuspendLayout();
            // 
            // tabControl1
            // 
            this.tabControl1.Anchor = ((System.Windows.Forms.AnchorStyles)((((System.Windows.Forms.AnchorStyles.Top | System.Windows.Forms.AnchorStyles.Bottom)
                        | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.tabControl1.Controls.Add(this.tabPage2);
            this.tabControl1.Controls.Add(this.tabPage3);
            this.tabControl1.Location = new System.Drawing.Point(15, 11);
            this.tabControl1.Name = "tabControl1";
            this.tabControl1.SelectedIndex = 0;
            this.tabControl1.Size = new System.Drawing.Size(456, 365);
            this.tabControl1.TabIndex = 9;
            // 
            // tabPage2
            // 
            this.tabPage2.Controls.Add(this.label2);
            this.tabPage2.Controls.Add(this.quantityBox);
            this.tabPage2.Controls.Add(this.sizeBox);
            this.tabPage2.Location = new System.Drawing.Point(4, 24);
            this.tabPage2.Name = "tabPage2";
            this.tabPage2.Padding = new System.Windows.Forms.Padding(3);
            this.tabPage2.Size = new System.Drawing.Size(448, 337);
            this.tabPage2.TabIndex = 1;
            this.tabPage2.Text = "Spacing";
            this.tabPage2.UseVisualStyleBackColor = true;
            // 
            // label2
            // 
            this.label2.AutoSize = true;
            this.label2.Location = new System.Drawing.Point(6, 220);
            this.label2.Name = "label2";
            this.label2.Size = new System.Drawing.Size(440, 105);
            this.label2.TabIndex = 16;
            this.label2.Text = resources.GetString("label2.Text");
            // 
            // quantityBox
            // 
            this.quantityBox.Controls.Add(this.yCountTextBox);
            this.quantityBox.Controls.Add(this.xCountTextBox);
            this.quantityBox.Controls.Add(this.label11);
            this.quantityBox.Controls.Add(this.label10);
            this.quantityBox.Location = new System.Drawing.Point(6, 130);
            this.quantityBox.Name = "quantityBox";
            this.quantityBox.Size = new System.Drawing.Size(356, 87);
            this.quantityBox.TabIndex = 15;
            this.quantityBox.TabStop = false;
            this.quantityBox.Text = "Number of Cells";
            // 
            // yCountTextBox
            // 
            this.yCountTextBox.Location = new System.Drawing.Point(89, 52);
            this.yCountTextBox.Name = "yCountTextBox";
            this.yCountTextBox.Size = new System.Drawing.Size(95, 23);
            this.yCountTextBox.TabIndex = 11;
            this.yCountTextBox.TextChanged += new System.EventHandler(this.IntegerTextBox_TextChanged);
            this.yCountTextBox.Leave += new System.EventHandler(this.CountTextBox_Leave);
            // 
            // xCountTextBox
            // 
            this.xCountTextBox.Location = new System.Drawing.Point(89, 22);
            this.xCountTextBox.Name = "xCountTextBox";
            this.xCountTextBox.Size = new System.Drawing.Size(95, 23);
            this.xCountTextBox.TabIndex = 10;
            this.xCountTextBox.TextChanged += new System.EventHandler(this.IntegerTextBox_TextChanged);
            this.xCountTextBox.Leave += new System.EventHandler(this.CountTextBox_Leave);
            // 
            // label11
            // 
            this.label11.AutoSize = true;
            this.label11.Location = new System.Drawing.Point(9, 55);
            this.label11.Name = "label11";
            this.label11.Size = new System.Drawing.Size(58, 15);
            this.label11.TabIndex = 13;
            this.label11.Text = "Vertically:";
            // 
            // label10
            // 
            this.label10.AutoSize = true;
            this.label10.Location = new System.Drawing.Point(9, 25);
            this.label10.Name = "label10";
            this.label10.Size = new System.Drawing.Size(74, 15);
            this.label10.TabIndex = 12;
            this.label10.Text = "Horizontally:";
            // 
            // sizeBox
            // 
            this.sizeBox.Controls.Add(this.widthTextBox);
            this.sizeBox.Controls.Add(this.label3);
            this.sizeBox.Controls.Add(this.label9);
            this.sizeBox.Controls.Add(this.heightTextBox);
            this.sizeBox.Controls.Add(this.unitsComboBox);
            this.sizeBox.Controls.Add(this.label4);
            this.sizeBox.Location = new System.Drawing.Point(6, 6);
            this.sizeBox.Name = "sizeBox";
            this.sizeBox.Size = new System.Drawing.Size(307, 118);
            this.sizeBox.TabIndex = 14;
            this.sizeBox.TabStop = false;
            this.sizeBox.Text = "Cell Size";
            // 
            // widthTextBox
            // 
            this.widthTextBox.Location = new System.Drawing.Point(89, 21);
            this.widthTextBox.Name = "widthTextBox";
            this.widthTextBox.Size = new System.Drawing.Size(95, 23);
            this.widthTextBox.TabIndex = 5;
            this.widthTextBox.TextChanged += new System.EventHandler(this.DoubleTextBox_TextChanged);
            this.widthTextBox.Leave += new System.EventHandler(this.SizeTextBox_Leave);
            // 
            // label3
            // 
            this.label3.AutoSize = true;
            this.label3.Location = new System.Drawing.Point(9, 24);
            this.label3.Name = "label3";
            this.label3.Size = new System.Drawing.Size(42, 15);
            this.label3.TabIndex = 4;
            this.label3.Text = "Width:";
            // 
            // label9
            // 
            this.label9.AutoSize = true;
            this.label9.Location = new System.Drawing.Point(9, 83);
            this.label9.Name = "label9";
            this.label9.Size = new System.Drawing.Size(37, 15);
            this.label9.TabIndex = 9;
            this.label9.Text = "Units:";
            // 
            // heightTextBox
            // 
            this.heightTextBox.Location = new System.Drawing.Point(89, 51);
            this.heightTextBox.Name = "heightTextBox";
            this.heightTextBox.Size = new System.Drawing.Size(95, 23);
            this.heightTextBox.TabIndex = 6;
            this.heightTextBox.TextChanged += new System.EventHandler(this.DoubleTextBox_TextChanged);
            this.heightTextBox.Leave += new System.EventHandler(this.SizeTextBox_Leave);
            // 
            // unitsComboBox
            // 
            this.unitsComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.unitsComboBox.FormattingEnabled = true;
            this.unitsComboBox.Location = new System.Drawing.Point(89, 80);
            this.unitsComboBox.Name = "unitsComboBox";
            this.unitsComboBox.Size = new System.Drawing.Size(212, 23);
            this.unitsComboBox.TabIndex = 8;
            this.toolTip1.SetToolTip(this.unitsComboBox, "Must be map units for now.");
            this.unitsComboBox.SelectedIndexChanged += new System.EventHandler(this.unitsComboBox_SelectedIndexChanged);
            // 
            // label4
            // 
            this.label4.AutoSize = true;
            this.label4.Location = new System.Drawing.Point(9, 54);
            this.label4.Name = "label4";
            this.label4.Size = new System.Drawing.Size(46, 15);
            this.label4.TabIndex = 7;
            this.label4.Text = "Height:";
            // 
            // browseSpatialRefButton
            // 
            this.browseSpatialRefButton.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.browseSpatialRefButton.Enabled = false;
            this.browseSpatialRefButton.Location = new System.Drawing.Point(448, 453);
            this.browseSpatialRefButton.Name = "browseSpatialRefButton";
            this.browseSpatialRefButton.Size = new System.Drawing.Size(23, 23);
            this.browseSpatialRefButton.TabIndex = 20;
            this.browseSpatialRefButton.Text = "...";
            this.toolTip1.SetToolTip(this.browseSpatialRefButton, "Feature not enabled yet");
            this.browseSpatialRefButton.UseVisualStyleBackColor = true;
            // 
            // spatialReferenceTextBox
            // 
            this.spatialReferenceTextBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.spatialReferenceTextBox.Location = new System.Drawing.Point(15, 454);
            this.spatialReferenceTextBox.Name = "spatialReferenceTextBox";
            this.spatialReferenceTextBox.ReadOnly = true;
            this.spatialReferenceTextBox.Size = new System.Drawing.Size(430, 23);
            this.spatialReferenceTextBox.TabIndex = 19;
            this.spatialReferenceTextBox.Text = "Unknown";
            // 
            // label12
            // 
            this.label12.AutoSize = true;
            this.label12.Location = new System.Drawing.Point(16, 436);
            this.label12.Name = "label12";
            this.label12.Size = new System.Drawing.Size(100, 15);
            this.label12.TabIndex = 18;
            this.label12.Text = "Spatial Reference:";
            // 
            // tabPage3
            // 
            this.tabPage3.Controls.Add(this.label20);
            this.tabPage3.Controls.Add(this.pageNumberComboBox);
            this.tabPage3.Controls.Add(this.delimiterTextBox);
            this.tabPage3.Controls.Add(this.conventionComboBox);
            this.tabPage3.Controls.Add(this.columnStyleComboBox);
            this.tabPage3.Controls.Add(this.suffixTextBox);
            this.tabPage3.Controls.Add(this.label18);
            this.tabPage3.Controls.Add(this.label17);
            this.tabPage3.Controls.Add(this.label16);
            this.tabPage3.Controls.Add(this.label15);
            this.tabPage3.Controls.Add(this.label14);
            this.tabPage3.Controls.Add(this.label13);
            this.tabPage3.Controls.Add(this.rowStyleComboBox);
            this.tabPage3.Controls.Add(this.prefixTextBox);
            this.tabPage3.Location = new System.Drawing.Point(4, 24);
            this.tabPage3.Name = "tabPage3";
            this.tabPage3.Size = new System.Drawing.Size(448, 337);
            this.tabPage3.TabIndex = 2;
            this.tabPage3.Text = "Labels";
            this.tabPage3.UseVisualStyleBackColor = true;
            // 
            // label20
            // 
            this.label20.AutoSize = true;
            this.label20.Location = new System.Drawing.Point(3, 183);
            this.label20.Name = "label20";
            this.label20.Size = new System.Drawing.Size(100, 15);
            this.label20.TabIndex = 15;
            this.label20.Text = "Page Numbering:";
            // 
            // pageNumberComboBox
            // 
            this.pageNumberComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.pageNumberComboBox.FormattingEnabled = true;
            this.pageNumberComboBox.Items.AddRange(new object[] {
            "Left to Right then Top to Bottom",
            "Left to Right then Bottom to Top",
            "Top to Bottom then Left to Right",
            "Bottom to Top then Left to Right"});
            this.pageNumberComboBox.Location = new System.Drawing.Point(119, 180);
            this.pageNumberComboBox.Name = "pageNumberComboBox";
            this.pageNumberComboBox.Size = new System.Drawing.Size(187, 23);
            this.pageNumberComboBox.TabIndex = 14;
            this.pageNumberComboBox.SelectedIndexChanged += new System.EventHandler(this.OptionalPreviewButton_Click);
            // 
            // delimiterTextBox
            // 
            this.delimiterTextBox.Location = new System.Drawing.Point(119, 93);
            this.delimiterTextBox.Name = "delimiterTextBox";
            this.delimiterTextBox.Size = new System.Drawing.Size(187, 23);
            this.delimiterTextBox.TabIndex = 13;
            this.delimiterTextBox.TextChanged += new System.EventHandler(this.OptionalPreviewButton_Click);
            // 
            // conventionComboBox
            // 
            this.conventionComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.conventionComboBox.FormattingEnabled = true;
            this.conventionComboBox.Items.AddRange(new object[] {
            "Row-Column",
            "Column-Row"});
            this.conventionComboBox.Location = new System.Drawing.Point(119, 6);
            this.conventionComboBox.Name = "conventionComboBox";
            this.conventionComboBox.Size = new System.Drawing.Size(187, 23);
            this.conventionComboBox.TabIndex = 12;
            this.conventionComboBox.SelectedIndexChanged += new System.EventHandler(this.OptionalPreviewButton_Click);
            // 
            // columnStyleComboBox
            // 
            this.columnStyleComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.columnStyleComboBox.FormattingEnabled = true;
            this.columnStyleComboBox.Items.AddRange(new object[] {
            "Uppercase Alphabetic (A..Z,AA..AZ,BA..BZ,...)",
            "Lowercase Alphabetic (a..z,aa..az,ba..bz,...)",
            "Integer (1,2,3,...)",
            "Zero padded Integers (01,02,03,...)"});
            this.columnStyleComboBox.Location = new System.Drawing.Point(119, 122);
            this.columnStyleComboBox.Name = "columnStyleComboBox";
            this.columnStyleComboBox.Size = new System.Drawing.Size(187, 23);
            this.columnStyleComboBox.TabIndex = 11;
            this.columnStyleComboBox.SelectedIndexChanged += new System.EventHandler(this.OptionalPreviewButton_Click);
            // 
            // suffixTextBox
            // 
            this.suffixTextBox.Location = new System.Drawing.Point(119, 151);
            this.suffixTextBox.Name = "suffixTextBox";
            this.suffixTextBox.Size = new System.Drawing.Size(187, 23);
            this.suffixTextBox.TabIndex = 10;
            this.suffixTextBox.TextChanged += new System.EventHandler(this.OptionalPreviewButton_Click);
            // 
            // label18
            // 
            this.label18.AutoSize = true;
            this.label18.Location = new System.Drawing.Point(3, 154);
            this.label18.Name = "label18";
            this.label18.Size = new System.Drawing.Size(39, 15);
            this.label18.TabIndex = 7;
            this.label18.Text = "Suffix:";
            // 
            // label17
            // 
            this.label17.AutoSize = true;
            this.label17.Location = new System.Drawing.Point(3, 9);
            this.label17.Name = "label17";
            this.label17.Size = new System.Drawing.Size(72, 15);
            this.label17.TabIndex = 6;
            this.label17.Text = "Convention:";
            // 
            // label16
            // 
            this.label16.AutoSize = true;
            this.label16.Location = new System.Drawing.Point(3, 125);
            this.label16.Name = "label16";
            this.label16.Size = new System.Drawing.Size(81, 15);
            this.label16.TabIndex = 5;
            this.label16.Text = "Column Style:";
            // 
            // label15
            // 
            this.label15.AutoSize = true;
            this.label15.Location = new System.Drawing.Point(3, 67);
            this.label15.Name = "label15";
            this.label15.Size = new System.Drawing.Size(61, 15);
            this.label15.TabIndex = 4;
            this.label15.Text = "Row Style:";
            // 
            // label14
            // 
            this.label14.AutoSize = true;
            this.label14.Location = new System.Drawing.Point(3, 96);
            this.label14.Name = "label14";
            this.label14.Size = new System.Drawing.Size(58, 15);
            this.label14.TabIndex = 3;
            this.label14.Text = "Delimiter:";
            // 
            // label13
            // 
            this.label13.AutoSize = true;
            this.label13.Location = new System.Drawing.Point(3, 38);
            this.label13.Name = "label13";
            this.label13.Size = new System.Drawing.Size(39, 15);
            this.label13.TabIndex = 2;
            this.label13.Text = "Prefix:";
            // 
            // rowStyleComboBox
            // 
            this.rowStyleComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.rowStyleComboBox.FormattingEnabled = true;
            this.rowStyleComboBox.Items.AddRange(new object[] {
            "Uppercase Alphabetic (A..Z,AA..AZ,BA..BZ,...)",
            "Lowercase Alphabetic (a..z,aa..az,ba..bz,...)",
            "Integer (1,2,3,...)",
            "Zero padded Integers (01,02,03,...)"});
            this.rowStyleComboBox.Location = new System.Drawing.Point(119, 64);
            this.rowStyleComboBox.Name = "rowStyleComboBox";
            this.rowStyleComboBox.Size = new System.Drawing.Size(187, 23);
            this.rowStyleComboBox.TabIndex = 1;
            this.rowStyleComboBox.SelectedIndexChanged += new System.EventHandler(this.OptionalPreviewButton_Click);
            // 
            // prefixTextBox
            // 
            this.prefixTextBox.Location = new System.Drawing.Point(119, 35);
            this.prefixTextBox.Name = "prefixTextBox";
            this.prefixTextBox.Size = new System.Drawing.Size(187, 23);
            this.prefixTextBox.TabIndex = 0;
            this.prefixTextBox.TextChanged += new System.EventHandler(this.OptionalPreviewButton_Click);
            // 
            // applyButton
            // 
            this.applyButton.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.applyButton.Location = new System.Drawing.Point(315, 483);
            this.applyButton.Name = "applyButton";
            this.applyButton.Size = new System.Drawing.Size(75, 23);
            this.applyButton.TabIndex = 11;
            this.applyButton.Text = "Preview";
            this.applyButton.UseVisualStyleBackColor = true;
            this.applyButton.Click += new System.EventHandler(this.PreviewButton_Click);
            // 
            // cancelButton
            // 
            this.cancelButton.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.cancelButton.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.cancelButton.Location = new System.Drawing.Point(396, 483);
            this.cancelButton.Name = "cancelButton";
            this.cancelButton.Size = new System.Drawing.Size(75, 23);
            this.cancelButton.TabIndex = 12;
            this.cancelButton.Text = "Cancel";
            this.cancelButton.UseVisualStyleBackColor = true;
            this.cancelButton.Click += new System.EventHandler(this.cancelButton_Click);
            // 
            // outputPathTextBox
            // 
            this.outputPathTextBox.Anchor = ((System.Windows.Forms.AnchorStyles)(((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)
                        | System.Windows.Forms.AnchorStyles.Right)));
            this.outputPathTextBox.Enabled = false;
            this.outputPathTextBox.Location = new System.Drawing.Point(15, 404);
            this.outputPathTextBox.Name = "outputPathTextBox";
            this.outputPathTextBox.Size = new System.Drawing.Size(430, 23);
            this.outputPathTextBox.TabIndex = 13;
            // 
            // label1
            // 
            this.label1.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Left)));
            this.label1.AutoSize = true;
            this.label1.Location = new System.Drawing.Point(16, 386);
            this.label1.Name = "label1";
            this.label1.Size = new System.Drawing.Size(177, 15);
            this.label1.TabIndex = 14;
            this.label1.Text = "Output shapefile or feature class";
            // 
            // browseButton
            // 
            this.browseButton.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.browseButton.Location = new System.Drawing.Point(448, 403);
            this.browseButton.Name = "browseButton";
            this.browseButton.Size = new System.Drawing.Size(23, 23);
            this.browseButton.TabIndex = 15;
            this.browseButton.Text = "...";
            this.browseButton.UseVisualStyleBackColor = true;
            this.browseButton.Click += new System.EventHandler(this.browseButton_Click);
            // 
            // saveButton
            // 
            this.saveButton.Anchor = ((System.Windows.Forms.AnchorStyles)((System.Windows.Forms.AnchorStyles.Bottom | System.Windows.Forms.AnchorStyles.Right)));
            this.saveButton.Enabled = false;
            this.saveButton.Location = new System.Drawing.Point(234, 482);
            this.saveButton.Name = "saveButton";
            this.saveButton.Size = new System.Drawing.Size(75, 23);
            this.saveButton.TabIndex = 16;
            this.saveButton.Text = "Save";
            this.saveButton.UseVisualStyleBackColor = true;
            // 
            // GenerateGridForm
            // 
            this.AcceptButton = this.applyButton;
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.cancelButton;
            this.ClientSize = new System.Drawing.Size(483, 518);
            this.Controls.Add(this.browseSpatialRefButton);
            this.Controls.Add(this.saveButton);
            this.Controls.Add(this.spatialReferenceTextBox);
            this.Controls.Add(this.browseButton);
            this.Controls.Add(this.outputPathTextBox);
            this.Controls.Add(this.cancelButton);
            this.Controls.Add(this.applyButton);
            this.Controls.Add(this.tabControl1);
            this.Controls.Add(this.label1);
            this.Controls.Add(this.label12);
            this.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.MinimumSize = new System.Drawing.Size(470, 470);
            this.Name = "GenerateGridForm";
            this.Text = "Generate Grid";
            this.tabControl1.ResumeLayout(false);
            this.tabPage2.ResumeLayout(false);
            this.tabPage2.PerformLayout();
            this.quantityBox.ResumeLayout(false);
            this.quantityBox.PerformLayout();
            this.sizeBox.ResumeLayout(false);
            this.sizeBox.PerformLayout();
            this.tabPage3.ResumeLayout(false);
            this.tabPage3.PerformLayout();
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.TabControl tabControl1;
        private System.Windows.Forms.TabPage tabPage2;
        private System.Windows.Forms.TabPage tabPage3;
        private System.Windows.Forms.Button applyButton;
        private System.Windows.Forms.Button cancelButton;
        private System.Windows.Forms.Label label1;
        private System.Windows.Forms.Button browseButton;
        private System.Windows.Forms.GroupBox quantityBox;
        private System.Windows.Forms.TextBox yCountTextBox;
        private System.Windows.Forms.TextBox xCountTextBox;
        private System.Windows.Forms.Label label11;
        private System.Windows.Forms.Label label10;
        private System.Windows.Forms.GroupBox sizeBox;
        private System.Windows.Forms.TextBox widthTextBox;
        private System.Windows.Forms.Label label3;
        private System.Windows.Forms.Label label9;
        private System.Windows.Forms.TextBox heightTextBox;
        private System.Windows.Forms.ComboBox unitsComboBox;
        private System.Windows.Forms.Label label4;
        private System.Windows.Forms.Label label12;
        private System.Windows.Forms.Button browseSpatialRefButton;
        private System.Windows.Forms.TextBox spatialReferenceTextBox;
        private System.Windows.Forms.TextBox delimiterTextBox;
        private System.Windows.Forms.ComboBox conventionComboBox;
        private System.Windows.Forms.ComboBox columnStyleComboBox;
        private System.Windows.Forms.TextBox suffixTextBox;
        private System.Windows.Forms.Label label18;
        private System.Windows.Forms.Label label17;
        private System.Windows.Forms.Label label16;
        private System.Windows.Forms.Label label15;
        private System.Windows.Forms.Label label14;
        private System.Windows.Forms.Label label13;
        private System.Windows.Forms.ComboBox rowStyleComboBox;
        private System.Windows.Forms.TextBox prefixTextBox;
        private System.Windows.Forms.Label label20;
        private System.Windows.Forms.ComboBox pageNumberComboBox;
        private System.Windows.Forms.Label label2;
        private System.Windows.Forms.ToolTip toolTip1;
        internal System.Windows.Forms.Button saveButton;
        private System.Windows.Forms.TextBox outputPathTextBox;

    }
}