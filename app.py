import streamlit as st
import pandas as pd

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تحسين الواجهة
st.set_page_config(page_title="Newyolk Chicken Calculator", page_icon="🐔", layout="wide")

# حالة اللغة (العربية أو الإنجليزية)
if "language" not in st.session_state:
    st.session_state.language = "العربية"

# حالة الوضع (Dark أو Light)
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

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
        f"""
        <style>
        body {{
            background: {'#ffffff' if st.session_state.theme == "Light" else 'linear-gradient(to right, #4B0082, #8A2BE2)'};
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .title {{
            font-size: 50px;
            font-weight: bold;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
            text-align: center;
            padding: 20px;
            direction: rtl;
        }}
        .subtitle {{
            font-size: 30px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
            text-align: center;
            margin-bottom: 30px;
            direction: rtl;
        }}
        .rtl {{
            direction: rtl;
            text-align: right;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stSelectbox, .stNumberInput {{
            direction: rtl;
            text-align: right;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stButton button {{
            font-size: 24px;
        }}
        .stDataFrame {{
            direction: rtl;  /* الجداول تكون من اليمين إلى اليسار */
            text-align: right;
            font-size: 24px;
            margin: 0 auto; /* توسيط الجدول */
        }}
        /* تعديل الزائد والناقص في الأرقام */
        .stNumberInput > div > div > button {{
            margin-left: 0;
            margin-right: 5px;
        }}
        /* زر التمرير إلى الأعلى */
        .scroll-top {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 50%;
            padding: 10px;
            font-size: 18px;
            cursor: pointer;
            display: none;
        }}
        .scroll-top:hover {{
            background-color: #45a049;
        }}
        /* تعديل الجدول ليكون بالكامل من اليمين إلى اليسار */
        .stDataFrame th, .stDataFrame td {{
            text-align: right !important;
            direction: rtl !important;
        }}
        /* توسيط الجدول */
        .stDataFrame {{
            margin: 0 auto;
        }}
        /* جعل الجدول ثابتًا */
        .stDataFrame div[data-testid="stDataFrameContainer"] {{
            overflow: hidden !important;
        }}
        </style>
        <div class="title">🐔 Newyolk - حاسبة الدجاج</div>
        <div class="subtitle">حساب أرباح الدجاج والمكافآت اليومية</div>
        """,
        unsafe_allow_html=True
    )
else:
    st.markdown(
        f"""
        <style>
        body {{
            background: {'#ffffff' if st.session_state.theme == "Light" else 'linear-gradient(to right, #4B0082, #8A2BE2)'};
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .title {{
            font-size: 50px;
            font-weight: bold;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
            text-align: center;
            padding: 20px;
            direction: ltr;
        }}
        .subtitle {{
            font-size: 30px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
            text-align: center;
            margin-bottom: 30px;
            direction: ltr;
        }}
        .ltr {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stSelectbox, .stNumberInput {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stButton button {{
            font-size: 24px;
        }}
        .stDataFrame {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
            margin: 0 auto; /* توسيط الجدول */
        }}
        /* زر التمرير إلى الأعلى */
        .scroll-top {{
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 50%;
            padding: 10px;
            font-size: 18px;
            cursor: pointer;
            display: none;
        }}
        .scroll-top:hover {{
            background-color: #45a049;
        }}
        /* جعل الجدول ثابتًا */
        .stDataFrame div[data-testid="stDataFrameContainer"] {{
            overflow: hidden !important;
        }}
        </style>
        <div class="title">🐔 Newyolk - Chicken Calculator</div>
        <div class="subtitle">Calculate Chicken Profits and Daily Rewards</div>
        """,
        unsafe_allow_html=True
    )

# زر التمرير إلى الأعلى
st.markdown(
    """
    <button onclick="scrollToTop()" class="scroll-top" id="scrollTopBtn" title="Go to top">↑</button>
    <script>
    // ظهور الزر عند التمرير لأسفل
    window.onscroll = function() {scrollFunction()};
    function scrollFunction() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            document.getElementById("scrollTopBtn").style.display = "block";
        } else {
            document.getElementById("scrollTopBtn").style.display = "none";
        }
    }
    // التمرير إلى الأعلى
    function scrollToTop() {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    }
    </script>
    """,
    unsafe_allow_html=True
)

# استخدام الأعمدة لتخطيط أفضل
col1, col2 = st.columns(2)

with col1:
    currency = st.selectbox("💰 العملة" if language == "العربية" else "💰 Currency", ["دولار" if language == "العربية" else "USD", "دينار عراقي" if language == "العربية" else "IQD"])

with col2:
    calculation_type = st.selectbox("📊 نوع الحساب" if language == "العربية" else "📊 Calculation Type", ["أرباح الدجاجة" if language == "العربية" else "Chicken Profits", "أرباح المكافآت والطعام اليومي" if language == "العربية" else "Daily Rewards and Food"])

