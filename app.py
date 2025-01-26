import streamlit as st
import pandas as pd
import plotly.express as px

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تحسين الواجهة
st.set_page_config(
    page_title="Newyolk Chicken Calculator",
    page_icon="🐔", 
    layout="wide"
)

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

# النصوص لكل لغة
texts = {
    "العربية": {
        "title": "🐔 حاسبة الدجاج - Newyolk",
        "subtitle": "حساب أرباح الدجاج والمكافآت اليومية",
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
        "currency_select": "💰 Monedă",
        "edit_prices": "⚙️ Editează Prețurile",
        "new_egg_price": "🥚 Prețul Actual al Ouălor",
        "new_feed_price": "🌽 Prețul Actual al Furajului",
        "save_prices": "💾 Salvează Noile Prețuri",
        "calculation_type": "📊 Tipul de Calcul",
        "chicken_profits": "Profituri din Pui",
        "daily_rewards": "Recompense și Hrană Zilnică",
        "eggs_input": "🥚 Numărul de Ouă",
        "days_input": "📅 Numărul de Zile",
        "calculate_profits": "🧮 Calculează Profiturile din Pui",
        "rewards_input": "🎁 Numărul de Recompense",
        "food_input": "🌽 Cantitatea de Hrană Necesară",
        "calculate_rewards": "🧮 Calculează Recompensele și Hrana Zilnică",
        "reset": "🔄 Resetează",
        "copyright": "by Tariq Al-Yaseen © 2025-2026"
    }
}

