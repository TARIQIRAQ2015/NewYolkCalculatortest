import streamlit as st
import pandas as pd
import plotly.express as px

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تحسين الواجهة
st.set_page_config(page_title="Newyolk Chicken Calculator", page_icon="🐔", layout="wide")

# حالة اللغة (العربية، الإنجليزية، الرومانية)
if "language" not in st.session_state:
    st.session_state.language = "العربية"

# حالة الوضع (Dark أو Light)
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# الأسعار المبدئية
if "egg_price" not in st.session_state:
    st.session_state.egg_price = 0.1155
if "feed_price" not in st.session_state:
    st.session_state.feed_price = 0.0189

# حالة الحقول (لإعادة التعيين)
if "eggs" not in st.session_state:
    st.session_state.eggs = ""
if "days" not in st.session_state:
    st.session_state.days = ""
if "rewards" not in st.session_state:
    st.session_state.rewards = ""
if "food" not in st.session_state:
    st.session_state.food = ""

# تغيير اتجاه الكتابة بناءً على اللغة
if st.session_state.language == "العربية":
    st.markdown(
        f"""
        <style>
        body {{
            background: {'#ffffff' if st.session_state.theme == "Light" else 'linear-gradient(to right, #4B0082, #8A2BE2)'};
            color: {'black' if st.session_state.theme == "Light" else 'white'};
            direction: rtl;
        }}
        .title {{
            font-size: 50px;
            font-weight: bold;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
            text-align: center;
            padding: 20px;
        }}
        .subtitle {{
            font-size: 30px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
            text-align: center;
            margin-bottom: 30px;
        }}
        .rtl {{
            direction: rtl;
            text-align: right;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stSelectbox, .stTextInput {{
            direction: rtl;
            text-align: right;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stButton button {{
            font-size: 24px;
        }}
        .stTable {{
            margin: 0 auto; /* توسيط الجدول */
            width: 50%; /* تحديد عرض الجدول */
            text-align: right; /* محاذاة النص إلى اليمين */
        }}
        .stTable th, .stTable td {{
            text-align: right !important; /* محاذاة النص داخل الخلايا إلى اليمين */
            direction: rtl !important; /* اتجاه النص من اليمين إلى اليسار */
        }}
        .scroll-top {{
            display: none;
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99;
            font-size: 18px;
            border: none;
            outline: none;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            padding: 15px;
            border-radius: 50%;
        }}
        .scroll-top:hover {{
            background-color: #45a049;
        }}
        </style>
        <div class="title"> 🐔 حاسبة الدجاج - Newyolk</div>
        <div class="subtitle">حساب أرباح الدجاج والمكافآت اليومية</div>
        """,
        unsafe_allow_html=True
    )
