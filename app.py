import streamlit as st
import pyperclip

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

# إزالة الأصفار الزائدة من الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تحميل الإعدادات
egg_price, feed_price = load_config()

# واجهة Streamlit
st.title("مرحباً بكم في حاسبة الدجاج Newyolk")

# استخدام الأعمدة لجعل الواجهة responsive
col1, col2 = st.columns(2)

with col1:
    # اختيار العملة
    currency = st.selectbox("العملة", ["دولار", "دينار عراقي"])

with col2:
    # اختيار نوع الحساب
    calculation_type = st.selectbox("نوع الحساب", ["أرباح الدجاجة", "أرباح المكافآت والطعام اليومي"])

# قسم الحسابات
if calculation_type == "أرباح الدجاجة":
    st.subheader("حساب أرباح الدجاجة")
    col3, col4 = st.columns(2)

    with col3:
        eggs = st.number_input("عدد البيض", min_value=0, max_value=580, value=0)

    with col4:
        days = st.number_input("عدد الأيام", min_value=0, max_value=730, value=0)

    if st.button("احسب أرباح الدجاجة"):
        if eggs > 580:
            st.error("عدد البيض يجب ألا يتجاوز 580!")
        elif days > 730:
            st.error("عدد الأيام يجب ألا يتجاوز 730!")
        else:
            # حساب النتائج بالدولار
            total_egg_price_usd = eggs * egg_price
            total_feed_cost_usd = (days * 2) * feed_price
            net_profit_before_rent_usd = total_egg_price_usd - total_feed_cost_usd
            rent_cost_usd = 6.0
            net_profit_usd = net_profit_before_rent_usd - rent_cost_usd

            # حساب النتائج بالدينار العراقي
            total_egg_price_iqd = total_egg_price_usd * 1480
            total_feed_cost_iqd = total_feed_cost_usd * 1480
            net_profit_before_rent_iqd = net_profit_before_rent_usd * 1480
            rent_cost_iqd = rent_cost_usd * 1480
            net_profit_iqd = net_profit_usd * 1480

            if currency == "دينار عراقي":
                st.write(f"سعر البيض الكلي: **{format_decimal(total_egg_price_iqd)}** دينار عراقي")
                st.write(f"تكلفة العلف الكلية: **{format_decimal(total_feed_cost_iqd)}** دينار عراقي")
                st.write(f"الربح الصافي قبل دفع الإيجار: **{format_decimal(net_profit_before_rent_iqd)}** دينار عراقي")
                st.write(f"دفع الإيجار للسنة الثانية: **{format_decimal(rent_cost_iqd)}** دينار عراقي")
                st.write(f"الربح الصافي: **{format_decimal(net_profit_iqd)}** دينار عراقي")
            else:
                st.write(f"سعر البيض الكلي: **{format_decimal(total_egg_price_usd)}** دولار")
                st.write(f"تكلفة العلف الكلية: **{format_decimal(total_feed_cost_usd)}** دولار")
                st.write(f"الربح الصافي قبل دفع الإيجار: **{format_decimal(net_profit_before_rent_usd)}** دولار")
                st.write(f"دفع الإيجار للسنة الثانية: **{format_decimal(rent_cost_usd)}** دولار")
                st.write(f"الربح الصافي: **{format_decimal(net_profit_usd)}** دولار")

            if st.button("نسخ النتائج إلى الحافظة"):
                results = f"""
                النتائج بالدولار:
                سعر البيض الكلي: {format_decimal(total_egg_price_usd)} دولار
                تكلفة العلف الكلية: {format_decimal(total_feed_cost_usd)} دولار
                الربح الصافي قبل دفع الإيجار: {format_decimal(net_profit_before_rent_usd)} دولار
                دفع الإيجار للسنة الثانية: {format_decimal(rent_cost_usd)} دولار
                الربح الصافي: {format_decimal(net_profit_usd)} دولار

                النتائج بالدينار العراقي:
                سعر البيض الكلي: {format_decimal(total_egg_price_iqd)} دينار عراقي
                تكلفة العلف الكلية: {format_decimal(total_feed_cost_iqd)} دينار عراقي
                الربح الصافي قبل دفع الإيجار: {format_decimal(net_profit_before_rent_iqd)} دينار عراقي
                دفع الإيجار للسنة الثانية: {format_decimal(rent_cost_iqd)} دينار عراقي
                الربح الصافي: {format_decimal(net_profit_iqd)} دينار عراقي
                """
                pyperclip.copy(results)
                st.success("تم نسخ النتائج إلى الحافظة بنجاح!")

elif calculation_type == "أرباح المكافآت والطعام اليومي":
    st.subheader("حساب أرباح المكافآت والطعام اليومي")
    col5, col6 = st.columns(2)

    with col5:
        rewards = st.number_input("عدد المكافآت", min_value=0, value=0)

    with col6:
        food = st.number_input("عدد الطعام المطلوب", min_value=0, value=0)

    if st.button("احسب أرباح المكافآت والطعام اليومي"):
        # حساب النتائج بالدولار
        total_egg_price_usd = rewards * egg_price
        total_feed_cost_usd = food * feed_price
        net_profit_usd = total_egg_price_usd - total_feed_cost_usd

        # حساب النتائج بالدينار العراقي
        total_egg_price_iqd = total_egg_price_usd * 1480
        total_feed_cost_iqd = total_feed_cost_usd * 1480
        net_profit_iqd = net_profit_usd * 1480

        if currency == "دينار عراقي":
            st.write(f"سعر البيض الكلي: **{format_decimal(total_egg_price_iqd)}** دينار عراقي")
            st.write(f"تكلفة العلف الكلية: **{format_decimal(total_feed_cost_iqd)}** دينار عراقي")
            st.write(f"الربح اليومي: **{format_decimal(net_profit_iqd)}** دينار عراقي")
        else:
            st.write(f"سعر البيض الكلي: **{format_decimal(total_egg_price_usd)}** دولار")
            st.write(f"تكلفة العلف الكلية: **{format_decimal(total_feed_cost_usd)}** دولار")
            st.write(f"الربح اليومي: **{format_decimal(net_profit_usd)}** دولار")

        if st.button("نسخ النتائج إلى الحافظة"):
            results = f"""
            النتائج بالدولار:
            سعر البيض الكلي: {format_decimal(total_egg_price_usd)} دولار
            تكلفة العلف الكلية: {format_decimal(total_feed_cost_usd)} دولار
            الربح اليومي: {format_decimal(net_profit_usd)} دولار

            النتائج بالدينار العراقي:
            سعر البيض الكلي: {format_decimal(total_egg_price_iqd)} دينار عراقي
            تكلفة العلف الكلية: {format_decimal(total_feed_cost_iqd)} دينار عراقي
            الربح اليومي: {format_decimal(net_profit_iqd)} دينار عراقي
            """
            pyperclip.copy(results)
            st.success("تم نسخ النتائج إلى الحافظة بنجاح!")

# قسم تعديل الأسعار
with st.expander("تعديل الأسعار"):
    st.subheader("تعديل الأسعار")
    new_egg_price = st.number_input("سعر البيض الجديد", value=egg_price)
    new_feed_price = st.number_input("سعر العلف الجديد", value=feed_price)

    if st.button("حفظ الأسعار الجديدة"):
        save_config(new_egg_price, new_feed_price)
        st.success("تم حفظ الأسعار الجديدة بنجاح!")
