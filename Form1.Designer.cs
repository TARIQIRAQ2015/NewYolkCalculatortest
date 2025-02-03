private void InitializeComponent()
{
    // ...existing code...
    this.comboBox2 = new System.Windows.Forms.ComboBox();
    // ...existing code...
    this.comboBox2.Items.AddRange(new object[] {
        "حساب رومانيا",
        "حساب العراق"});
    this.comboBox2.SelectedIndexChanged += new System.EventHandler(this.comboBox2_SelectedIndexChanged);
    // ...existing code...
}
