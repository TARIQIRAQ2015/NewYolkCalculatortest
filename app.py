import streamlit as st
import plotly.express as px
import pandas as pd

# إعدادات الصفحة
st.set_page_config(page_title="Newyolk Chicken Calculator", layout="wide")

# دعم تعدد اللغات
languages = {
    "العربية": {
        "title": "Newyolk Chicken Calculator",
        "description": "حساب أرباح الدجاج والمكافآت اليومية",
        "reset": "إعادة التعيين",
        "calculate": "حساب",
        "profit": "الربح الصافي",
        "daily_profit": "الربح اليومي",
        "total_egg_price": "سعر البيض الكلي",
        "total_feed_cost": "تكلفة العلف الكلية",
        "rent_cost": "تكلفة الإيجار",
        "before_rent": "الربح قبل الإيجار",
        "currency": "العملة",
        "language": "اللغة",
        "dark_mode": "الوضع الداكن",
        "copyright": "جميع الحقوق محفوظة © 2025 by Tariq Al-Yaseen"
    },
    "English": {
        "title": "Newyolk Chicken Calculator",
        "description": "Calculate Chicken Profits and Daily Rewards",
        "reset": "Reset",
        "calculate": "Calculate",
        "profit": "Net Profit",
        "daily_profit": "Daily Profit",
        "total_egg_price": "Total Egg Price",
        "total_feed_cost": "Total Feed Cost",
        "rent_cost": "Rent Cost",
        "before_rent": "Profit Before Rent",
        "currency": "Currency",
        "language": "Language",
        "dark_mode": "Dark Mode",
        "copyright": "All rights reserved © 2025 by Tariq Al-Yaseen"
    },
    "Română": {
        "title": "Newyolk Chicken Calculator",
        "description": "Calculați Profiturile și Recompensele Zilnice ale Găinilor",
        "reset": "Resetați",
        "calculate": "Calculați",
        "profit": "Profit Net",
        "daily_profit": "Profit Zilnic",
        "total_egg_price": "Prețul Total al Oului",
        "total_feed_cost": "Costul Total al Furajului",
        "rent_cost": "Costul Închirierii",
        "before_rent": "Profit înainte de Închiriere",
        "currency": "Monedă",
        "language": "Limba",
        "dark_mode": "Mod Întunecat",
        "copyright": "Toate drepturile rezervate © 2025 de Tariq Al-Yaseen"
    }
}

# اختيار اللغة
language = st.sidebar.selectbox("اللغة / Language / Limba", list(languages.keys()))

# الوضع الداكن
dark_mode = st.sidebar.checkbox("الوضع الداكن / Dark Mode / Mod Întunecat")

# العملة
currency = st.sidebar.selectbox("العملة / Currency / Monedă", ["USD", "IQD"])

# أسعار الصرف
exchange_rate = 1480 if currency == "IQD" else 1

# القيم الافتراضية
default_egg_price = 0.1155 * exchange_rate
default_feed_price = 0.0189 * exchange_rate
default_rent = 6 * exchange_rate

# واجهة المستخدم
st.title(languages[language]["title"])
st.write(languages[language]["description"])

# إدخال البيانات
col1, col2 = st.columns(2)

with col1:
    eggs = st.number_input("عدد البيض / Number of Eggs / Numărul de Ouă", min_value=0, max_value=580, value=0)
    days = st.number_input("عدد الأيام / Number of Days / Numărul de Zile", min_value=0, max_value=730, value=0)

with col2:
    rewards = st.number_input("عدد المكافآت / Number of Rewards / Numărul de Recompense", min_value=0, value=0)
    food = st.number_input("عدد الطعام المطلوب / Required Food Amount / Cantitatea de Hrană Necesară", min_value=0, value=0)

# تعديل الأسعار
st.sidebar.header("تعديل الأسعار / Adjust Prices / Ajustarea Prețurilor")
egg_price = st.sidebar.number_input("سعر البيض / Egg Price / Prețul Oului", value=default_egg_price)
feed_price = st.sidebar.number_input("سعر العلف / Feed Price / Prețul Furajului", value=default_feed_price)

# الحسابات
total_egg_price = eggs * egg_price
total_feed_cost = (days * 2) * feed_price
profit_before_rent = total_egg_price - total_feed_cost
rent_cost = default_rent if days >= 365 else 0
net_profit = profit_before_rent - rent_cost

daily_egg_price = rewards * egg_price
daily_feed_cost = food * feed_price
daily_profit = daily_egg_price - daily_feed_cost

# عرض النتائج
results = {
    languages[language]["total_egg_price"]: total_egg_price,
    languages[language]["total_feed_cost"]: total_feed_cost,
    languages[language]["before_rent"]: profit_before_rent,
    languages[language]["rent_cost"]: rent_cost,
    languages[language]["profit"]: net_profit,
    languages[language]["daily_profit"]: daily_profit
}

df = pd.DataFrame(list(results.items()), columns=["العنصر / Item / Element", "القيمة / Value / Valoare"])
st.table(df)

# الرسم البياني
fig = px.pie(df, values="القيمة / Value / Valoare", names="العنصر / Item / Element", title="توزيع التكاليف والأرباح / Cost and Profit Distribution / Distribuția Costurilor și Profiturilor")
st.plotly_chart(fig)

# إعادة التعيين
if st.button(languages[language]["reset"]):
    eggs = 0
    days = 0
    rewards = 0
    food = 0
    egg_price = default_egg_price
    feed_price = default_feed_price

# حقوق النشر
st.markdown(f"<div style='text-align: center;'>{languages[language]['copyright']}</div>", unsafe_allow_html=True)
