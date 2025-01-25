import streamlit as st
import clipboard  # مكتبة للتعامل مع الحافظة

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# دالة لنسخ النتائج إلى الحافظة
def copy_to_clipboard(text):
    try:
        clipboard.copy(text)  # نسخ النص إلى الحافظة
        st.success("تم نسخ النتائج إلى الحافظة بنجاح!" if language == "العربية" else "Results copied to clipboard successfully!")
    except Exception as e:
        st.error(f"حدث خطأ أثناء النسخ: {e}" if language == "العربية" else f"An error occurred while copying: {e}")

# تحسين الواجهة
st.set_page_config(page_title="Newyolk Chicken Calculator", page_icon="🐔", layout="wide")

# اختيار اللغة
language = st.sidebar.selectbox("اختر اللغة / Choose Language", ["العربية", "English"])

# الأسعار المبدئية
if "egg_price" not in st.session_state:
    st.session_state.egg_price = 0.1155
if "feed_price" not in st.session_state:
    st.session_state.feed_price = 0.0189

# عنوان التطبيق مع تصميم مخصص
if language == "العربية":
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
else:
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
        <div class="title">🐔 Newyolk - Chicken Calculator</div>
        <div class="subtitle">Calculate Chicken Profits and Daily Rewards</div>
        """,
        unsafe_allow_html=True
    )

# استخدام الأعمدة لتخطيط أفضل
col1, col2 = st.columns(2)

with col1:
    currency = st.selectbox("العملة" if language == "العربية" else "Currency", ["دولار" if language == "العربية" else "USD", "دينار عراقي" if language == "العربية" else "IQD"])

with col2:
    calculation_type = st.selectbox("نوع الحساب" if language == "العربية" else "Calculation Type", ["أرباح الدجاجة" if language == "العربية" else "Chicken Profits", "أرباح المكافآت والطعام اليومي" if language == "العربية" else "Daily Rewards and Food"])

# قسم الحسابات
if calculation_type == "أرباح الدجاجة" or calculation_type == "Chicken Profits":
    st.subheader("حساب أرباح الدجاجة" if language == "العربية" else "Chicken Profits Calculation")
    col3, col4 = st.columns(2)

    with col3:
        eggs = st.number_input("عدد البيض" if language == "العربية" else "Number of Eggs", min_value=0, max_value=580, value=0, help="أدخل عدد البيض (بحد أقصى 580)" if language == "العربية" else "Enter the number of eggs (max 580)")

    with col4:
        days = st.number_input("عدد الأيام" if language == "العربية" else "Number of Days", min_value=0, max_value=730, value=0, help="أدخل عدد الأيام (بحد أقصى 730)" if language == "العربية" else "Enter the number of days (max 730)")

    if st.button("احسب أرباح الدجاجة" if language == "العربية" else "Calculate Chicken Profits", type="primary"):
        if eggs > 580:
            st.error("عدد البيض يجب ألا يتجاوز 580!" if language == "العربية" else "Number of eggs must not exceed 580!")
        elif days > 730:
            st.error("عدد الأيام يجب ألا يتجاوز 730!" if language == "العربية" else "Number of days must not exceed 730!")
        else:
            # حساب النتائج
            total_egg_price_usd = eggs * st.session_state.egg_price
            total_feed_cost_usd = (days * 2) * st.session_state.feed_price
            net_profit_before_rent_usd = total_egg_price_usd - total_feed_cost_usd
            rent_cost_usd = 6.0
            net_profit_usd = net_profit_before_rent_usd - rent_cost_usd

            if currency == "دينار عراقي" or currency == "IQD":
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
            st.success("تم الحساب بنجاح!" if language == "العربية" else "Calculation completed successfully!")
            st.write(f"سعر البيض الكلي: **{format_decimal(total_egg_price)}** {currency}" if language == "العربية" else f"Total Egg Price: **{format_decimal(total_egg_price)}** {currency}")
            st.write(f"تكلفة العلف الكلية: **{format_decimal(total_feed_cost)}** {currency}" if language == "العربية" else f"Total Feed Cost: **{format_decimal(total_feed_cost)}** {currency}")
            st.write(f"الربح الصافي قبل دفع الإيجار: **{format_decimal(net_profit_before_rent)}** {currency}" if language == "العربية" else f"Net Profit Before Rent: **{format_decimal(net_profit_before_rent)}** {currency}")
            st.write(f"دفع الإيجار للسنة الثانية: **{format_decimal(rent_cost)}** {currency}" if language == "العربية" else f"Rent Cost for Second Year: **{format_decimal(rent_cost)}** {currency}")
            st.write(f"الربح الصافي: **{format_decimal(net_profit)}** {currency}" if language == "العربية" else f"Net Profit: **{format_decimal(net_profit)}** {currency}")

            # نسخ النتائج
            results = f"""
            سعر البيض الكلي: {format_decimal(total_egg_price)} {currency}
            تكلفة العلف الكلية: {format_decimal(total_feed_cost)} {currency}
            الربح الصافي قبل دفع الإيجار: {format_decimal(net_profit_before_rent)} {currency}
            دفع الإيجار للسنة الثانية: {format_decimal(rent_cost)} {currency}
            الربح الصافي: {format_decimal(net_profit)} {currency}
            """ if language == "العربية" else f"""
            Total Egg Price: {format_decimal(total_egg_price)} {currency}
            Total Feed Cost: {format_decimal(total_feed_cost)} {currency}
            Net Profit Before Rent: {format_decimal(net_profit_before_rent)} {currency}
            Rent Cost for Second Year: {format_decimal(rent_cost)} {currency}
            Net Profit: {format_decimal(net_profit)} {currency}
            """
            if st.button("نسخ النتائج إلى الحافظة" if language == "العربية" else "Copy Results to Clipboard"):
                copy_to_clipboard(results)

elif calculation_type == "أرباح المكافآت والطعام اليومي" or calculation_type == "Daily Rewards and Food":
    st.subheader("حساب أرباح المكافآت والطعام اليومي" if language == "العربية" else "Daily Rewards and Food Calculation")
    col5, col6 = st.columns(2)

    with col5:
        rewards = st.number_input("عدد المكافآت" if language == "العربية" else "Number of Rewards", min_value=0, value=0, help="أدخل عدد المكافآت" if language == "العربية" else "Enter the number of rewards")

    with col6:
        food = st.number_input("عدد الطعام المطلوب" if language == "العربية" else "Amount of Food Required", min_value=0, value=0, help="أدخل عدد الطعام المطلوب" if language == "العربية" else "Enter the amount of food required")

    if st.button("احسب أرباح المكافآت والطعام اليومي" if language == "العربية" else "Calculate Daily Rewards and Food", type="primary"):
        # حساب النتائج
        total_egg_price_usd = rewards * st.session_state.egg_price
        total_feed_cost_usd = food * st.session_state.feed_price
        net_profit_usd = total_egg_price_usd - total_feed_cost_usd

        if currency == "دينار عراقي" or currency == "IQD":
            total_egg_price = total_egg_price_usd * 1480
            total_feed_cost = total_feed_cost_usd * 1480
            net_profit = net_profit_usd * 1480
        else:
            total_egg_price, total_feed_cost, net_profit = (
                total_egg_price_usd, total_feed_cost_usd, net_profit_usd
            )

        # عرض النتائج
        st.success("تم الحساب بنجاح!" if language == "العربية" else "Calculation completed successfully!")
        st.write(f"سعر البيض الكلي: **{format_decimal(total_egg_price)}** {currency}" if language == "العربية" else f"Total Egg Price: **{format_decimal(total_egg_price)}** {currency}")
        st.write(f"تكلفة العلف الكلية: **{format_decimal(total_feed_cost)}** {currency}" if language == "العربية" else f"Total Feed Cost: **{format_decimal(total_feed_cost)}** {currency}")
        st.write(f"الربح اليومي: **{format_decimal(net_profit)}** {currency}" if language == "العربية" else f"Daily Profit: **{format_decimal(net_profit)}** {currency}")

        # نسخ النتائج
        results = f"""
        سعر البيض الكلي: {format_decimal(total_egg_price)} {currency}
        تكلفة العلف الكلية: {format_decimal(total_feed_cost)} {currency}
        الربح اليومي: {format_decimal(net_profit)} {currency}
        """ if language == "العربية" else f"""
        Total Egg Price: {format_decimal(total_egg_price)} {currency}
        Total Feed Cost: {format_decimal(total_feed_cost)} {currency}
        Daily Profit: {format_decimal(net_profit)} {currency}
        """
        if st.button("نسخ النتائج إلى الحافظة" if language == "العربية" else "Copy Results to Clipboard"):
            copy_to_clipboard(results)

# قسم تعديل الأسعار
with st.expander("⚙️ تعديل الأسعار" if language == "العربية" else "⚙️ Edit Prices"):
    st.subheader("تعديل الأسعار" if language == "العربية" else "Edit Prices")
    new_egg_price = st.number_input("سعر البيض الجديد" if language == "العربية" else "New Egg Price", value=st.session_state.egg_price, format="%.4f")
    new_feed_price = st.number_input("سعر العلف الجديد" if language == "العربية" else "New Feed Price", value=st.session_state.feed_price, format="%.4f")

    if st.button("حفظ الأسعار الجديدة" if language == "العربية" else "Save New Prices", type="secondary"):
        st.session_state.egg_price = new_egg_price
        st.session_state.feed_price = new_feed_price
        st.success("تم حفظ الأسعار الجديدة بنجاح!" if language == "العربية" else "New prices saved successfully!")
