import streamlit as st
import clipboard  # مكتبة للتعامل مع الحافظة

# ملف الإعدادات
CONFIG_FILE = "config.txt"

# قراءة الإعدادات من الملف
def load_config():
    try:
        with open(CONFIG_FILE, "r") as file:
            egg_price = float(file.readline().strip())
            feed_price = float(file.readline().strip())
            return egg_price, feed_price
    except FileNotFoundError:
        egg_price = 0.1155
        feed_price = 0.0189
        save_config(egg_price, feed_price)
        return egg_price, feed_price

# حفظ الإعدادات في الملف
def save_config(egg_price, feed_price):
    with open(CONFIG_FILE, "w") as file:
        file.write(f"{egg_price}\n{feed_price}\n")

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# دالة لنسخ النتائج إلى الحافظة
def copy_to_clipboard(text):
    try:
        clipboard.copy(text)  # نسخ النص إلى الحافظة
        st.success("تم نسخ النتائج إلى الحافظة بنجاح!")
    except Exception as e:
        st.error(f"حدث خطأ أثناء النسخ: {e}")

# تحميل الإعدادات
egg_price, feed_price = load_config()

# تحسين الواجهة
st.set_page_config(page_title="حاسبة الدجاج Newyolk", page_icon="🐔", layout="wide")

# عنوان التطبيق مع تصميم مخصص
st.markdown(
    """
    <style>
    .title {
        font-size: 40px;
        font-weight: bold;
        color: #4CAF50;
        text-align: center;
        padding: 20px;
    }
    .subtitle {
        font-size: 20px;
        color: #FF5722;
        text-align: center;
        margin-bottom: 30px;
    }
    </style>
    <div class="title">🐔 Newyolk - حاسبة الدجاج</div>
    <div class="subtitle">حساب أرباح الدجاج والمكافآت اليومية</div>
    """,
    unsafe_allow_html=True
)

# استخدام الأعمدة لتخطيط أفضل
col1, col2 = st.columns(2)

with col1:
    currency = st.selectbox("العملة", ["دولار", "دينار عراقي"])

with col2:
    calculation_type = st.selectbox("نوع الحساب", ["أرباح الدجاجة", "أرباح المكافآت والطعام اليومي"])

# قسم الحسابات
if calculation_type == "أرباح الدجاجة":
    st.subheader("حساب أرباح الدجاجة")
    col3, col4 = st.columns(2)

    with col3:
        eggs = st.number_input("عدد البيض", min_value=0, max_value=580, value=0, help="أدخل عدد البيض (بحد أقصى 580)")

    with col4:
        days = st.number_input("عدد الأيام", min_value=0, max_value=730, value=0, help="أدخل عدد الأيام (بحد أقصى 730)")

    if st.button("احسب أرباح الدجاجة", type="primary"):
        if eggs > 580:
            st.error("عدد البيض يجب ألا يتجاوز 580!")
        elif days > 730:
            st.error("عدد الأيام يجب ألا يتجاوز 730!")
        else:
            # حساب النتائج
            total_egg_price_usd = eggs * egg_price
            total_feed_cost_usd = (days * 2) * feed_price
            net_profit_before_rent_usd = total_egg_price_usd - total_feed_cost_usd
            rent_cost_usd = 6.0
            net_profit_usd = net_profit_before_rent_usd - rent_cost_usd

            if currency == "دينار عراقي":
                total_egg_price = total_egg_price_usd * 1480
                total_feed_cost = total_feed_cost_usd * 1480
                net_profit_before_rent = net_profit_before_rent_usd * 1480
                rent_cost = rent_cost_usd * 1480
                net_profit = net_profit_usd * 1480
            else:
                total_egg_price, total_feed_cost, net_profit_before_rent, rent_cost, net_profit = (
                    total_egg_price_usd, total_feed_cost_usd, net_profit_before_rent_usd, rent_cost_usd, net_profit_usd
                )

            # عرض النتائج
            st.success("تم الحساب بنجاح!")
            st.write(f"سعر البيض الكلي: **{format_decimal(total_egg_price)}** {currency}")
            st.write(f"تكلفة العلف الكلية: **{format_decimal(total_feed_cost)}** {currency}")
            st.write(f"الربح الصافي قبل دفع الإيجار: **{format_decimal(net_profit_before_rent)}** {currency}")
            st.write(f"دفع الإيجار للسنة الثانية: **{format_decimal(rent_cost)}** {currency}")
            st.write(f"الربح الصافي: **{format_decimal(net_profit)}** {currency}")

            # نسخ النتائج
            results = f"""
            سعر البيض الكلي: {format_decimal(total_egg_price)} {currency}
            تكلفة العلف الكلية: {format_decimal(total_feed_cost)} {currency}
            الربح الصافي قبل دفع الإيجار: {format_decimal(net_profit_before_rent)} {currency}
            دفع الإيجار للسنة الثانية: {format_decimal(rent_cost)} {currency}
            الربح الصافي: {format_decimal(net_profit)} {currency}
            """
            if st.button("نسخ النتائج إلى الحافظة"):
                copy_to_clipboard(results)

elif calculation_type == "أرباح المكافآت والطعام اليومي":
    st.subheader("حساب أرباح المكافآت والطعام اليومي")
    col5, col6 = st.columns(2)

    with col5:
        rewards = st.number_input("عدد المكافآت", min_value=0, value=0, help="أدخل عدد المكافآت")

    with col6:
        food = st.number_input("عدد الطعام المطلوب", min_value=0, value=0, help="أدخل عدد الطعام المطلوب")

    if st.button("احسب أرباح المكافآت والطعام اليومي", type="primary"):
        # حساب النتائج
        total_egg_price_usd = rewards * egg_price
        total_feed_cost_usd = food * feed_price
        net_profit_usd = total_egg_price_usd - total_feed_cost_usd

        if currency == "دينار عراقي":
            total_egg_price = total_egg_price_usd * 1480
            total_feed_cost = total_feed_cost_usd * 1480
            net_profit = net_profit_usd * 1480
        else:
            total_egg_price, total_feed_cost, net_profit = (
                total_egg_price_usd, total_feed_cost_usd, net_profit_usd
            )

        # عرض النتائج
        st.success("تم الحساب بنجاح!")
        st.write(f"سعر البيض الكلي: **{format_decimal(total_egg_price)}** {currency}")
        st.write(f"تكلفة العلف الكلية: **{format_decimal(total_feed_cost)}** {currency}")
        st.write(f"الربح اليومي: **{format_decimal(net_profit)}** {currency}")

        # نسخ النتائج
        results = f"""
        سعر البيض الكلي: {format_decimal(total_egg_price)} {currency}
        تكلفة العلف الكلية: {format_decimal(total_feed_cost)} {currency}
        الربح اليومي: {format_decimal(net_profit)} {currency}
        """
        if st.button("نسخ النتائج إلى الحافظة"):
            copy_to_clipboard(results)

# قسم تعديل الأسعار
with st.expander("⚙️ تعديل الأسعار"):
    st.subheader("تعديل الأسعار")
    new_egg_price = st.number_input("سعر البيض الجديد", value=egg_price, format="%.4f")
    new_feed_price = st.number_input("سعر العلف الجديد", value=feed_price, format="%.4f")

    if st.button("حفظ الأسعار الجديدة", type="secondary"):
        save_config(new_egg_price, new_feed_price)
        st.success("تم حفظ الأسعار الجديدة بنجاح!")
