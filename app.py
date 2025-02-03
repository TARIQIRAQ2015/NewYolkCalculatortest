import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# التحقق من صحة الأرقام
def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# تعريف النصوص بجميع اللغات
texts = {
    "العربية": {
        "title": "حاسبة الدجاج - نيويولك",
        "subtitle": "حساب أرباح الدجاج والمكافآت اليومية",
        "language": "اللغة 🌍",
        "currency": "العملة 💵",
        "calculation_type": "نوع الحساب",
        "chicken_profits": "أرباح الدجاج 📊",
        "daily_rewards": "المكافآت اليومية 📈",
        "romania_calculation": "حساب رومانيا",
        "iraq_calculation": "حساب العراق",
        "egg_price": "سعر البيض",
        "feed_price": "سعر العلف",
        "save_prices": "حفظ الأسعار ✅",
        "eggs_count": "عدد البيض 🥚",
        "days_count": "عدد الأيام 📅",
        "calculate": "حساب النتائج",
        "rewards_count": "عدد المكافآت",
        "food_count": "كمية العلف",
        "results": "النتائج 📊",
        "calculation_time": "وقت الحساب",
        "usd_results": "النتائج بالدولار",
        "iqd_results": "النتائج بالدينار العراقي",
        "daily_profit": "الربح اليومي",
        "total_eggs": "إجمالي البيض",
        "total_price": "السعر الإجمالي",
        "net_profit": "صافي الربح",
        "first_year_rental": "إيجار السنة الأولى",
        "final_profit": "الربح النهائي",
        "value": "القيمة"
    },
    "English": {
        "title": "Chicken Calculator - NewYolk",
        "subtitle": "Calculate Chicken Profits and Daily Rewards",
        "language": "Language 🌍",
        "currency": "Currency 💵",
        "calculation_type": "Calculation Type",
        "chicken_profits": "Chicken Profits 📊",
        "daily_rewards": "Daily Rewards 📈",
        "romania_calculation": "Romania Calculation",
        "iraq_calculation": "Iraq Calculation",
        "egg_price": "Egg Price",
        "feed_price": "Feed Price",
        "save_prices": "Save Prices ✅",
        "eggs_count": "Eggs Count 🥚",
        "days_count": "Days Count 📅",
        "calculate": "Calculate Results",
        "rewards_count": "Rewards Count",
        "food_count": "Food Amount",
        "results": "Results 📊",
        "calculation_time": "Calculation Time",
        "usd_results": "Results in USD",
        "iqd_results": "Results in IQD",
        "daily_profit": "Daily Profit",
        "total_eggs": "Total Eggs",
        "total_price": "Total Price",
        "net_profit": "Net Profit",
        "first_year_rental": "First Year Rental",
        "final_profit": "Final Profit",
        "value": "Value"
    }
}

# إعداد الصفحة
st.set_page_config(
    page_title="Chicken Calculator - Newyolk",
    page_icon="🐔",
    layout="wide"
)

# تحسين الواجهة
st.markdown("""
    <style>
        /* إخفاء العناصر غير الضرورية */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stToolbar"] {visibility: hidden;}
        
        /* تحسين المظهر العام والخلفية */
        .stApp {
            background: linear-gradient(135deg, 
                #1a1a2e,
                #16213e,
                #0f3460,
                #162447
            );
            background-size: 400% 400%;
            animation: gradient 15s ease infinite;
            color: #e2e2e2;
        }
        
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        
        /* تحسين القوائم المنسدلة */
        .stSelectbox > div > div {
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            transition: all 0.3s ease;
        }
        
        .stSelectbox > div > div:hover {
            background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.1)) !important;
            border-color: rgba(255, 255, 255, 0.3) !important;
        }
        
        /* تحسين العنوان الرئيسي */
        .main-title {
            font-size: 2.5em !important;
            font-weight: bold !important;
            text-align: center !important;
            margin: 1em 0 !important;
            color: #ffffff !important;
            text-shadow: 0 0 10px rgba(255,255,255,0.3);
        }
    </style>
""", unsafe_allow_html=True)

# إنشاء الشريط العلوي
top_bar_col1, top_bar_col2, *remaining_cols = st.columns([1, 1, 3, 3])

with top_bar_col1:
    language = st.selectbox(
        "🌍",
        ["العربية", "English"],
        key="language_selector",
        label_visibility="visible"
    )

with top_bar_col2:
    calculation_country = st.selectbox(
        "🏦",
        [texts[language]["romania_calculation"], texts[language]["iraq_calculation"]],
        label_visibility="visible"
    )

# تحديد الأسعار الافتراضية بناءً على نوع الحساب
if calculation_country == texts[language]["iraq_calculation"]:
    default_egg_price = 0.1219
    default_feed_price = 0.0191
else:  # رومانيا
    default_egg_price = 0.1450
    default_feed_price = 0.0220

