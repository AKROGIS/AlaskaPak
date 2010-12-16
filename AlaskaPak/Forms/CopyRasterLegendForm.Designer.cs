namespace NPS.AKRO.ArcGIS.Forms
{
    partial class CopyRasterLegendForm
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
            this.sourceLabel = new System.Windows.Forms.Label();
            this.destinationLabel = new System.Windows.Forms.Label();
            this.sourceComboBox = new System.Windows.Forms.ComboBox();
            this.destinationListBox = new System.Windows.Forms.CheckedListBox();
            this.selectAllButton = new System.Windows.Forms.Button();
            this.unselectAllButton = new System.Windows.Forms.Button();
            this.copyButton = new System.Windows.Forms.Button();
            this.cancelButton = new System.Windows.Forms.Button();
            this.SuspendLayout();
            // 
            // sourceLabel
            // 
            this.sourceLabel.AutoSize = true;
            this.sourceLabel.Location = new System.Drawing.Point(15, 15);
            this.sourceLabel.Name = "sourceLabel";
            this.sourceLabel.Size = new System.Drawing.Size(46, 15);
            this.sourceLabel.TabIndex = 0;
            this.sourceLabel.Text = "Source:";
            // 
            // destinationLabel
            // 
            this.destinationLabel.AutoSize = true;
            this.destinationLabel.Location = new System.Drawing.Point(15, 41);
            this.destinationLabel.Name = "destinationLabel";
            this.destinationLabel.Size = new System.Drawing.Size(70, 15);
            this.destinationLabel.TabIndex = 1;
            this.destinationLabel.Text = "Destination:";
            // 
            // sourceComboBox
            // 
            this.sourceComboBox.DropDownStyle = System.Windows.Forms.ComboBoxStyle.DropDownList;
            this.sourceComboBox.FormattingEnabled = true;
            this.sourceComboBox.Location = new System.Drawing.Point(91, 12);
            this.sourceComboBox.Name = "sourceComboBox";
            this.sourceComboBox.Size = new System.Drawing.Size(354, 23);
            this.sourceComboBox.Sorted = true;
            this.sourceComboBox.TabIndex = 2;
            this.sourceComboBox.SelectedIndexChanged += new System.EventHandler(this.sourceComboBox_SelectedIndexChanged);
            // 
            // destinationListBox
            // 
            this.destinationListBox.CheckOnClick = true;
            this.destinationListBox.FormattingEnabled = true;
            this.destinationListBox.HorizontalScrollbar = true;
            this.destinationListBox.Location = new System.Drawing.Point(91, 41);
            this.destinationListBox.Name = "destinationListBox";
            this.destinationListBox.Size = new System.Drawing.Size(354, 94);
            this.destinationListBox.Sorted = true;
            this.destinationListBox.TabIndex = 4;
            this.destinationListBox.ItemCheck += new System.Windows.Forms.ItemCheckEventHandler(this.destinationListBox_ItemCheck);
            // 
            // selectAllButton
            // 
            this.selectAllButton.Location = new System.Drawing.Point(91, 263);
            this.selectAllButton.Name = "selectAllButton";
            this.selectAllButton.Size = new System.Drawing.Size(75, 23);
            this.selectAllButton.TabIndex = 6;
            this.selectAllButton.Text = "&Select All";
            this.selectAllButton.UseVisualStyleBackColor = true;
            this.selectAllButton.Click += new System.EventHandler(this.selectAllButton_Click);
            // 
            // unselectAllButton
            // 
            this.unselectAllButton.Location = new System.Drawing.Point(172, 263);
            this.unselectAllButton.Name = "unselectAllButton";
            this.unselectAllButton.Size = new System.Drawing.Size(75, 23);
            this.unselectAllButton.TabIndex = 7;
            this.unselectAllButton.Text = "&Unselect All";
            this.unselectAllButton.UseVisualStyleBackColor = true;
            this.unselectAllButton.Click += new System.EventHandler(this.unselectAllButton_Click);
            // 
            // copyButton
            // 
            this.copyButton.Location = new System.Drawing.Point(289, 263);
            this.copyButton.Name = "copyButton";
            this.copyButton.Size = new System.Drawing.Size(75, 23);
            this.copyButton.TabIndex = 8;
            this.copyButton.Text = "Copy";
            this.copyButton.UseVisualStyleBackColor = true;
            this.copyButton.Click += new System.EventHandler(this.copyButton_Click);
            // 
            // cancelButton
            // 
            this.cancelButton.DialogResult = System.Windows.Forms.DialogResult.Cancel;
            this.cancelButton.Location = new System.Drawing.Point(370, 263);
            this.cancelButton.Name = "cancelButton";
            this.cancelButton.Size = new System.Drawing.Size(75, 23);
            this.cancelButton.TabIndex = 9;
            this.cancelButton.Text = "&Cancel";
            this.cancelButton.UseVisualStyleBackColor = true;
            this.cancelButton.Click += new System.EventHandler(this.cancelButton_Click);
            // 
            // CopyRasterLegendForm
            // 
            this.AcceptButton = this.copyButton;
            this.AutoScaleDimensions = new System.Drawing.SizeF(7F, 15F);
            this.AutoScaleMode = System.Windows.Forms.AutoScaleMode.Font;
            this.CancelButton = this.cancelButton;
            this.ClientSize = new System.Drawing.Size(460, 301);
            this.Controls.Add(this.cancelButton);
            this.Controls.Add(this.copyButton);
            this.Controls.Add(this.unselectAllButton);
            this.Controls.Add(this.selectAllButton);
            this.Controls.Add(this.destinationListBox);
            this.Controls.Add(this.sourceComboBox);
            this.Controls.Add(this.destinationLabel);
            this.Controls.Add(this.sourceLabel);
            this.Font = new System.Drawing.Font("Segoe UI", 9F, System.Drawing.FontStyle.Regular, System.Drawing.GraphicsUnit.Point, ((byte)(0)));
            this.Name = "CopyRasterLegendForm";
            this.Text = "Copy Raster Layer Legend";
            this.ResumeLayout(false);
            this.PerformLayout();

        }

        #endregion

        private System.Windows.Forms.Label sourceLabel;
        private System.Windows.Forms.Label destinationLabel;
        private System.Windows.Forms.ComboBox sourceComboBox;
        private System.Windows.Forms.CheckedListBox destinationListBox;
        private System.Windows.Forms.Button selectAllButton;
        private System.Windows.Forms.Button unselectAllButton;
        private System.Windows.Forms.Button copyButton;
        private System.Windows.Forms.Button cancelButton;
    }
}