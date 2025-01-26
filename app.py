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
if "chicken_price" not in st.session_state:
    st.session_state.chicken_price = 0.0  # سعر شراء الدجاجة

# حالة الحقول (لإعادة التعيين)
if "eggs" not in st.session_state:
    st.session_state.eggs = ""
if "days" not in st.session_state:
    st.session_state.days = ""
if "rewards" not in st.session_state:
    st.session_state.rewards = ""
if "food" not in st.session_state:
    st.session_state.food = ""

# النصوص لكل لغة
texts = {
    "العربية": {
        "title": "🐔 حاسبة الدجاج - Newyolk",
        "subtitle": "حساب أرباح الدجاج والمكافآت اليومية",
        "language_select": "اختر اللغة",
        "currency_select": "العملة 💰",
        "edit_prices": "تعديل الأسعار ⚙️",
        "new_egg_price": "سعر البيض الحالي 🥚",
        "new_feed_price": "سعر العلف الحالي 🌽",
        "save_prices": "حفظ الأسعار الجديدة 💾",
        "calculation_type": "نوع الحساب 📊",
        "chicken_profits": "أرباح الدجاجة",
        "daily_rewards": "أرباح المكافآت والطعام اليومي",
        "eggs_input": "عدد البيض 🥚",
        "days_input": "عدد الأيام 📅",
        "chicken_price_input": "سعر شراء الدجاجة 🐔",
        "calculate_profits": "احسب أرباح الدجاجة 🧮",
        "rewards_input": "عدد المكافآت 🎁",
        "food_input": "عدد الطعام المطلوب 🌽",
        "calculate_rewards": "احسب أرباح المكافآت والطعام اليومي 🧮",
        "reset": "إعادة التعيين 🔄",
        "copyright": "by Tariq Al-Yaseen © 2025-2026"
    },
    "English": {
        "title": "🐔 Newyolk - Chicken Calculator",
        "subtitle": "Calculate Chicken Profits and Daily Rewards",
        "language_select": "Choose Language",
        "currency_select": "💰 Currency",
        "edit_prices": "⚙️ Edit Prices",
        "new_egg_price": "🥚 New Egg Price",
        "new_feed_price": "🌽 New Feed Price",
        "save_prices": "💾 Save New Prices",
        "calculation_type": "📊 Calculation Type",
        "chicken_profits": "Chicken Profits",
        "daily_rewards": "Daily Rewards and Food",
        "eggs_input": "🥚 Number of Eggs",
        "days_input": "📅 Number of Days",
        "chicken_price_input": "🐔 Chicken Purchase Price",
        "calculate_profits": "🧮 Calculate Chicken Profits",
        "rewards_input": "🎁 Number of Rewards",
        "food_input": "🌽 Amount of Food Required",
        "calculate_rewards": "🧮 Calculate Daily Rewards and Food",
        "reset": "🔄 Reset",
        "copyright": "by Tariq Al-Yaseen © 2025-2026"
    },
    "Română": {
        "title": "🐔 Newyolk - Calculator de Pui",
        "subtitle": "Calculează Profiturile și Recompensele Zilnice",
        "language_select": "Alegeți limba",
        "currency_select": "💰 Monedă",
        "edit_prices": "⚙️ Editează Prețuri",
        "new_egg_price": "🥚 Prețul Nou al Ouălor",
        "new_feed_price": "🌽 Prețul Nou al Furajului",
        "save_prices": "💾 Salvează Prețurile Noi",
        "calculation_type": "📊 Tip de Calcul",
        "chicken_profits": "Profituri Pui",
        "daily_rewards": "Recompense Zilnice și Mâncare",
        "eggs_input": "🥚 Numărul de Ouă",
        "days_input": "📅 Numărul de Zile",
        "chicken_price_input": "🐔 Prețul de Achiziție al Puiului",
        "calculate_profits": "🧮 Calculează Profiturile Pui",
        "rewards_input": "🎁 Numărul de Recompense",
        "food_input": "🌽 Cantitatea de Mâncare Necesară",
        "calculate_rewards": "🧮 Calculează Recompense Zilnice și Mâncare",
        "reset": "🔄 Resetează",
        "copyright": "by Tariq Al-Yaseen © 2025-2026"
    }
}

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
        <div class="title"> {texts[st.session_state.language]["title"]}</div>
        <div class="subtitle">{texts[st.session_state.language]["subtitle"]}</div>
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
        <div class="title">{texts[st.session_state.language]["title"]}</div>
        <div class="subtitle">{texts[st.session_state.language]["subtitle"]}</div>
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
    language = st.selectbox(texts[st.session_state.language]["language_select"], ["العربية", "English", "Română"], key="language_selectbox")