# عرض العنوان الرئيسي
st.markdown(f"<h1 class='main-title'>{texts[language]['title']}</h1>", unsafe_allow_html=True)

# القسم الرئيسي للتطبيق
col1, col2 = st.columns(2)

with col1:
    currency = st.selectbox(
        texts[language]["currency"],
        ["USD", "IQD"]
    )

with col2:
    calculation_type = st.selectbox(
        texts[language]["calculation_type"],
        [texts[language]["chicken_profits"], texts[language]["daily_rewards"]]
    )

# قسم تعديل الأسعار
st.subheader(texts[language]["save_prices"])
price_col1, price_col2 = st.columns(2)

with price_col1:
    egg_price = st.number_input(
        texts[language]["egg_price"],
        min_value=0.0,
        value=default_egg_price,
        format="%.4f"
    )

with price_col2:
    feed_price = st.number_input(
        texts[language]["feed_price"],
        min_value=0.0,
        value=default_feed_price,
        format="%.4f"
    )

# عرض الأسعار الحالية
if currency == "IQD":
    egg_price_display = float(egg_price) * 1480
    feed_price_display = float(feed_price) * 1480
else:
    egg_price_display = float(egg_price)
    feed_price_display = float(feed_price)

st.write(f"{texts[language]['egg_price']}: {format_decimal(egg_price_display)} {currency}")
st.write(f"{texts[language]['feed_price']}: {format_decimal(feed_price_display)} {currency}")

# قسم الحسابات
if calculation_type == texts[language]["chicken_profits"]:
    st.subheader(texts[language]["chicken_profits"])
    calc_col1, calc_col2 = st.columns(2)
    
    with calc_col1:
        eggs = st.number_input(texts[language]["eggs_count"], min_value=0)
    
    with calc_col2:
        days = st.number_input(texts[language]["days_count"], min_value=0)
    
    if st.button(texts[language]["calculate"]):
        if eggs == 0 or days == 0:
            st.error("يرجى إدخال جميع القيم المطلوبة! ❗️")
        elif days > 730:
            st.error("عدد الأيام يجب ألا يتجاوز 730! ❗️")
        else:
            # حساب الأرباح
            total_egg_price = eggs * float(egg_price)
            total_feed_cost = (days * 2) * float(feed_price)
            total_rent = 6 if eggs >= 260 else 0
            
            net_profit_before_rent = total_egg_price - total_feed_cost
            net_profit = net_profit_before_rent - total_rent
            
            # تحضير نص النتائج للنسخ
            if currency == "IQD":
                conversion = 1480
            else:
                conversion = 1
            
            results_text = f"""
🥚 {texts[language]['total_eggs']}: {eggs}
💰 {texts[language]['total_price']}: {format_decimal(total_egg_price * conversion)} {currency}
🌾 {texts[language]['feed_price']}: {format_decimal(total_feed_cost * conversion)} {currency}
📈 {texts[language]['net_profit']}: {format_decimal(net_profit_before_rent * conversion)} {currency}
🏠 {texts[language]['first_year_rental']}: {format_decimal(total_rent * conversion)} {currency}
💎 {texts[language]['final_profit']}: {format_decimal(net_profit * conversion)} {currency}
"""
            # عرض النتائج مع زر النسخ
            st.code(results_text)
            st.button("نسخ النتائج 📋", key="copy_results", on_click=lambda: st.write(results_text))

elif calculation_type == texts[language]["daily_rewards"]:
    st.subheader(texts[language]["daily_rewards"])
    reward_col1, reward_col2 = st.columns(2)
    
    with reward_col1:
        rewards = st.number_input(texts[language]["rewards_count"], min_value=0)
    
    with reward_col2:
        food = st.number_input(texts[language]["food_count"], min_value=0)
    
    if st.button(texts[language]["calculate"]):
        if rewards == 0 or food == 0:
            st.error("يرجى إدخال جميع القيم المطلوبة! ❗️")
        else:
            # حساب الربح اليومي
            daily_profit = rewards * float(egg_price) - food * float(feed_price)
            
            # تحضير نص النتائج للنسخ
            if currency == "IQD":
                conversion = 1480
            else:
                conversion = 1
            
            results_text = f"""
🥚 {texts[language]['egg_price']}: {format_decimal(rewards * float(egg_price) * conversion)} {currency}
🌾 {texts[language]['feed_price']}: {format_decimal(food * float(feed_price) * conversion)} {currency}
💎 {texts[language]['daily_profit']}: {format_decimal(daily_profit * conversion)} {currency}
"""
            # عرض النتائج مع زر النسخ
            st.code(results_text)
            st.button("نسخ النتائج 📋", key="copy_daily_results", on_click=lambda: st.write(results_text))

