import streamlit as st
import pandas as pd  # لإنشاء الجداول

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تحسين الواجهة
st.set_page_config(page_title="Newyolk Chicken Calculator", page_icon="🐔", layout="wide")

# حالة اللغة (العربية أو الإنجليزية)
if "language" not in st.session_state:
    st.session_state.language = "العربية"

# اختيار اللغة في السايد بار
language = st.sidebar.selectbox("اختر اللغة / Choose Language", ["العربية", "English"])

# الأسعار المبدئية
if "egg_price" not in st.session_state:
    st.session_state.egg_price = 0.1155
if "feed_price" not in st.session_state:
    st.session_state.feed_price = 0.0189

# تغيير اتجاه الكتابة بناءً على اللغة
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
            direction: rtl;
        }
        .subtitle {
            font-size: 20px;
            color: #FF5722;
            text-align: center;
            margin-bottom: 30px;
            direction: rtl;
        }
        .rtl {
            direction: rtl;
            text-align: right;
            font-size: 18px;
        }
        .stSelectbox, .stNumberInput {
            direction: rtl;
            text-align: right;
        }
        /* تعديل الزائد والناقص في الأرقام */
        .stNumberInput > div > div > button {
            margin-left: 0;
            margin-right: 5px;
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
            direction: ltr;
        }
        .subtitle {
            font-size: 20px;
            color: #FF5722;
            text-align: center;
            margin-bottom: 30px;
            direction: ltr;
        }
        .ltr {
            direction: ltr;
            text-align: left;
            font-size: 18px;
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
    currency = st.selectbox("العملة" if language == "العربية" else "Currency", ["دولار" if language == "العربية" else "USD", "دينار عراقي" if language == "العربية" else "IQD Flag: Iraq"])

with col2:
    calculation_type = st.selectbox("نوع الحساب" if language == "العربية" else "Calculation Type", ["أرباح الدجاجة" if language == "العربية" else "Chicken Profits", "أرباح المكافآت والطعام اليومي" if language == "العربية" else "Daily Rewards and Food"])

# قسم الحسابات
if calculation_type == "أرباح الدجاجة" or calculation_type == "Chicken Profits":
    st.subheader("حساب أرباح الدجاجة" if language == "العربية" else "Chicken Profits Calculation")
    col3, col4 = st.columns(2)

    with col3:
        eggs = st.number_input("🥚 عدد البيض" if language == "العربية" else "🥚 Number of Eggs", min_value=0, max_value=580, value=0, help="أدخل عدد البيض (بحد أقصى 580)" if language == "العربية" else "Enter the number of eggs (max 580)", key="eggs")

    with col4:
        days = st.number_input("📅 عدد الأيام" if language == "العربية" else "📅 Number of Days", min_value=0, max_value=730, value=0, help="أدخل عدد الأيام (بحد أقصى 730)" if language == "العربية" else "Enter the number of days (max 730)", key="days")

    if st.button("🧮 احسب أرباح الدجاجة" if language == "العربية" else "🧮 Calculate Chicken Profits", type="primary"):
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

            # إنشاء جدول للنتائج
            results = {
                "العنصر" if language == "العربية" else "Item": [
                    "💰 سعر البيض الكلي" if language == "العربية" else "💰 Total Egg Price",
                    "🌾 تكلفة العلف الكلية" if language == "العربية" else "🌾 Total Feed Cost",
                    "📊 الربح الصافي قبل دفع الإيجار" if language == "العربية" else "📊 Net Profit Before Rent",
                    "🏠 دفع الإيجار للسنة الثانية" if language == "العربية" else "🏠 Rent Cost for Second Year",
                    "💵 الربح الصافي" if language == "العربية" else "💵 Net Profit"
                ],
                "القيمة" if language == "العربية" else "Value": [
                    f"{format_decimal(total_egg_price)} {currency}",
                    f"{format_decimal(total_feed_cost)} {currency}",
                    f"{format_decimal(net_profit_before_rent)} {currency}",
                    f"{format_decimal(rent_cost)} {currency}",
                    f"{format_decimal(net_profit)} {currency}"
                ]
            }

            # عرض النتائج كجدول
            st.success("✅ تم الحساب بنجاح!" if language == "العربية" else "✅ Calculation completed successfully!")
            st.table(pd.DataFrame(results))

elif calculation_type == "أرباح المكافآت والطعام اليومي" or calculation_type == "Daily Rewards and Food":
    st.subheader("حساب أرباح المكافآت والطعام اليومي" if language == "العربية" else "Daily Rewards and Food Calculation")
    col5, col6 = st.columns(2)

    with col5:
        rewards = st.number_input("🎁 عدد المكافآت" if language == "العربية" else "🎁 Number of Rewards", min_value=0, value=0, help="أدخل عدد المكافآت" if language == "العربية" else "Enter the number of rewards", key="rewards")

    with col6:
        food = st.number_input("🍽️ عدد الطعام المطلوب" if language == "العربية" else "🍽️ Amount of Food Required", min_value=0, value=0, help="أدخل عدد الطعام المطلوب" if language == "العربية" else "Enter the amount of food required", key="food")

    if st.button("🧮 احسب أرباح المكافآت والطعام اليومي" if language == "العربية" else "🧮 Calculate Daily Rewards and Food", type="primary"):
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

        # إنشاء جدول للنتائج
        results = {
            "العنصر" if language == "العربية" else "Item": [
                "💰 سعر البيض الكلي" if language == "العربية" else "💰 Total Egg Price",
                "🌾 تكلفة العلف الكلية" if language == "العربية" else "🌾 Total Feed Cost",
                "💵 الربح اليومي" if language == "العربية" else "💵 Daily Profit"
            ],
            "القيمة" if language == "العربية" else "Value": [
                f"{format_decimal(total_egg_price)} {currency}",
                f"{format_decimal(total_feed_cost)} {currency}",
                f"{format_decimal(net_profit)} {currency}"
            ]
        }

        # عرض النتائج كجدول
        st.success("✅ تم الحساب بنجاح!" if language == "العربية" else "✅ Calculation completed successfully!")
        st.table(pd.DataFrame(results))

# قسم تعديل الأسعار
with st.expander("⚙️ تعديل الأسعار" if language == "العربية" else "⚙️ Edit Prices"):
    st.subheader("تعديل الأسعار" if language == "العربية" else "Edit Prices")
    new_egg_price = st.number_input("🥚 سعر البيض الجديد" if language == "العربية" else "🥚 New Egg Price", value=st.session_state.egg_price, format="%.4f")
    new_feed_price = st.number_input("🌾 سعر العلف الجديد" if language == "العربية" else "🌾 New Feed Price", value=st.session_state.feed_price, format="%.4f")

    if st.button("💾 حفظ الأسعار الجديدة" if language == "العربية" else "💾 Save New Prices", type="secondary"):
        st.session_state.egg_price = new_egg_price
        st.session_state.feed_price = new_feed_price
        st.success("✅ تم حفظ الأسعار الجديدة بنجاح!" if language == "العربية" else "✅ New prices saved successfully!")