with col2:
    currency = st.selectbox(
        texts[st.session_state.language]["currency_select"],
        ["دولار أمريكي" if language == "العربية" else "USD" if language == "English" else "USD", "دينار عراقي" if language == "العربية" else "IQD" if language == "English" else "IQD"]
    )

# قسم تعديل الأسعار
st.subheader(texts[st.session_state.language]["edit_prices"])
col3, col4 = st.columns(2)

with col3:
    new_egg_price = st.text_input(texts[st.session_state.language]["new_egg_price"], value=str(st.session_state.egg_price))

with col4:
    new_feed_price = st.text_input(texts[st.session_state.language]["new_feed_price"], value=str(st.session_state.feed_price))

if st.button(texts[st.session_state.language]["save_prices"], type="secondary"):
    try:
        st.session_state.egg_price = float(new_egg_price)
        st.session_state.feed_price = float(new_feed_price)
        st.success("تم حفظ الأسعار الجديدة بنجاح! ✅" if language == "العربية" else "✅ New prices saved successfully!" if language == "English" else "✅ Prețurile noi au fost salvate cu succes!")
    except ValueError:
        st.error("يرجى إدخال أرقام صحيحة! ❗️" if language == "العربية" else "❗️ Please enter valid numbers!" if language == "English" else "❗️ Vă rugăm să introduceți numere valide!")

# قسم الحسابات
calculation_type = st.selectbox(
    texts[st.session_state.language]["calculation_type"],
    [texts[st.session_state.language]["chicken_profits"], texts[st.session_state.language]["daily_rewards"]]
)