# إضافة الأيقونات والروابط
st.markdown("""
    <style>
        .social-links {
            display: flex;
            justify-content: center;
            gap: 25px;
            margin: 30px 0 20px;
        }
        
        .social-links a {
            display: inline-block;
            transition: all 0.3s ease;
        }
        
        .social-links img {
            width: 36px;
            height: 36px;
            filter: brightness(1);
            transition: all 0.3s ease;
        }
        
        .social-links a:hover img {
            transform: translateY(-3px);
            filter: brightness(1.2);
        }
    </style>
    <div class="social-links">
        <a href="https://farm.newyolk.io/" target="_blank">
            <img src="https://i.ibb.co/YDKWBRf/internet.png" alt="Website">
        </a>
        <a href="https://discord.gg/RYDExGGWXh" target="_blank">
            <img src="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png" alt="Discord">
        </a>
        <a href="https://t.me/newyolkfarm" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" alt="Telegram">
        </a>
        <a href="https://www.facebook.com/newyolkfarming" target="_blank">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook">
        </a>
    </div>
    
    <style>
        .copyright {
            text-align: center;
            color: rgba(255,255,255,0.9);
            padding: 24px 0;
            font-size: 22px !important;
            margin-top: 30px;
            border-top: 1px solid rgba(255,255,255,0.1);
            font-weight: 600;
            letter-spacing: 0.5px;
        }
    </style>
    <div class="copyright">By Tariq Al-Yaseen &copy; 2025-2026</div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        /* تحسين الإيموجي في العنوان */
        .emoji-link {
            text-decoration: none;
            font-size: 24px !important;
            display: inline-block;
            transition: all 0.3s ease;
            line-height: 1;
            cursor: pointer;
            margin-right: 8px;
        }
        
        .emoji-link:hover {
            transform: scale(1.2) rotate(10deg);
        }
        
        .title {
            display: flex;
            align-items: center;
            justify-content: center;
            margin-bottom: 12px;
        }
        
        .title-text {
            background: linear-gradient(120deg, #ffffff, #e2e2e2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
            font-size: 32px;
            font-weight: bold;
        }
    </style>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        /* تنسيق ملخص النتائج */
        pre {
            background: linear-gradient(45deg, 
                #1a1a2e,
                #16213e
            ) !important;
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 15px !important;
            padding: 20px !important;
            color: #ffffff !important;
            font-family: 'Courier New', monospace !important;
            position: relative !important;
            overflow: hidden !important;
            transition: all 0.3s ease !important;
            animation: gradientBG 15s ease infinite !important;
            background-size: 200% 200% !important;
        }

        pre:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 20px rgba(0,0,0,0.3);
            border-color: rgba(255, 255, 255, 0.2) !important;
        }

        /* تأثير الخلفية المتحركة */
        @keyframes gradientBG {
            0% {
                background: linear-gradient(45deg, 
                    #1a1a2e,
                    #16213e,
                    #0f3460
                );
                background-size: 200% 200%;
                background-position: 0% 50%;
            }
            50% {
                background: linear-gradient(45deg, 
                    #16213e,
                    #0f3460,
                    #1a1a2e
                );
                background-size: 200% 200%;
                background-position: 100% 50%;
            }
            100% {
                background: linear-gradient(45deg, 
                    #1a1a2e,
                    #16213e,
                    #0f3460
                );
                background-size: 200% 200%;
                background-position: 0% 50%;
            }
        }

        /* تنسيق النص داخل ملخص النتائج */
        pre code {
            color: #e2e2e2 !important;
            font-size: 1.1em !important;
            line-height: 1.5 !important;
        }

        /* تأثير الحدود المضيئة */
        pre::before {
            content: '';
            position: absolute;
            top: -2px;
            left: -2px;
            right: -2px;
            bottom: -2px;
            border-radius: 16px;
            background: linear-gradient(45deg, 
                #1a1a2e,
                #0f3460,
                #1a1a2e
            );
            z-index: -1;
            animation: borderGlow 3s ease-in-out infinite;
            opacity: 0.5;
        }

        @keyframes borderGlow {
            0% {
                opacity: 0.3;
            }
            50% {
                opacity: 0.6;
            }
            100% {
                opacity: 0.3;
            }
        }
        
        /* تنسيق العنوان الرئيسي */
        .main-title {
            font-size: 2.5em !important;
            font-weight: bold !important;
            text-align: center !important;
            margin-bottom: 1em !important;
            color: #ffffff !important;
            text-shadow: 0 0 10px rgba(255,255,255,0.3);
        }
        
        /* تأثير الإيموجي المتحرك */
        .chicken-emoji {
            display: inline-block;
            font-size: 2em;
            cursor: pointer;
            transition: all 0.3s ease;
            animation: float 2s ease-in-out infinite;
        }
        
        .chicken-emoji:hover {
            transform: scale(1.3) rotate(15deg);
        }
        
        @keyframes float {
            0% { transform: translateY(0px); }
            50% { transform: translateY(-10px); }
            100% { transform: translateY(0px); }
        }
    </style>
""", unsafe_allow_html=True)
