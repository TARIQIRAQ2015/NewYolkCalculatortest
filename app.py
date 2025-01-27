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
        "profit_before_rent": "الربح قبل الإيجار",
        "rent_payment": "دفع الإيجار",
        "net_profit": "صافي الربح",
        "daily_profit": "الربح اليومي",
        "copyright": "by Tariq Al-Yaseen © 2025-2026"
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
        "profit_before_rent": "Profit before rent",
        "rent_payment": "Rent payment",
        "net_profit": "Net profit",
        "daily_profit": "Daily profit",
        "copyright": "by Tariq Al-Yaseen © 2025-2026"
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
        "profit_before_rent": "Profit înainte de chirie",
        "rent_payment": "Plata chiriei",
        "net_profit": "Profit net",
        "daily_profit": "Profit zilnic",
        "copyright": "by Tariq Al-Yaseen © 2025-2026"
    }
}

# اختيار اللغة
language = st.selectbox("Select Language", ["العربية", "English", "Română"])

# تغيير اتجاه الكتابة بناءً على اللغة
direction = "rtl" if language == "العربية" else "ltr"
st.markdown(
    f"""
    <style>
    body {{
        background: {{'black' if st.session_state.theme == "Dark" else 'white'}};
        color: {{'black' if st.session_state.theme == "Dark" else 'white'}};
        direction: {direction};
    }}
    .stTable {{ text-align: {direction}; }}
    </style>
    """,
    unsafe_allow_html=True
)

# باقي الكود يتبع نفس التعديلات لتطبيق النصوص المترجمة بشكل ديناميكي بناءً على اللغة المختارة