if calculation_type == texts[st.session_state.language]["chicken_profits"]:
    st.subheader("حساب أرباح الدجاجة 📈" if language == "العربية" else "📈 Chicken Profits Calculation" if language == "English" else "📈 Calcul Profituri Pui")
    col5, col6 = st.columns(2)

    with col5:
        eggs = st.text_input(
            texts[st.session_state.language]["eggs_input"],
            value=st.session_state.eggs,
            help="أدخل عدد البيض (بحد أقصى 580)" if language == "العربية" else "Enter the number of eggs (max 580)" if language == "English" else "Introduceți numărul de ouă (max 580)",
            key="eggs_input"
        )

    with col6:
        days = st.text_input(
            texts[st.session_state.language]["days_input"],
            value=st.session_state.days,
            help="أدخل عدد الأيام (بحد أقصى 730)" if language == "العربية" else "Enter the number of days (max 730)" if language == "English" else "Introduceți numărul de zile (max 730)",
            key="days_input"
        )

    # إضافة حقل لإدخال سعر شراء الدجاجة
    chicken_price = st.text_input(
        texts[st.session_state.language]["chicken_price_input"],
        value=str(st.session_state.chicken_price),
        help="أدخل سعر شراء الدجاجة(اختياري)" if language == "العربية" else "Enter the chicken purchase price" if language == "English" else "Introduceți prețul de achiziție al puiului",
        key="chicken_price_input"
    )

    # زر الحساب وإعادة التعيين في نفس الصف
    col7, col8 = st.columns([3, 1])
    with col7:
        if st.button(texts[st.session_state.language]["calculate_profits"], type="primary"):
            try:
                eggs = float(eggs) if eggs else None
                days = float(days) if days else None
                chicken_price = float(chicken_price) if chicken_price else 0.0

                if eggs is None or days is None:
                    st.error("يرجى إدخال جميع القيم المطلوبة! ❗️" if language == "العربية" else "❗️ Please enter all required values!" if language == "English" else "❗️ Vă rugăm să introduceți toate valorile necesare!")
                elif eggs > 580:
                    st.error("عدد البيض يجب ألا يتجاوز 580! ❗️" if language == "العربية" else "❗️ Number of eggs must not exceed 580!" if language == "English" else "❗️ Numărul de ouă nu trebuie să depășească 580!")
                elif days > 730:
                    st.error("عدد الأيام يجب ألا يتجاوز 730! ❗️" if language == "العربية" else "❗️ Number of days must not exceed 730!" if language == "English" else "❗️ Numărul de zile nu trebuie să depășească 730!")
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
                        "العنصر" if language == "العربية" else "Item" if language == "English" else "Element": [
                            "سعر البيض الكلي 💰" if language == "العربية" else "💰 Total Egg Price" if language == "English" else "💰 Prețul Total al Ouălor",
                            "تكلفة العلف الكلية 🌽" if language == "العربية" else "🌽 Total Feed Cost" if language == "English" else "🌽 Costul Total al Furajului",
                            "الربح قبل خصم الإيجار 📊" if language == "العربية" else "📊 Net Profit Before Rent" if language == "English" else "📊 Profit Net înainte de Chirii",
                            "دفع الإيجار للسنة الثانية 💸" if language == "العربية" else "🏠 Rent Cost for Second Year" if language == "English" else "🏠 Costul Chiriei pentru Anul Doi",
                            "سعر شراء الدجاجة 🐔" if language == "العربية" else "🐔 Chicken Purchase Price" if language == "English" else "🐔 Prețul de Achiziție al Puiului",
                            "الربح الصافي 💵" if language == "العربية" else "💵 Net Profit" if language == "English" else "💵 Profit Net"
                        ],
                        "القيمة" if language == "العربية" else "Value" if language == "English" else "Valoare": [
                            f"{format_decimal(total_egg_price)} {currency}",
                            f"{format_decimal(total_feed_cost)} {currency}",
                            f"{format_decimal(net_profit_before_rent)} {currency}",
                            f"{format_decimal(rent_cost)} {currency}",
                            f"{format_decimal(chicken_price_converted)} {currency}",
                            f"{format_decimal(net_profit)} {currency}"
                        ]
                    }

                    # عرض النتائج كجدول
                    st.success("تم الحساب بنجاح! ✅" if language == "العربية" else "✅ Calculation completed successfully!" if language == "English" else "✅ Calcul finalizat cu succes!")
                    df = pd.DataFrame(results)
                    if language == "العربية":
                        df = df[["العنصر", "القيمة"]]  # تغيير ترتيب الأعمدة للغة العربية
                    st.table(df)

                    # إضافة رسم بياني شريطي
                    chart_data = pd.DataFrame({
                        "الفئة" if language == "العربية" else "Category" if language == "English" else "Categorie": [
                            "سعر البيض الكلي" if language == "العربية" else "Total Egg Price" if language == "English" else "Prețul Total al Ouălor",
                            "تكلفة العلف الكلية" if language == "العربية" else "Total Feed Cost" if language == "English" else "Costul Total al Furajului",
                            "دفع الإيجار" if language == "العربية" else "Rent Cost" if language == "English" else "Costul Chiriei",
                            "سعر شراء الدجاجة" if language == "العربية" else "Chicken Purchase Price" if language == "English" else "Prețul de Achiziție al Puiului"
                        ],
                        "القيمة" if language == "العربية" else "Value" if language == "English" else "Valoare": [
                            total_egg_price,
                            total_feed_cost,
                            rent_cost,
                            chicken_price_converted
                        ]
                    })

                    fig = px.bar(chart_data, x="الفئة" if language == "العربية" else "Category", y="القيمة" if language == "العربية" else "Value",
                                 title="توزيع التكاليف والأرباح" if language == "العربية" else "Distribution of Costs and Profits" if language == "English" else "Distribuția Costurilor și Profiturilor",
                                 color="الفئة" if language == "العربية" else "Category",
                                 color_discrete_sequence=px.colors.qualitative.Pastel)
                    st.plotly_chart(fig, use_container_width=True)

            except ValueError:
                st.error("يرجى إدخال أرقام صحيحة! ❗️" if language == "العربية" else "❗️ Please enter valid numbers!" if language == "English" else "❗️ Vă rugăm să introduceți numere valide!")

    with col8:
        if st.button(texts[st.session_state.language]["reset"], type="secondary"):
            st.session_state.egg_price = 0.1155
            st.session_state.feed_price = 0.0189
            st.session_state.chicken_price = 0.0
            st.session_state.eggs = ""
            st.session_state.days = ""
            st.session_state.rewards = ""
            st.session_state.food = ""
            st.success("تم إعادة التعيين بنجاح! ✅" if language == "العربية" else "✅ Reset completed successfully!" if language == "English" else "✅ Resetare finalizată cu succes!")