# حالة اللغة (الإنجليزية بشكل افتراضي)
if "language" not in st.session_state:
    st.session_state.language = "English"

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
        </style>
        <div class="title">{texts[st.session_state.language]["title"]}</div>
        <div class="subtitle">{texts[st.session_state.language]["subtitle"]}</div>
        """,
        unsafe_allow_html=True
    )

# استخدام الأعمدة لتخطيط أفضل
col1, col2 = st.columns(2)

with col1:
    language = st.selectbox(
        "Choose Language",
        ["English", "العربية", "Română"],
        key="language_selectbox",
        index=["English", "العربية", "Română"].index(st.session_state.language),
        on_change=lambda: st.session_state.update({"language": language}),
        disabled=True  # قفل الكتابة في القائمة
    )

with col2:
    currency = st.selectbox(
        texts[st.session_state.language]["currency_select"],
        ["دولار أمريكي" if st.session_state.language == "العربية" else "USD", "دينار عراقي" if st.session_state.language == "العربية" else "IQD"],
        disabled=True  # قفل الكتابة في القائمة
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
        st.success("تم حفظ الأسعار الجديدة بنجاح! ✅" if st.session_state.language == "العربية" else "✅ New prices saved successfully!")
    except ValueError:
        st.error("يرجى إدخال أرقام صحيحة! ❗️" if st.session_state.language == "العربية" else "❗️ Please enter valid numbers!")

# قسم الحسابات
calculation_type = st.selectbox(
    texts[st.session_state.language]["calculation_type"],
    [texts[st.session_state.language]["chicken_profits"], texts[st.session_state.language]["daily_rewards"]],
    disabled=True  # قفل الكتابة في القائمة
)

if calculation_type == texts[st.session_state.language]["chicken_profits"]:
    st.subheader("حساب أرباح الدجاجة 📈" if st.session_state.language == "العربية" else "📈 Chicken Profits Calculation")
    col5, col6 = st.columns(2)

    with col5:
        eggs = st.text_input(
            texts[st.session_state.language]["eggs_input"],
            value=st.session_state.eggs,
            help="أدخل عدد البيض (بحد أقصى 580)" if st.session_state.language == "العربية" else "Enter the number of eggs (max 580)",
            key="eggs_input"
        )

    with col6:
        days = st.text_input(
            texts[st.session_state.language]["days_input"],
            value=st.session_state.days,
            help="أدخل عدد الأيام (بحد أقصى 730)" if st.session_state.language == "العربية" else "Enter the number of days (max 730)",
            key="days_input"
        )

    if st.button(texts[st.session_state.language]["calculate_profits"], type="primary"):
        try:
            eggs = float(eggs) if eggs else None
            days = float(days) if days else None

            if eggs is None or days is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗️" if st.session_state.language == "العربية" else "❗️ Please enter all required values!")
            elif eggs > 580:
                st.error("عدد البيض يجب ألا يتجاوز 580! ❗️" if st.session_state.language == "العربية" else "❗️ Number of eggs must not exceed 580!")
            elif days > 730:
                st.error("عدد الأيام يجب ألا يتجاوز 730! ❗️" if st.session_state.language == "العربية" else "❗️ Number of days must not exceed 730!")
            else:
                # حساب النتائج
                total_egg_price_usd = eggs * st.session_state.egg_price
                total_feed_cost_usd = (days * 2) * st.session_state.feed_price
                net_profit_before_rent_usd = total_egg_price_usd - total_feed_cost_usd

                # حساب تكلفة الإيجار بناءً على عدد البيض
                rent_cost_usd = 6.0 if eggs >= 260 else 0.0
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
                    "العنصر" if st.session_state.language == "العربية" else "Item": [
                        "سعر البيض الكلي 💰" if st.session_state.language == "العربية" else "💰 Total Egg Price",
                        "تكلفة العلف الكلية 🌽" if st.session_state.language == "العربية" else "🌽 Total Feed Cost",
                        "الربح قبل خصم الإيجار 📊" if st.session_state.language == "العربية" else "📊 Net Profit Before Rent",
                        "دفع الإيجار 💸" if st.session_state.language == "العربية" else "🏠 Rent Cost",
                        "الربح الصافي 💵" if st.session_state.language == "العربية" else "💵 Net Profit"
                    ],
                    "القيمة" if st.session_state.language == "العربية" else "Value": [
                        f"{format_decimal(total_egg_price)} {currency}",
                        f"{format_decimal(total_feed_cost)} {currency}",
                        f"{format_decimal(net_profit_before_rent)} {currency}",
                        f"{format_decimal(rent_cost)} {currency}",
                        f"{format_decimal(net_profit)} {currency}"
                    ]
                }

                # عرض النتائج كجدول
                st.success("تم الحساب بنجاح! ✅" if st.session_state.language == "العربية" else "✅ Calculation completed successfully!")
                df = pd.DataFrame(results)
                if st.session_state.language == "العربية":
                    df = df[["العنصر", "القيمة"]]  # تغيير ترتيب الأعمدة للغة العربية
                st.table(df)

                # إضافة رسم بياني شريطي
                chart_data = pd.DataFrame({
                    "الفئة" if st.session_state.language == "العربية" else "Category": [
                        "سعر البيض الكلي" if st.session_state.language == "العربية" else "Total Egg Price",
                        "تكلفة العلف الكلية" if st.session_state.language == "العربية" else "Total Feed Cost",
                        "دفع الإيجار" if st.session_state.language == "العربية" else "Rent Cost"
                    ],
                    "القيمة" if st.session_state.language == "العربية" else "Value": [
                        total_egg_price,
                        total_feed_cost,
                        rent_cost
                    ]
                })

                fig = px.bar(chart_data, x="الفئة" if st.session_state.language == "العربية" else "Category", y="القيمة" if st.session_state.language == "العربية" else "Value",
                             title="توزيع التكاليف والأرباح" if st.session_state.language == "العربية" else "Distribution of Costs and Profits",
                             color="الفئة" if st.session_state.language == "العربية" else "Category",
                             color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)

        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗️" if st.session_state.language == "العربية" else "❗️ Please enter valid numbers!")

elif calculation_type == texts[st.session_state.language]["daily_rewards"]:
    st.subheader("حساب أرباح المكافآت والطعام اليومي 📈" if st.session_state.language == "العربية" else "📈 Daily Rewards and Food Calculation")
    col7, col8 = st.columns(2)

    with col7:
        rewards = st.text_input(
            texts[st.session_state.language]["rewards_input"],
            value=st.session_state.rewards,
            help="أدخل عدد المكافآت" if st.session_state.language == "العربية" else "Enter the number of rewards",
            key="rewards_input"
        )

    with col8:
        food = st.text_input(
            texts[st.session_state.language]["food_input"],
            value=st.session_state.food,
            help="أدخل عدد الطعام المطلوب" if st.session_state.language == "العربية" else "Enter the amount of food required",
            key="food_input"
        )

    if st.button(texts[st.session_state.language]["calculate_rewards"], type="primary"):
        try:
            rewards = float(rewards) if rewards else None
            food = float(food) if food else None

            if rewards is None or food is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗️" if st.session_state.language == "العربية" else "❗️ Please enter all required values!")
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
                    "العنصر" if st.session_state.language == "العربية" else "Item": [
                        "سعر البيض الكلي 💰" if st.session_state.language == "العربية" else "💰 Total Egg Price",
                        "تكلفة العلف الكلية 🌽" if st.session_state.language == "العربية" else "🌽 Total Feed Cost",
                        "الربح اليومي 💵" if st.session_state.language == "العربية" else "💵 Daily Profit"
                    ],
                    "القيمة" if st.session_state.language == "العربية" else "Value": [
                        f"{format_decimal(total_egg_price)} {currency}",
                        f"{format_decimal(total_feed_cost)} {currency}",
                        f"{format_decimal(net_profit)} {currency}"
                    ]
                }

                # عرض النتائج كجدول
                st.success("تم الحساب بنجاح! ✅" if st.session_state.language == "العربية" else "✅ Calculation completed successfully!")
                df = pd.DataFrame(results)
                if st.session_state.language == "العربية":
                    df = df[["العنصر", "القيمة"]]  # تغيير ترتيب الأعمدة للغة العربية
                st.table(df)

                # إضافة رسم بياني شريطي
                chart_data = pd.DataFrame({
                    "الفئة" if st.session_state.language == "العربية" else "Category": [
                        "سعر البيض الكلي" if st.session_state.language == "العربية" else "Total Egg Price",
                        "تكلفة العلف الكلية" if st.session_state.language == "العربية" else "Total Feed Cost"
                    ],
                    "القيمة" if st.session_state.language == "العربية" else "Value": [
                        total_egg_price,
                        total_feed_cost
                    ]
                })

                fig = px.bar(chart_data, x="الفئة" if st.session_state.language == "العربية" else "Category", y="القيمة" if st.session_state.language == "العربية" else "Value",
                             title="توزيع التكاليف والأرباح" if st.session_state.language == "العربية" else "Distribution of Costs and Profits",
                             color="الفئة" if st.session_state.language == "العربية" else "Category",
                             color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)

        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗️" if st.session_state.language == "العربية" else "❗️ Please enter valid numbers!")

# زر إعادة التعيين
if st.button(texts[st.session_state.language]["reset"], type="secondary"):
    st.session_state.egg_price = 0.1155
    st.session_state.feed_price = 0.0189
    st.session_state.eggs = ""
    st.session_state.days = ""
    st.session_state.rewards = ""
    st.session_state.food = ""
    st.success("تم إعادة التعيين بنجاح! ✅" if st.session_state.language == "العربية" else "✅ Reset completed successfully!")

# إضافة نص حقوق النشر والأيقونات
st.markdown(
    """
    <div style="text-align: center; font-size: 16px; color: gray; margin-top: 30px; font-weight: bold;">
        <a href="https://www.facebook.com/newyolkfarming" target="_blank" style="text-decoration: none; color: inherit; margin: 0 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
        </a>
        <a href="https://farm.newyolk.io" target="_blank" style="text-decoration: none; color: inherit; margin: 0 10px;">
            <img src="https://i.ibb.co/YDKWBRf/internet.png" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
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
