public partial class Form1 : Form
{
    private const double EGG_PRICE = 0.15;
    private const double FEED_PRICE = 0.02;
    private const double IRAQ_EGG_PRICE = 0.1219;
    private const double IRAQ_FEED_PRICE = 0.0191;

    public Form1()
    {
        InitializeComponent();
    }

    private void Form1_Load(object sender, EventArgs e)
    {
        comboBox1.Items.Add("Romania");
        comboBox1.Items.Add("Iraq");
        comboBox1.SelectedIndex = 0;

        comboBox2.Items.Clear();
        comboBox2.Items.Add("حساب رومانيا");
        comboBox2.Items.Add("حساب العراق");
        comboBox2.SelectedIndex = 0;
    }

    private void button1_Click(object sender, EventArgs e)
    {
        Calculate();
    }

    private void Calculate()
    {
        double eggPrice = comboBox2.SelectedIndex == 0 ? EGG_PRICE : IRAQ_EGG_PRICE;
        double feedPrice = comboBox2.SelectedIndex == 0 ? FEED_PRICE : IRAQ_FEED_PRICE;

        // استخدم eggPrice و feedPrice في العمليات الحسابية
        double eggs = double.Parse(textBox1.Text);
        double feed = double.Parse(textBox2.Text);
        double totalCost = eggs * eggPrice + feed * feedPrice;

        label3.Text = "Total Cost: " + totalCost.ToString("C");
    }

    private void comboBox2_SelectedIndexChanged(object sender, EventArgs e)
    {
        Calculate();
        UpdateResults();
    }

    private void UpdateResults()
    {
        if (comboBox2.SelectedIndex == 0)
        {
            // عرض نتائج حساب رومانيا
            label4.Text = "Romania Results";
        }
        else
        {
            // عرض نتائج حساب العراق
            // نفس المنطق ولكن باستخدام IRAQ_EGG_PRICE و IRAQ_FEED_PRICE
            label4.Text = "Iraq Results";
        }
    }
}
