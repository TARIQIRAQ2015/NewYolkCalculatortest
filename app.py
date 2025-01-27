import streamlit as st
import pandas as pd
import plotly.express as px

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تحسين الواجهة
st.set_page_config(
    page_title="Newyolk Chicken Calculator",
    page_icon="🐔"
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

# النصوص للغات المختلفة
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
        "copyright": "by Tariq Al-Yaseen © 2025-2026",
        "profit_before_rent": "الأرباح قبل الإيجار 📊",
        "rent_payment": "دفع الإيجار 💸",
        "net_profit": "الأرباح الصافية 💵",
        "success_message": "تم الحساب بنجاح! ✅",
        "error_message_required": "يرجى إدخال جميع القيم المطلوبة! ❗️",
        "error_message_eggs": "عدد البيض يجب ألا يتجاوز 580! ❗️",
        "error_message_days": "عدد الأيام يجب ألا يتجاوز 730! ❗️",
        "error_message_valid_numbers": "يرجى إدخال أرقام صحيحة! ❗️",
        "reset_success": "تم إعادة التعيين بنجاح! ✅",
        "price_saved": "تم حفظ الأسعار الجديدة بنجاح! ✅"
    },
    "English": {
        "title": "🐔 Chicken Calculator - Newyolk",
        "subtitle": "Calculate Chicken Profits and Daily Rewards",
        "currency_select": "Currency 💰",
        "edit_prices": "Edit Prices ⚙️",
        "new_egg_price": "Current Egg Price 🥚",
        "new_feed_price": "Current Feed Price 🌽",
        "save_prices": "Save New Prices 💾",
        "calculation_type": "Calculation Type 📊",
        "chicken_profits": "Chicken Profits",
        "daily_rewards": "Daily Rewards and Food Profits",
        "eggs_input": "Number of Eggs 🥚",
        "days_input": "Number of Days 📅",
        "calculate_profits": "Calculate Chicken Profits 🧮",
        "rewards_input": "Number of Rewards 🎁",
        "food_input": "Amount of Food Needed 🌽",
        "calculate_rewards": "Calculate Daily Rewards and Food Profits 🧮",
        "reset": "Reset 🔄",
        "copyright": "by Tariq Al-Yaseen © 2025-2026",
        "profit_before_rent": "Profit before rent 📊",
        "rent_payment": "Rent payment 💸",
        "net_profit": "Net profit 💵",
        "success_message": "Calculation successful! ✅",
        "error_message_required": "Please enter all required values! ❗️",
        "error_message_eggs": "Number of eggs should not exceed 580! ❗️",
        "error_message_days": "Number of days should not exceed 730! ❗️",
        "error_message_valid_numbers": "Please enter valid numbers! ❗️",
        "reset_success": "Reset successful! ✅",
        "price_saved": "New prices saved successfully! ✅"
    },
    "Română": {
        "title": "🐔 Calculator de Găini - Newyolk",
        "subtitle": "Calculează Profiturile și Recompensele Zilnice",
        "currency_select": "Monedă 💰",
        "edit_prices": "Editează Prețurile ⚙️",
        "new_egg_price": "Prețul Curent al Ouălor 🥚",
        "new_feed_price": "Prețul Curent al Furajului 🌽",
        "save_prices": "Salvează Noile Prețuri 💾",
        "calculation_type": "Tipul Calculului 📊",
        "chicken_profits": "Profituri din Găini",
        "daily_rewards": "Recompense Zilnice și Profituri din Mâncare",
        "eggs_input": "Numărul de Ouă 🥚",
        "days_input": "Numărul de Zile 📅",
        "calculate_profits": "Calculează Profiturile din Găini 🧮",
        "rewards_input": "Numărul de Recompense 🎁",
        "food_input": "Cantitatea de Mâncare Necesară 🌽",
        "calculate_rewards": "Calculează Recompensele Zilnice și Profiturile din Mâncare 🧮",
        "reset": "Resetează 🔄",
        "copyright": "by Tariq Al-Yaseen © 2025-2026",
        "profit_before_rent": "Profit înainte de chirie 📊",
        "rent_payment": "Plată chirie 💸",
        "net_profit": "Profit net 💵",
        "success_message": "Calcul reușit! ✅",
        "error_message_required": "Vă rugăm să introduceți toate valorile necesare! ❗️",
        "error_message_eggs": "Numărul de ouă nu trebuie să depășească 580! ❗️",
        "error_message_days": "Numărul de zile nu trebuie să depășească 730! ❗️",
        "error_message_valid_numbers": "Vă rugăm să introduceți numere valide! ❗️",
        "reset_success": "Resetare reușită! ✅",
        "price_saved": "Prețurile noi au fost salvate cu succes! ✅"
    }
}