elif calculation_type == texts[st.session_state.language]["daily_rewards"]:
    st.subheader("حساب أرباح المكافآت والطعام اليومي 📈" if language == "العربية" else "📈 Daily Rewards and Food Calculation" if language == "English" else "📈 Calcul Recompense Zilnice și Mâncare")
    col7, col8 = st.columns(2)

    with col7:
        rewards = st.text_input(
            texts[st.session_state.language]["rewards_input"],
            value=st.session_state.rewards,
            help="أدخل عدد المكافآت" if language == "العربية" else "Enter the number of rewards" if language == "English" else "Introduceți numărul de recompense",
            key="rewards_input"
        )

    with col8:
        food = st.text_input(
            texts[st.session_state.language]["food_input"],
            value=st.session_state.food,
            help="أدخل عدد الطعام المطلوب" if language == "العربية" else "Enter the amount of food required" if language == "English" else "Introduceți cantitatea de mâncare necesară",
            key="food_input"
        )

    if st.button(texts[st.session_state.language]["calculate_rewards"], type="primary"):
        try:
            rewards = float(rewards) if rewards else None
            food = float(food) if food else None

            if rewards is None or food is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗️" if language == "العربية" else "❗️ Please enter all required values!" if language == "English" else "❗️ Vă rugăm să introduceți toate valorile necesare!")
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
                    "العنصر" if language == "العربية" else "Item" if language == "English" else "Element": [
                        "سعر البيض الكلي 💰" if language == "العربية" else "💰 Total Egg Price" if language == "English" else "💰 Prețul Total al Ouălor",
                        "تكلفة العلف الكلية 🌽" if language == "العربية" else "🌽 Total Feed Cost" if language == "English" else "🌽 Costul Total al Furajului",
                        "الربح اليومي 💵" if language == "العربية" else "💵 Daily Profit" if language == "English" else "💵 Profit Zilnic"
                    ],
                    "القيمة" if language == "العربية" else "Value" if language == "English" else "Valoare": [
                        f"{format_decimal(total_egg_price)} {currency}",
                        f"{format_decimal(total_feed_cost)} {currency}",
                        f"{format_decimal(net_profit)} {currency}"
                    ]
                }

                # عرض النتائج كجدول
                st.success("تم الحساب بنجاح! ✅" if language == "العربية" else "✅ Calculation completed successfully!" if language == "English" else "✅ Calcul finalizat cu succes!")
                df = pd.DataFrame(results)
                if language == "العربية":
                    df = df[["العنصر", "القيمة"]]  # تغيير ترتيب الأعمدة للغة العربية
                st.table(df)

                # إضافة رسم بياني شريطي
                chart_data = pd.DataFrame({
                    "الفئة" if language == "العربية" else "Category" if language == "English" else "Categorie": [
                        "سعر البيض الكلي" if language == "العربية" else "Total Egg Price" if language == "English" else "Prețul Total al Ouălor",
                        "تكلفة العلف الكلية" if language == "العربية" else "Total Feed Cost" if language == "English" else "Costul Total al Furajului"
                    ],
                    "القيمة" if language == "العربية" else "Value" if language == "English" else "Valoare": [
                        total_egg_price,
                        total_feed_cost
                    ]
                })

                fig = px.bar(chart_data, x="الفئة" if language == "العربية" else "Category", y="القيمة" if language == "العربية" else "Value",
                             title="توزيع التكاليف والأرباح" if language == "العربية" else "Distribution of Costs and Profits" if language == "English" else "Distribuția Costurilor și Profiturilor",
                             color="الفئة" if language == "العربية" else "Category",
                             color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)

        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗️" if language == "العربية" else "❗️ Please enter valid numbers!" if language == "English" else "❗️ Vă rugăm să introduceți numere valide!")

# إضافة نص حقوق النشر والأيقونات
st.markdown(
    """
    <div style="text-align: center; font-size: 16px; color: gray; margin-top: 50px; font-weight: bold;">
        <a href="https://www.facebook.com/newyolkfarming" target="_blank" style="text-decoration: none; color: inherit; margin: 0 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
        </a>
        <a href="https://farm.newyolk.io" target="_blank" style="text-decoration: none; color: inherit; margin: 0 10px;">
            <img src="https://cdn-icons-png.flaticon.com/512/25/25231.png" alt="Website" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
        </a>
        <a href="https://t.me/newyolkfarm" target="_blank" style="text-decoration: none; color: inherit; margin: 0 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" alt="Telegram" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
        </a>
        <a href="https://discord.gg/RYDExGGWXh" target="_blank" style="text-decoration: none; color: inherit; margin: 0 10px;">
            <img src="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png" alt="Discord" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
        </a>
        <br>
        <br>
        by Tariq Al-Yaseen © 2025-2026
    </div>
    <style>
        a img:hover {
            transform: scale(1.2);
        }
    </style>
    """,
    unsafe_allow_html=True
)