# قسم الحسابات
if calculation_type == "أرباح الدجاجة" or calculation_type == "Chicken Profits":
    st.subheader("📈 حساب أرباح الدجاجة" if language == "العربية" else "📈 Chicken Profits Calculation")
    col3, col4 = st.columns(2)

    with col3:
        eggs = st.number_input("🥚 عدد البيض" if language == "العربية" else "🥚 Number of Eggs", min_value=0, max_value=580, value=None, help="أدخل عدد البيض (بحد أقصى 580)" if language == "العربية" else "Enter the number of eggs (max 580)", key="eggs")

    with col4:
        days = st.number_input("📅 عدد الأيام" if language == "العربية" else "📅 Number of Days", min_value=0, max_value=730, value=None, help="أدخل عدد الأيام (بحد أقصى 730)" if language == "العربية" else "Enter the number of days (max 730)", key="days")

    if st.button("🧮 احسب أرباح الدجاجة" if language == "العربية" else "🧮 Calculate Chicken Profits", type="primary"):
        if eggs is None or days is None:
            st.error("❗ يرجى إدخال جميع القيم المطلوبة!" if language == "العربية" else "❗ Please enter all required values!")
        elif eggs > 580:
            st.error("❗ عدد البيض يجب ألا يتجاوز 580!" if language == "العربية" else "❗ Number of eggs must not exceed 580!")
        elif days > 730:
            st.error("❗ عدد الأيام يجب ألا يتجاوز 730!" if language == "العربية" else "❗ Number of days must not exceed 730!")
        else:
            # حساب النتائج
            total_egg_price_usd = eggs * st.session_state.egg_price
            total_feed_cost_usd = (days * 2) * st.session_state.feed_price
            net_profit_before_rent_usd = total_egg_price_usd - total_feed_cost_usd

            # حساب تكلفة الإيجار فقط إذا كان عدد الأيام 365 أو أكثر
            rent_cost_usd = 6.0 if days >= 365 else 0.0
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
                    "🌽 تكلفة العلف الكلية" if language == "العربية" else "🌽 Total Feed Cost",
                    "📊 الربح قبل دفع الإيجار" if language == "العربية" else "📊 Net Profit Before Rent",
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
            df = pd.DataFrame(results)
            if language == "العربية":
                df = df[["القيمة", "العنصر"]]  # تغيير ترتيب الأعمدة للغة العربية
            st.dataframe(df.style.set_properties(**{'text-align': 'right', 'direction': 'rtl'}))

elif calculation_type == "أرباح المكافآت والطعام اليومي" or calculation_type == "Daily Rewards and Food":
    st.subheader("📈 حساب أرباح المكافآت والطعام اليومي" if language == "العربية" else "📈 Daily Rewards and Food Calculation")
    col5, col6 = st.columns(2)

    with col5:
        rewards = st.number_input("🎁 عدد المكافآت" if language == "العربية" else "🎁 Number of Rewards", min_value=0, value=None, help="أدخل عدد المكافآت" if language == "العربية" else "Enter the number of rewards", key="rewards")

    with col6:
        food = st.number_input("🌽 عدد الطعام المطلوب" if language == "العربية" else "🌽 Amount of Food Required", min_value=0, value=None, help="أدخل عدد الطعام المطلوب" if language == "العربية" else "Enter the amount of food required", key="food")

    if st.button("🧮 احسب أرباح المكافآت والطعام اليومي" if language == "العربية" else "🧮 Calculate Daily Rewards and Food", type="primary"):
        if rewards is None or food is None:
            st.error("❗ يرجى إدخال جميع القيم المطلوبة!" if language == "العربية" else "❗ Please enter all required values!")
        else:
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
                    "🌽 تكلفة العلف الكلية" if language == "العربية" else "🌽 Total Feed Cost",
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
            df = pd.DataFrame(results)
            if language == "العربية":
                df = df[["القيمة", "العنصر"]]  # تغيير ترتيب الأعمدة للغة العربية
            st.dataframe(df.style.set_properties(**{'text-align': 'right', 'direction': 'rtl'}))

# قسم تعديل الأسعار
with st.expander("⚙️ تعديل الأسعار" if language == "العربية" else "⚙️ Edit Prices"):
    st.subheader("⚙️ تعديل الأسعار" if language == "العربية" else "⚙️ Edit Prices")
    new_egg_price = st.number_input("🥚 سعر البيض الجديد" if language == "العربية" else "🥚 New Egg Price", value=st.session_state.egg_price, format="%.4f")
    new_feed_price = st.number_input("🌽 سعر العلف الجديد" if language == "العربية" else "🌽 New Feed Price", value=st.session_state.feed_price, format="%.4f")

    if st.button("💾 حفظ الأسعار الجديدة" if language == "العربية" else "💾 Save New Prices", type="secondary"):
        st.session_state.egg_price = new_egg_price
        st.session_state.feed_price = new_feed_price
        st.success("✅ تم حفظ الأسعار الجديدة بنجاح!" if language == "العربية" else "✅ New prices saved successfully!")

# زر إعادة التعيين
if st.button("🔄 إعادة التعيين" if language == "العربية" else "🔄 Reset", type="secondary"):
    st.session_state.egg_price = 0.1155
    st.session_state.feed_price = 0.0189
    st.success("✅ تم إعادة التعيين بنجاح!" if language == "العربية" else "✅ Reset completed successfully!")

# إضافة نص حقوق النشر
st.markdown(
    """
    <div style="text-align: center; font-size: 16px; color: gray; margin-top: 50px;">
        جميع الحقوق محفوظة © 2025 by Tariq Al-Yaseen
    </div>
    """,
    unsafe_allow_html=True
)