# اختيار اللغة
language = st.selectbox("Select Language", ["العربية", "English", "Română"])

# تغيير اتجاه الكتابة بناءً على اللغة
direction = "rtl" if language == "العربية" else "ltr"
st.markdown(
    f"""
    <style>
    div[data-testid="stTextInput"] label {{
        text-align: {direction};
    }}
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown(
    f"""
    {texts[language]["title"]}
    {texts[language]["subtitle"]}
    """,
    unsafe_allow_html=True
)

# استخدام الأعمدة لتخطيط أفضل
col1, col2 = st.columns(2)
with col1:
    currency = st.selectbox(
        texts[language]["currency_select"],
        ["دولار أمريكي", "دينار عراقي"] if language == "العربية" else ["USD", "IQD"] if language == "English" else ["USD", "IQD"]
    )
with col2:
    calculation_type = st.selectbox(
        texts[language]["calculation_type"],
        [texts[language]["chicken_profits"], texts[language]["daily_rewards"]]
    )

# قسم تعديل الأسعار
st.subheader(texts[language]["edit_prices"])
col3, col4 = st.columns(2)
with col3:
    new_egg_price = st.text_input(texts[language]["new_egg_price"], value=str(st.session_state.egg_price))
with col4:
    new_feed_price = st.text_input(texts[language]["new_feed_price"], value=str(st.session_state.feed_price))

if st.button(texts[language]["save_prices"], type="secondary"):
    try:
        st.session_state.egg_price = float(new_egg_price)
        st.session_state.feed_price = float(new_feed_price)
        st.success(texts[language]["price_saved"])
    except ValueError:
        st.error(texts[language]["error_message_valid_numbers"])

# تحديث الأسعار بناءً على العملة
if currency == "دينار عراقي" or currency == "Iraqi Dinar" or currency == "Dinar Irakian":
    egg_price_display = st.session_state.egg_price * 1480
    feed_price_display = st.session_state.feed_price * 1480
else:
    egg_price_display = st.session_state.egg_price
    feed_price_display = st.session_state.feed_price

st.write(f"{texts[language]['new_egg_price']}: {format_decimal(egg_price_display)} {currency}")
st.write(f"{texts[language]['new_feed_price']}: {format_decimal(feed_price_display)} {currency}")

if calculation_type == texts[language]["chicken_profits"]:
    st.subheader(texts[language]["chicken_profits"] + " 📈")
    col5, col6 = st.columns(2)
    with col5:
        eggs = st.text_input(
            texts[language]["eggs_input"],
            value=st.session_state.eggs,
            help="أدخل عدد البيض (بحد أقصى 580)" if language == "العربية" else "Enter the number of eggs (max 580)" if language == "English" else "Introduceți numărul de ouă (maxim 580)",
            key="eggs_input"
        )
    with col6:
        days = st.text_input(
            texts[language]["days_input"],
            value=st.session_state.days,
            help="أدخل عدد الأيام (بحد أقصى 730)" if language == "العربية" else "Enter the number of days (max 730)" if language == "English" else "Introduceți numărul de zile (maxim 730)",
            key="days_input"
        )
    
    if st.button(texts[language]["calculate_profits"], type="primary"):
        try:
            eggs = float(eggs) if eggs else None
            days = float(days) if days else None
            if eggs is None or days is None:
                st.error(texts[language]["error_message_required"])
            elif eggs > 580:
                st.error(texts[language]["error_message_eggs"])
            elif days > 730:
                st.error(texts[language]["error_message_days"])
            else:
                # حساب النتائج
                total_egg_price_usd = eggs * st.session_state.egg_price
                total_feed_cost_usd = (days * 2) * st.session_state.feed_price
                net_profit_before_rent_usd = total_egg_price_usd - total_feed_cost_usd
                
                # حساب تكلفة الإيجار بناءً على عدد البيض
                rent_cost_usd = 6.0 if eggs >= 260 else 0.0
                net_profit_usd = net_profit_before_rent_usd - rent_cost_usd
                
                if currency == "دينار عراقي" or currency == "Iraqi Dinar" or currency == "Dinar Irakian":
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
                    texts[language]["calculation_type"]: [
                        texts[language]["new_egg_price"] + " 💰",
                        texts[language]["new_feed_price"] + " 🌽",
                        texts[language]["profit_before_rent"] + " 📊",
                        texts[language]["rent_payment"] + " 💸",
                        texts[language]["net_profit"] + " 💵"
                    ],
                    "Value": [
                        f"{format_decimal(total_egg_price)} {currency}",
                        f"{format_decimal(total_feed_cost)} {currency}",
                        f"{format_decimal(net_profit_before_rent)} {currency}",
                        f"{format_decimal(rent_cost)} {currency}",
                        f"{format_decimal(net_profit)} {currency}"
                    ]
                }
                
                # عرض النتائج كجدول
                st.success(texts[language]["success_message"])
                df = pd.DataFrame(results)
                df = df[[texts[language]["calculation_type"], "Value"]]  # تغيير ترتيب الأعمدة للغة العربية
                st.table(df)
                
                # إضافة رسم بياني شريطي
                chart_data = pd.DataFrame({
                    "Category": [
                        texts[language]["new_egg_price"],
                        texts[language]["new_feed_price"],
                        texts[language]["rent_payment"]
                    ],
                    "Value": [
                        total_egg_price,
                        total_feed_cost,
                        rent_cost
                    ]
                })
                fig = px.bar(chart_data, x="Category", y="Value",
                             title="Cost and Profit Distribution",
                             color="Category",
                             color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)
        
        except ValueError:
            st.error(texts[language]["error_message_valid_numbers"])
            
elif calculation_type == texts[language]["daily_rewards"]:
    st.subheader(texts[language]["daily_rewards"] + " 📈")
    col7, col8 = st.columns(2)
    with col7:
        rewards = st.text_input(
            texts[language]["rewards_input"],
            value=st.session_state.rewards,
            help="أدخل عدد المكافآت" if language == "العربية" else "Enter the number of rewards" if language == "English" else "Introduceți numărul de recompense",
            key="rewards_input"
        )
    with col8:
        food = st.text_input(
            texts[language]["food_input"],
            value=st.session_state.food,
            help="أدخل عدد الطعام المطلوب" if language == "العربية" else "Enter the amount of food needed" if language == "English" else "Introduceți cantitatea de mâncare necesară",
            key="food_input"
        )
    
    if st.button(texts[language]["calculate_rewards"], type="primary"):
        try:
            rewards = float(rewards) if rewards else None
            food = float(food) if food else None
            if rewards is None or food is None:
                st.error(texts[language]["error_message_required"])
            else:
                # حساب النتائج
                total_egg_price_usd = rewards * st.session_state.egg_price
                total_feed_cost_usd = food * st.session_state.feed_price
                net_profit_usd = total_egg_price_usd - total_feed_cost_usd
                
                if currency == "دينار عراقي" or currency == "Iraqi Dinar" or currency == "Dinar Irakian":
                    total_egg_price = total_egg_price_usd * 1480
                    total_feed_cost = total_feed_cost_usd * 1480
                    net_profit = net_profit_usd * 1480
                else:
                    total_egg_price, total_feed_cost, net_profit = (
                        total_egg_price_usd, total_feed_cost_usd, net_profit_usd
                    )
                
                # إنشاء جدول للنتائج
                results = {
                    texts[language]["calculation_type"]: [
                        texts[language]["new_egg_price"] + " 💰",
                        texts[language]["new_feed_price"] + " 🌽",
                        "Daily profit 💵"
                    ],
                    "Value": [
                        f"{format_decimal(total_egg_price)} {currency}",
                        f"{format_decimal(total_feed_cost)} {currency}",
                        f"{format_decimal(net_profit)} {currency}"
                    ]
                }
                
                # عرض النتائج كجدول
                st.success(texts[language]["success_message"])
                df = pd.DataFrame(results)
                df = df[[texts[language]["calculation_type"], "Value"]]  # تغيير ترتيب الأعمدة للغة العربية
                st.table(df)
                
                # إضافة رسم بياني شريطي
                chart_data = pd.DataFrame({
                    "Category": [
                        texts[language]["new_egg_price"],
                        texts[language]["new_feed_price"]
                    ],
                    "Value": [
                        total_egg_price,
                        total_feed_cost
                    ]
                })
                fig = px.bar(chart_data, x="Category", y="Value",
                             title="Cost and Profit Distribution",
                             color="Category",
                             color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)
        
        except ValueError:
            st.error(texts[language]["error_message_valid_numbers"])

# زر إعادة التعيين
if st.button(texts[language]["reset"], type="secondary"):
    st.session_state.egg_price = 0.1155
    st.session_state.feed_price = 0.0189
    st.session_state.eggs = ""
    st.session_state.days = ""
    st.session_state.rewards = ""
    st.session_state.food = ""
    st.success(texts[language]["reset_success"])

# إضافة نص حقوق النشر والأيقونات
st.markdown(
    f"""
    by Tariq Al-Yaseen © 2025-2026
    """,
    unsafe_allow_html=True
)