elif st.session_state.language == "English":
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
        }}
        .subtitle {{
            font-size: 30px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
            text-align: center;
            margin-bottom: 30px;
        }}
        .ltr {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stSelectbox, .stTextInput {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stButton button {{
            font-size: 24px;
        }}
        .stTable {{
            margin: 0 auto; /* توسيط الجدول */
            width: 50%; /* تحديد عرض الجدول */
            text-align: left; /* محاذاة النص إلى اليسار */
        }}
        .scroll-top {{
            display: none;
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99;
            font-size: 18px;
            border: none;
            outline: none;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            padding: 15px;
            border-radius: 50%;
        }}
        .scroll-top:hover {{
            background-color: #45a049;
        }}
        </style>
        <div class="title">🐔 Newyolk - Chicken Calculator</div>
        <div class="subtitle">Calculate Chicken Profits and Daily Rewards</div>
        """,
        unsafe_allow_html=True
    )
else:  # اللغة الرومانية
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
        }}
        .subtitle {{
            font-size: 30px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
            text-align: center;
            margin-bottom: 30px;
        }}
        .ltr {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stSelectbox, .stTextInput {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stButton button {{
            font-size: 24px;
        }}
        .stTable {{
            margin: 0 auto; /* توسيط الجدول */
            width: 50%; /* تحديد عرض الجدول */
            text-align: left; /* محاذاة النص إلى اليسار */
        }}
        .scroll-top {{
            display: none;
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99;
            font-size: 18px;
            border: none;
            outline: none;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            padding: 15px;
            border-radius: 50%;
        }}
        .scroll-top:hover {{
            background-color: #45a049;
        }}
        </style>
        <div class="title">🐔 Newyolk - Calculator de Pui</div>
        <div class="subtitle">Calculează Profiturile și Recompensele Zilnice</div>
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
    st.session_state.language = st.selectbox(
        "اختر اللغة / Choose Language / Alegeți limba", 
        ["العربية", "English", "Română"],
        key="language_selectbox"
    )

with col2:
    currency = st.selectbox(
        "العملة 💰" if st.session_state.language == "العربية" else "💰 Currency" if st.session_state.language == "English" else "💰 Monedă",
        ["دولار أمريكي" if st.session_state.language == "العربية" else "USD" if st.session_state.language == "English" else "USD", "دينار عراقي" if st.session_state.language == "العربية" else "IQD" if st.session_state.language == "English" else "IQD"],
        key="currency_selectbox"
    )

# قسم تعديل الأسعار
st.subheader("تعديل الأسعار ⚙️" if st.session_state.language == "العربية" else "⚙️ Edit Prices" if st.session_state.language == "English" else "⚙️ Editează Prețuri")
col3, col4 = st.columns(2)

with col3:
    new_egg_price = st.text_input(
        "سعر البيض الحالي 🥚" if st.session_state.language == "العربية" else "🥚 New Egg Price" if st.session_state.language == "English" else "🥚 Prețul Nou al Ouălor", 
        value=str(st.session_state.egg_price),
        key="new_egg_price_input"
    )

with col4:
    new_feed_price = st.text_input(
        "سعر العلف الحالي 🌽" if st.session_state.language == "العربية" else "🌽 New Feed Price" if st.session_state.language == "English" else "🌽 Prețul Nou al Furajului", 
        value=str(st.session_state.feed_price),
        key="new_feed_price_input"
    )

if st.button("حفظ الأسعار الجديدة 💾" if st.session_state.language == "العربية" else "💾 Save New Prices" if st.session_state.language == "English" else "💾 Salvează Prețurile Noi", type="secondary"):
    try:
        st.session_state.egg_price = float(new_egg_price)
        st.session_state.feed_price = float(new_feed_price)
        st.session_state.chicken_price = float(new_chicken_price)
        st.success("تم حفظ الأسعار الجديدة بنجاح! ✅" if st.session_state.language == "العربية" else "✅ New prices saved successfully!" if st.session_state.language == "English" else "✅ Prețurile noi au fost salvate cu succes!")
    except ValueError:
        st.error("يرجى إدخال أرقام صحيحة! ❗" if st.session_state.language == "العربية" else "❗ Please enter valid numbers!" if st.session_state.language == "English" else "❗ Vă rugăm să introduceți numere valide!")

# قسم الحسابات
calculation_type = st.selectbox(
    "نوع الحساب 📊" if st.session_state.language == "العربية" else "📊 Calculation Type" if st.session_state.language == "English" else "📊 Tip de Calcul",
    ["أرباح الدجاجة" if st.session_state.language == "العربية" else "Chicken Profits" if st.session_state.language == "English" else "Profituri Pui", "أرباح المكافآت والطعام اليومي" if st.session_state.language == "العربية" else "Daily Rewards and Food" if st.session_state.language == "English" else "Recompense Zilnice și Mâncare"],
    key="calculation_type_selectbox"
)

if calculation_type == "أرباح الدجاجة" or calculation_type == "Chicken Profits" or calculation_type == "Profituri Pui":
    st.subheader("حساب أرباح الدجاجة 📈" if st.session_state.language == "العربية" else "📈 Chicken Profits Calculation" if st.session_state.language == "English" else "📈 Calcul Profituri Pui")
    col5, col6 = st.columns(2)

    with col5:
        eggs = st.text_input(
            "عدد البيض 🥚" if st.session_state.language == "العربية" else "🥚 Number of Eggs" if st.session_state.language == "English" else "🥚 Numărul de Ouă",
            value=st.session_state.eggs,
            help="أدخل عدد البيض (بحد أقصى 580)" if st.session_state.language == "العربية" else "Enter the number of eggs (max 580)" if st.session_state.language == "English" else "Introduceți numărul de ouă (max 580)",
            key="eggs_input"
        )

    with col6:
        days = st.text_input(
            "عدد الأيام 📅" if st.session_state.language == "العربية" else "📅 Number of Days" if st.session_state.language == "English" else "📅 Numărul de Zile",
            value=st.session_state.days,
            help="أدخل عدد الأيام (بحد أقصى 730)" if st.session_state.language == "العربية" else "Enter the number of days (max 730)" if st.session_state.language == "English" else "Introduceți numărul de zile (max 730)",
            key="days_input"
        )

    # إضافة حقل لإدخال سعر شراء الدجاجة
    chicken_price = st.text_input(
        "سعر شراء الدجاجة 🐔" if st.session_state.language == "العربية" else "🐔 Chicken Purchase Price" if st.session_state.language == "English" else "🐔 Prețul de Achiziție al Puiului",
        value=str(st.session_state.chicken_price),
        help="أدخل سعر شراء الدجاجة(اختياري)" if st.session_state.language == "العربية" else "Enter the chicken purchase price" if st.session_state.language == "English" else "Introduceți prețul de achiziție al puiului",
        key="chicken_price_input"
    )

    if st.button("احسب أرباح الدجاجة 🧮" if st.session_state.language == "العربية" else "🧮 Calculate Chicken Profits" if st.session_state.language == "English" else "🧮 Calculează Profiturile Pui", type="primary"):
        try:
            eggs = float(eggs) if eggs else None
            days = float(days) if days else None
            chicken_price = float(chicken_price) if chicken_price else 0.0

            if eggs is None or days is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗" if st.session_state.language == "العربية" else "❗ Please enter all required values!" if st.session_state.language == "English" else "❗ Vă rugăm să introduceți toate valorile necesare!")
            elif eggs > 580:
                st.error("عدد البيض يجب ألا يتجاوز 580! ❗" if st.session_state.language == "العربية" else "❗ Number of eggs must not exceed 580!" if st.session_state.language == "English" else "❗ Numărul de ouă nu trebuie să depășească 580!")
            elif days > 730:
                st.error("عدد الأيام يجب ألا يتجاوز 730! ❗" if st.session_state.language == "العربية" else "❗ Number of days must not exceed 730!" if st.session_state.language == "English" else "❗ Numărul de zile nu trebuie să depășească 730!")
            else:
                # حساب النتائج
                total_egg_price_usd = eggs * st.session_state.egg_price
                total_feed_cost_usd = (days * 2) * st.session_state.feed_price
                net_profit_before_rent_usd = total_egg_price_usd - total_feed_cost_usd

                # حساب تكلفة الإيجار فقط إذا كان عدد الأيام 365 أو أكثر
                rent_cost_usd = 6.0 if days >= 365 else 0.0
                net_profit_usd = net_profit_before_rent_usd - rent_cost_usd - chicken_price

                if currency == "دينار عراقي" or currency == "IQD":
                    total_egg_price = total_egg_price_usd * 1480
                    total_feed_cost = total_feed_cost_usd * 1480
                    net_profit_before_rent = net_profit_before_rent_usd * 1480
                    rent_cost = rent_cost_usd * 1480
                    chicken_price_converted = chicken_price * 1480
                    net_profit = net_profit_usd * 1480
                else:
                    total_egg_price, total_feed_cost, net_profit_before_rent, rent_cost, chicken_price_converted, net_profit = (
                        total_egg_price_usd, total_feed_cost_usd, net_profit_before_rent_usd, rent_cost_usd, chicken_price, net_profit_usd
                    )

                # إنشاء جدول للنتائج
                results = {
                    "العنصر" if st.session_state.language == "العربية" else "Item" if st.session_state.language == "English" else "Element": [
                        "سعر البيض الكلي 💰" if st.session_state.language == "العربية" else "💰 Total Egg Price" if st.session_state.language == "English" else "💰 Prețul Total al Ouălor",
                        "تكلفة العلف الكلية 🌽" if st.session_state.language == "العربية" else "🌽 Total Feed Cost" if st.session_state.language == "English" else "🌽 Costul Total al Furajului",
                        "الربح قبل خصم الإيجار 📊" if st.session_state.language == "العربية" else "📊 Net Profit Before Rent" if st.session_state.language == "English" else "📊 Profit Net înainte de Chirii",
                        "دفع الإيجار للسنة الثانية 💸" if st.session_state.language == "العربية" else "🏠 Rent Cost for Second Year" if st.session_state.language == "English" else "🏠 Costul Chiriei pentru Anul Doi",
                        "سعر شراء الدجاجة 🐔" if st.session_state.language == "العربية" else "🐔 Chicken Purchase Price" if st.session_state.language == "English" else "🐔 Prețul de Achiziție al Puiului",
                        "الربح الصافي 💵" if st.session_state.language == "العربية" else "💵 Net Profit" if st.session_state.language == "English" else "💵 Profit Net"
                    ],
                    "القيمة" if st.session_state.language == "العربية" else "Value" if st.session_state.language == "English" else "Valoare": [
                        f"{format_decimal(total_egg_price)} {currency}",
                        f"{format_decimal(total_feed_cost)} {currency}",
                        f"{format_decimal(net_profit_before_rent)} {currency}",
                        f"{format_decimal(rent_cost)} {currency}",
                        f"{format_decimal(chicken_price_converted)} {currency}",
                        f"{format_decimal(net_profit)} {currency}"
                    ]
                }

                # عرض النتائج كجدول
                st.success("تم الحساب بنجاح! ✅" if st.session_state.language == "العربية" else "✅ Calculation completed successfully!" if st.session_state.language == "English" else "✅ Calcul finalizat cu succes!")
                df = pd.DataFrame(results)
                if st.session_state.language == "العربية":
                    df = df[["العنصر", "القيمة"]]  # تغيير ترتيب الأعمدة للغة العربية
                st.table(df)

                # إضافة رسم بياني دائري
                chart_data = pd.DataFrame({
                    "الفئة" if st.session_state.language == "العربية" else "Category" if st.session_state.language == "English" else "Categorie": [
                        "سعر البيض الكلي" if st.session_state.language == "العربية" else "Total Egg Price" if st.session_state.language == "English" else "Prețul Total al Ouălor",
                        "تكلفة العلف الكلية" if st.session_state.language == "العربية" else "Total Feed Cost" if st.session_state.language == "English" else "Costul Total al Furajului",
                        "دفع الإيجار" if st.session_state.language == "العربية" else "Rent Cost" if st.session_state.language == "English" else "Costul Chiriei",
                        "سعر شراء الدجاجة" if st.session_state.language == "العربية" else "Chicken Purchase Price" if st.session_state.language == "English" else "Prețul de Achiziție al Puiului"
                    ],
                    "القيمة" if st.session_state.language == "العربية" else "Value" if st.session_state.language == "English" else "Valoare": [
                        total_egg_price,
                        total_feed_cost,
                        rent_cost,
                        chicken_price_converted
                    ]
                })

                fig = px.pie(chart_data, values="القيمة" if st.session_state.language == "العربية" else "Value", names="الفئة" if st.session_state.language == "العربية" else "Category",
                             title="توزيع التكاليف والأرباح" if st.session_state.language == "العربية" else "Distribution of Costs and Profits" if st.session_state.language == "English" else "Distribuția Costurilor și Profiturilor",
                             color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig, use_container_width=True)

        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗" if st.session_state.language == "العربية" else "❗ Please enter valid numbers!" if st.session_state.language == "English" else "❗ Vă rugăm să introduceți numere valide!")

elif calculation_type == "أرباح المكافآت والطعام اليومي" or calculation_type == "Daily Rewards and Food" or calculation_type == "Recompense Zilnice și Mâncare":
    st.subheader("حساب أرباح المكافآت والطعام اليومي 📈" if st.session_state.language == "العربية" else "📈 Daily Rewards and Food Calculation" if st.session_state.language == "English" else "📈 Calcul Recompense Zilnice și Mâncare")
    col7, col8 = st.columns(2)

    with col7:
        rewards = st.text_input(
            "عدد المكافآت 🎁" if st.session_state.language == "العربية" else "🎁 Number of Rewards" if st.session_state.language == "English" else "🎁 Numărul de Recompense",
            value=st.session_state.rewards,
            help="أدخل عدد المكافآت" if st.session_state.language == "العربية" else "Enter the number of rewards" if st.session_state.language == "English" else "Introduceți numărul de recompense",
            key="rewards_input"
        )

    with col8:
        food = st.text_input(
            "عدد الطعام المطلوب 🌽" if st.session_state.language == "العربية" else "🌽 Amount of Food Required" if st.session_state.language == "English" else "🌽 Cantitatea de Mâncare Necesară",
            value=st.session_state.food,
            help="أدخل عدد الطعام المطلوب" if st.session_state.language == "العربية" else "Enter the amount of food required" if st.session_state.language == "English" else "Introduceți cantitatea de mâncare necesară",
            key="food_input"
        )

    if st.button("احسب أرباح المكافآت والطعام اليومي 🧮" if st.session_state.language == "العربية" else "🧮 Calculate Daily Rewards and Food" if st.session_state.language == "English" else "🧮 Calculează Recompense Zilnice și Mâncare", type="primary"):
        try:
            rewards = float(rewards) if rewards else None
            food = float(food) if food else None

            if rewards is None or food is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗" if st.session_state.language == "العربية" else "❗ Please enter all required values!" if st.session_state.language == "English" else "❗ Vă rugăm să introduceți toate valorile necesare!")
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
                    "العنصر" if st.session_state.language == "العربية" else "Item" if st.session_state.language == "English" else "Element": [
                        "سعر البيض الكلي 💰" if st.session_state.language == "العربية" else "💰 Total Egg Price" if st.session_state.language == "English" else "💰 Prețul Total al Ouălor",
                        "تكلفة العلف الكلية 🌽" if st.session_state.language == "العربية" else "🌽 Total Feed Cost" if st.session_state.language == "English" else "🌽 Costul Total al Furajului",
                        "الربح اليومي 💵" if st.session_state.language == "العربية" else "💵 Daily Profit" if st.session_state.language == "English" else "💵 Profit Zilnic"
                    ],
                    "القيمة" if st.session_state.language == "العربية" else "Value" if st.session_state.language == "English" else "Valoare": [
                        f"{format_decimal(total_egg_price)} {currency}",
                        f"{format_decimal(total_feed_cost)} {currency}",
                        f"{format_decimal(net_profit)} {currency}"
                    ]
                }

                # عرض النتائج كجدول
                st.success("تم الحساب بنجاح! ✅" if st.session_state.language == "العربية" else "✅ Calculation completed successfully!" if st.session_state.language == "English" else "✅ Calcul finalizat cu succes!")
                df = pd.DataFrame(results)
                if st.session_state.language == "العربية":
                    df = df[["العنصر", "القيمة"]]  # تغيير ترتيب الأعمدة للغة العربية
                st.table(df)

                # إضافة رسم بياني دائري
                chart_data = pd.DataFrame({
                    "الفئة" if st.session_state.language == "العربية" else "Category" if st.session_state.language == "English" else "Categorie": [
                        "سعر البيض الكلي" if st.session_state.language == "العربية" else "Total Egg Price" if st.session_state.language == "English" else "Prețul Total al Ouălor",
                        "تكلفة العلف الكلية" if st.session_state.language == "العربية" else "Total Feed Cost" if st.session_state.language == "English" else "Costul Total al Furajului"
                    ],
                    "القيمة" if st.session_state.language == "العربية" else "Value" if st.session_state.language == "English" else "Valoare": [
                        total_egg_price,
                        total_feed_cost
                    ]
                })

                fig = px.pie(chart_data, values="القيمة" if st.session_state.language == "العربية" else "Value", names="الفئة" if st.session_state.language == "العربية" else "Category",
                             title="توزيع التكاليف والأرباح" if st.session_state.language == "العربية" else "Distribution of Costs and Profits" if st.session_state.language == "English" else "Distribuția Costurilor și Profiturilor",
                             color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig, use_container_width=True)

        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗" if st.session_state.language == "العربية" else "❗ Please enter valid numbers!" if st.session_state.language == "English" else "❗ Vă rugăm să introduceți numere valide!")

# زر إعادة التعيين
if st.button("إعادة التعيين 🔄" if st.session_state.language == "العربية" else "🔄 Reset" if st.session_state.language == "English" else "🔄 Resetează", type="secondary"):
    st.session_state.egg_price = 0.1155
    st.session_state.feed_price = 0.0189
    st.session_state.chicken_price = 0.0
    st.session_state.eggs = ""
    st.session_state.days = ""
    st.session_state.rewards = ""
    st.session_state.food = ""
    st.success("تم إعادة التعيين بنجاح! ✅" if st.session_state.language == "العربية" else "✅ Reset completed successfully!" if st.session_state.language == "English" else "✅ Resetare finalizată cu succes!")

# إضافة نص حقوق النشر
st.markdown(
    """
    <div style="text-align: center; font-size: 16px; color: gray; margin-top: 50px; font-weight: bold;">
       by Tariq Al-Yaseen © 2025-2026
    </div>
    """,
    unsafe_allow_html=True
)
