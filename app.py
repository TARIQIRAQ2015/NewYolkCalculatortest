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
        "title": "🐔 حاسبة الدجاج - نيويولك",
        "subtitle": "حساب أرباح الدجاج والمكافآت اليومية",
        "currency_select": "العملة 💰",
        "edit_prices": "تعديل الأسعار ⚙️",
        "new_egg_price": "سعر البيض الجديد 🥚",
        "new_feed_price": "سعر العلف الجديد 🌽",
        "save_prices": "حفظ الأسعار الجديدة 💾",
        "calculation_type": "نوع الحساب 📊",
        "chicken_profits": "أرباح الدجاج",
        "daily_rewards": "المكافآت والطعام اليومي",
        "eggs_input": "عدد البيض 🥚",
        "days_input": "عدد الأيام 📅",
        "calculate_profits": "حساب أرباح الدجاج 🧮",
        "rewards_input": "عدد المكافآت 🎁",
        "food_input": "كمية الطعام المطلوبة 🌽",
        "calculate_rewards": "حساب المكافآت والطعام اليومي 🧮",
        "reset": "إعادة تعيين 🔄",
        "profit_before_rent": "الربح قبل الإيجار 📊",
        "rent_payment": "دفعة الإيجار 💸",
        "net_profit": "صافي الربح 💵",
        "daily_profit": "الربح اليومي 💵",
        "total_egg_value": "قيمة البيض الكلية 💰",
        "total_feed_cost": "تكلفة العلف الكلية 🌽",
        "cost_profit_distribution": "توزيع التكاليف والأرباح",
        "calculation_successful": "تم الحساب بنجاح! ✅",
        "reset_successful": "تم إعادة التعيين بنجاح! ✅",
        "enter_valid_numbers": "يرجى إدخال أرقام صحيحة! ❗️",
        "enter_all_values": "يرجى إدخال جميع القيم المطلوبة! ❗️",
        "eggs_limit_error": "عدد البيض يجب ألا يتجاوز 580! ❗️",
        "days_limit_error": "عدد الأيام يجب ألا يتجاوز 730! ❗️",
        "prices_saved": "تم حفظ الأسعار الجديدة بنجاح! ✅",
        "eggs_help": "أدخل عدد البيض (بحد أقصى 580)",
        "days_help": "أدخل عدد الأيام (بحد أقصى 730)",
        "rewards_help": "أدخل عدد المكافآت",
        "food_help": "أدخل كمية الطعام المطلوبة"
    },
    "English": {
        # [English translations remain the same]
    },
    "Română": {
        # [Romanian translations remain the same]
    }
}

# اختيار اللغة
language = st.selectbox("اختر اللغة / Select Language / Selectați limba", ["العربية", "English", "Română"])

# تغيير اتجاه الكتابة بناءً على اللغة
direction = "rtl" if language == "العربية" else "ltr"

[Rest of the code remains the same, but with enhanced Arabic support for all UI elements and calculations]
