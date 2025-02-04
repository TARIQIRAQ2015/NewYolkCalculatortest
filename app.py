import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# تحسين الواجهة
st.set_page_config(
    page_title="New Yolk Calculator",
    page_icon="🐔",
    layout="wide"
)

# إخفاء أزرار التحكم بالمظهر
st.markdown("""
    <style>
        /* إخفاء العناصر غير الضرورية */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
        [data-testid="stToolbar"] {visibility: hidden;}
        
        /* تحسين المظهر العام والخلفية */
        .stApp {
            background: linear-gradient(-45deg, #1e3c72, #2a5298, #2c3e50, #3498db) !important;
            background-size: 400% 400% !important;
            animation: gradientBG 8s ease infinite !important;
        }
        
        @keyframes gradientBG {
            0% {
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }
        
        /* تأثير الإيموجي */
        .emoji-link {
            text-decoration: none;
            display: inline-block;
            transition: all 0.3s ease;
            cursor: pointer;
            font-size: 32px;
            margin-right: 10px;
        }
        .emoji-link:hover {
            transform: scale(1.5);
            text-shadow: 0 0 20px rgba(255,255,255,0.5);
        }
        
        /* تحسين القوائم المنسدلة */
        .stSelectbox > div > div,
        .stNumberInput > div > div {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            padding: 12px !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            height: auto !important;
            min-height: 48px !important;
            font-size: 16px !important;
            line-height: 1.5 !important;
            position: relative;
            overflow: hidden;
        }
        
        /* تأثير الموجة عند التحويم */
        .stSelectbox > div > div::before,
        .stNumberInput > div > div::before,
        div[data-baseweb="select"] ul li::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.05),
                transparent
            );
            transition: all 0.5s ease;
            z-index: 1;
        }
        
        .stSelectbox > div > div:hover::before,
        .stNumberInput > div > div:hover::before,
        div[data-baseweb="select"] ul li:hover::before {
            left: 100%;
        }
        
        /* تأثير التحويم */
        .stSelectbox > div > div:hover,
        .stNumberInput > div > div:hover {
            background: linear-gradient(135deg, #161b25 0%, #1e212b 100%) !important;
            border-color: rgba(255, 255, 255, 0.3) !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        /* تحسين قائمة الخيارات المنسدلة */
        div[data-baseweb="select"] > div {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            padding: 8px !important;
            transition: all 0.3s ease;
        }
        
        div[data-baseweb="select"] ul {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            padding: 4px !important;
            border-radius: 8px !important;
            backdrop-filter: blur(10px);
        }
        
        /* تحسين عناصر القائمة */
        div[data-baseweb="select"] ul li {
            background: transparent !important;
            transition: all 0.3s ease;
            border-radius: 6px;
            margin: 2px 0;
            padding: 10px 12px !important;
            position: relative;
            overflow: hidden;
            cursor: pointer;
            color: rgba(255, 255, 255, 0.8) !important;
        }
        
        div[data-baseweb="select"] ul li:hover {
            background: linear-gradient(135deg, #161b25 0%, #1e212b 100%) !important;
            transform: translateX(4px);
            color: #ffffff !important;
        }
        
        /* تحسين الأيقونات في القوائم */
        .stSelectbox svg,
        div[data-baseweb="select"] svg {
            transition: all 0.3s ease;
            fill: rgba(255, 255, 255, 0.7) !important;
        }
        
        .stSelectbox:hover svg,
        div[data-baseweb="select"]:hover svg {
            fill: rgba(255, 255, 255, 1) !important;
            transform: translateY(1px);
        }
        
        /* تحسين النص المحدد */
        div[data-baseweb="select"] [aria-selected="true"] {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            color: #ffffff !important;
            font-weight: 500 !important;
        }
        
        /* تحسين الخط والقراءة */
        .stMarkdown {
            font-size: 16px !important;
            line-height: 1.6 !important;
            color: #e2e2e2 !important;
        }
        
        /* تحسين المسافات بين العناصر */
        .element-container {
            margin: 1.5rem 0 !important;
        }
        
        /* تحسين النصوص والعناصر الأخرى */
        .stMarkdown {
            color: #e2e2e2;
        }
        
        /* تحسين الروابط */
        a {
            color: #4f8fba !important;
            text-decoration: none !important;
            transition: all 0.3s ease;
        }
        a:hover {
            color: #6ba5d1 !important;
            text-decoration: none !important;
        }
        
        /* تحسين تأثير الضغط على الدجاجة */
        .emoji-link {
            font-size: 24px;
            text-decoration: none;
            transition: all 0.3s ease;
            display: inline-block;
            margin-right: 8px;
            filter: drop-shadow(0 0 8px rgba(255,255,255,0.2));
        }
        
        .emoji-link:hover {
            transform: scale(1.2);
            filter: drop-shadow(0 0 12px rgba(255,255,255,0.4));
        }
        
        .emoji-link:active {
            transform: scale(0.95);
        }
        
        /* تحسين العنوان */
        .title {
            font-size: 32px;
            font-weight: bold;
            margin-bottom: 12px;
            text-align: center;
            background: linear-gradient(120deg, #ffffff, #e2e2e2);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        .title-text {
            text-decoration: none;
            color: inherit;
            margin-left: 8px;
        }
        
        /* تحسين القوائم المنسدلة */
        .stSelectbox > div > div {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            color: #ffffff !important;
            backdrop-filter: blur(10px);
            transition: all 0.3s ease;
            padding: 12px !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            height: auto !important;
            min-height: 48px !important;
            font-size: 16px !important;
            line-height: 1.5 !important;
        }
        
        /* تحسين قائمة الخيارات المنسدلة */
        div[data-baseweb="select"] > div {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            backdrop-filter: blur(10px) !important;
            border-radius: 8px !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
            padding: 8px !important;
            min-width: 200px !important;
        }
        
        div[data-baseweb="select"] ul {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            padding: 4px !important;
        }
        
        div[data-baseweb="select"] ul li {
            color: #ffffff !important;
            font-size: 16px !important;
            padding: 12px !important;
            margin: 4px 0 !important;
            border-radius: 6px !important;
            line-height: 1.5 !important;
        }
        
        /* تحسين النصوص في القوائم */
        .stSelectbox label {
            color: #ffffff !important;
            font-size: 18px !important;
            font-weight: 500 !important;
            margin-bottom: 12px !important;
            text-shadow: 0 1px 2px rgba(0,0,0,0.1);
            line-height: 1.5 !important;
        }
        
        /* تحسين الأيقونة في القائمة المنسدلة */
        .stSelectbox svg {
            fill: #ffffff !important;
            width: 24px !important;
            height: 24px !important;
        }
        
        /* تحسين العنوان */
        .subtitle {
            font-size: 18px;
            color: #b8b8b8;
            margin-bottom: 24px;
            text-align: center;
        }
        
        /* تحسين أزرار الحساب */
        .stButton > button {
            background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05)) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            color: #e2e2e2 !important;
            border-radius: 8px !important;
            padding: 8px 16px !important;
            font-weight: 500 !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(10px);
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
        }
        
        .stButton > button:hover {
            background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.1)) !important;
            border-color: rgba(255,255,255,0.3) !important;
            transform: translateY(-2px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.15);
        }
        
        .stButton > button:active {
            transform: translateY(0);
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        
        /* تحسين حقول الإدخال */
        .stNumberInput > div > div > input {
            background: linear-gradient(135deg, #1e212b 0%, #161b25 100%) !important;
            border: 1px solid rgba(255, 255, 255, 0.15) !important;
            border-radius: 8px !important;
            color: #e2e2e2 !important;
            padding: 8px 12px !important;
            transition: all 0.3s ease;
        }
        
        .stNumberInput > div > div > input:focus {
            border-color: rgba(255, 255, 255, 0.3) !important;
            box-shadow: 0 0 0 2px rgba(255,255,255,0.1) !important;
        }
        
        /* تحسين حقوق النشر */
        .copyright {
            text-align: center;
            color: rgba(255,255,255,0.5);
            padding: 16px;
            font-size: 14px;
            margin-top: 32px;
            border-top: 1px solid rgba(255,255,255,0.1);
        }
        
        /* تحسين الشريط العلوي */
        .stProgress > div > div {
            background: rgba(30, 37, 48, 0.7) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            border-radius: 8px !important;
            overflow: hidden;
            position: relative;
            height: 48px !important;
            box-shadow: 0 2px 6px rgba(0,0,0,0.1);
            backdrop-filter: blur(10px);
        }
        
        .stProgress > div > div > div {
            background: linear-gradient(90deg, 
                rgba(255,255,255,0.1),
                rgba(255,255,255,0.15),
                rgba(255,255,255,0.1)
            ) !important;
            border-radius: 6px !important;
            height: 100% !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(5px);
        }
        
        .stProgress > div > div::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(255, 255, 255, 0.05),
                transparent
            );
            transition: all 0.5s ease;
            z-index: 1;
        }
        
        .stProgress > div > div:hover::before {
            left: 100%;
        }
        
        .stProgress > div > div:hover {
            background: rgba(22, 27, 37, 0.8) !important;
            border-color: rgba(255, 255, 255, 0.3) !important;
            transform: translateY(-1px);
            box-shadow: 0 4px 12px rgba(0,0,0,0.2);
        }
        
        /* تحديث شفافية القوائم المنسدلة */
        .stSelectbox > div > div,
        .stNumberInput > div > div {
            background: rgba(30, 37, 48, 0.7) !important;
            backdrop-filter: blur(10px);
        }
        
        .stSelectbox > div > div:hover,
        .stNumberInput > div > div:hover {
            background: rgba(22, 27, 37, 0.8) !important;
        }
        
        div[data-baseweb="select"] > div,
        div[data-baseweb="popover"] > div {
            background: rgba(30, 37, 48, 0.7) !important;
            backdrop-filter: blur(10px) !important;
        }
        
        div[data-baseweb="select"] ul,
        div[data-baseweb="menu"] ul {
            background: rgba(30, 37, 48, 0.7) !important;
            backdrop-filter: blur(10px);
        }
        
        div[data-baseweb="select"] ul li:hover,
        div[data-baseweb="menu"] ul li:hover {
            background: rgba(22, 27, 37, 0.8) !important;
        }
        
        /* تحسين ملخص النتائج */
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
                background-position: 0% 50%;
            }
            50% {
                background-position: 100% 50%;
            }
            100% {
                background-position: 0% 50%;
            }
        }

        .stApp {
            background: linear-gradient(-45deg, #1e3c72, #2a5298, #2c3e50, #3498db) !important;
            background-size: 400% 400% !important;
            animation: gradientBG 8s ease infinite !important;
        }

        /* تنسيق الأزرار */
        .stButton > button {
            background: linear-gradient(135deg, #3498db, #2980b9) !important;
            border: 1px solid rgba(255,255,255,0.2) !important;
            color: white !important;
            transition: all 0.3s ease !important;
        }

        .stButton > button:hover {
            background: linear-gradient(135deg, #2980b9, #3498db) !important;
            transform: translateY(-2px) !important;
            box-shadow: 0 5px 15px rgba(0,0,0,0.2) !important;
        }

        /* تنسيق مربعات الإدخال */
        .stTextInput > div > div > input {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            color: white !important;
            transition: all 0.3s ease !important;
        }

        .stTextInput > div > div > input:focus {
            border-color: #3498db !important;
            box-shadow: 0 0 10px rgba(52, 152, 219, 0.5) !important;
        }

        /* تنسيق القوائم المنسدلة */
        div[data-baseweb="select"] {
            background: rgba(255, 255, 255, 0.1) !important;
            border: 1px solid rgba(255, 255, 255, 0.2) !important;
            transition: all 0.3s ease !important;
        }

        div[data-baseweb="select"]:hover {
            border-color: #3498db !important;
            box-shadow: 0 0 10px rgba(52, 152, 219, 0.5) !important;
        }
    </style>
""", unsafe_allow_html=True)

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تعريف النصوص بجميع اللغات
texts = {
    "العربية": {
        "title": "حاسبة نيويورك",
        "subtitle": "حساب أرباح الدجاج والمكافآت اليومية",
        "language": "اللغة 🌍",
        "currency": "العملة 💵",
        "egg_price": "سعر البيض الحالي 🥚",
        "feed_price": "سعر العلف الحالي 🌾",
        "new_egg_price": "سعر البيض الجديد",
        "new_feed_price": "سعر العلف الجديد",
        "save_prices": "💾 حفظ الأسعار",
        "reset": "إعادة التعيين",
        "success_save": "تم حفظ الأسعار الجديدة بنجاح!",
        "success_reset": "تم إعادة التعيين بنجاح!",
        "error_numbers": "يرجى إدخال أرقام صحيحة ❗️"
    },
    "English": {
        "title": "NewYolk Calculator",
        "subtitle": "Calculate Chicken Profits and Daily Rewards",
        "language": "Language 🌍",
        "currency": "Currency 💵",
        "egg_price": "Current Egg Price 🥚",
        "feed_price": "Current Feed Price 🌾",
        "new_egg_price": "New Egg Price",
        "new_feed_price": "New Feed Price",
        "save_prices": "💾 Save Prices",
        "reset": "Reset",
        "success_save": "New prices saved successfully!",
        "success_reset": "Reset completed successfully!",
        "error_numbers": "Please enter valid numbers! ❗️"
    }
}

# اختيار اللغة
language = st.selectbox(
    texts[language]["language"],
    ["العربية", "English"],
    key="language_selector"
)

# تحسين الواجهة
st.markdown(
    f"""
    <style>
        .stApp {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
        }}
        .title {{
            font-size: 36px;
            font-weight: bold;
            text-align: center;
            padding: 20px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .subtitle {{
            font-size: 24px;
            text-align: center;
            margin-bottom: 30px;
            white-space: nowrap;
            overflow: hidden;
            text-overflow: ellipsis;
        }}
        .stButton {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
            text-align: {'right' if language == 'العربية' else 'left'};
            font-size: 24px;
        }}
        .stSelectbox, .stTextInput {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
            text-align: {'right' if language == 'العربية' else 'left'};
            font-size: 24px;
        }}
        .stButton button {{
            font-size: 24px;
            padding: 10px 24px;
            border-radius: 12px;
            width: 100%;
        }}
        .stTable th, .stTable td {{
            text-align: {'right' if language == 'العربية' else 'left'} !important;
            direction: {'rtl' if language == 'العربية' else 'ltr'} !important;
        }}
        [data-testid="stMarkdownContainer"] {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
            text-align: {'right' if language == 'العربية' else 'left'};
        }}
        .element-container {{
            direction: {'rtl' if language == 'العربية' else 'ltr'};
        }}
        thead tr th:first-child {{
            text-align: {'right' if language == 'العربية' else 'left'} !important;
        }}
        tbody tr td:first-child {{
            text-align: {'right' if language == 'العربية' else 'left'} !important;
        }}
    </style>
    <div class="main-title">
        {texts[language]["title"]}
        <a href="https://newyolkcalculator.streamlit.app" target="_blank" class="chicken-emoji">🐔</a>
        <div class="subtitle">
            {texts[language]["subtitle"]}
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

st.markdown("""
    <style>
        .main-title {
            font-size: 2.5em !important;
            font-weight: bold !important;
            text-align: center !important;
            margin-bottom: 0.2em !important;
            color: #ffffff !important;
            text-shadow: 0 0 10px rgba(255,255,255,0.3);
        }
        
        .subtitle {
            font-size: 0.7em;
            text-align: center;
            margin-top: 0.5em;
            color: #e2e2e2;
            opacity: 0.9;
            font-weight: normal;
        }
    </style>
""", unsafe_allow_html=True)

# استخدام الأعمدة لتخطيط أفضل
col1, col2 = st.columns(2)

with col1:
    currency = st.selectbox(
        texts[language]["currency"],
        ["USD", "IQD"]
    )

with col2:
    calculation_type = st.selectbox(
        "Calculation Type 📊",
        ["Chicken Profits", "Daily Rewards"]
    )

# دالة التحقق من المدخلات
def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# قسم تعديل الأسعار
st.subheader("💾 Save Prices")
col3, col4 = st.columns(2)

with col3:
    new_egg_price = st.text_input(
        texts[language]["new_egg_price"],
        value="0.1155"
    )

with col4:
    new_feed_price = st.text_input(
        texts[language]["new_feed_price"],
        value="0.0189"
    )

st.markdown("""
    <style>
        /* تنسيق رسائل النجاح */
        .success-message {
            background: linear-gradient(135deg, rgba(20, 30, 48, 0.95), rgba(5, 8, 15, 0.95));
            border: 1px solid rgba(218, 165, 32, 0.3);
            border-radius: 10px;
            color: rgba(218, 165, 32, 0.9);
            padding: 1rem;
            margin: 1rem 0;
            backdrop-filter: blur(10px);
            box-shadow: 
                0 4px 20px rgba(0, 0, 0, 0.3),
                0 0 30px rgba(218, 165, 32, 0.1);
            position: relative;
            overflow: hidden;
            display: flex;
            align-items: center;
            gap: 10px;
        }

        .success-message::before {
            content: '✓';
            font-size: 1.4em;
            font-weight: bold;
            background: linear-gradient(135deg, rgba(218, 165, 32, 0.9), rgba(218, 165, 32, 0.7));
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            margin-right: 10px;
        }

        .success-message::after {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 100%;
            height: 100%;
            background: linear-gradient(
                90deg,
                transparent,
                rgba(218, 165, 32, 0.1),
                transparent
            );
            animation: shine 2s infinite;
        }

        @keyframes shine {
            to {
                left: 100%;
            }
        }
    </style>
""", unsafe_allow_html=True)

if st.button(texts[language]["save_prices"], type="secondary"):
    if not is_number(new_egg_price) or not is_number(new_feed_price):
        st.error(texts[language]["error_numbers"])
    else:
        st.markdown(f"""
            <div class="success-message">
                {texts[language]["success_save"]}
            </div>
        """, unsafe_allow_html=True)

# تحديث الأسعار بناءً على العملة
if is_number(new_egg_price) and is_number(new_feed_price):
    if currency == "IQD":
        egg_price_display = float(new_egg_price) * 1480
        feed_price_display = float(new_feed_price) * 1480
    else:
        egg_price_display = float(new_egg_price)
        feed_price_display = float(new_feed_price)

    col1, col2 = st.columns(2)

    with col2:
        st.markdown(f'<div style="text-align: right; font-size: 18px; color: var(--text); padding: 10px; background: rgba(45, 91, 133, 0.1); border-radius: 8px; backdrop-filter: blur(10px); border: 1px solid var(--border);">{texts[language]["egg_price"]} : USD {format_decimal(egg_price_display)}</div>', unsafe_allow_html=True)

    with col1:
        st.markdown(f'<div style="text-align: left; font-size: 18px; color: var(--text); padding: 10px; background: rgba(45, 91, 133, 0.1); border-radius: 8px; backdrop-filter: blur(10px); border: 1px solid var(--border);">{texts[language]["feed_price"]} : USD {format_decimal(feed_price_display)}</div>', unsafe_allow_html=True)

# دالة إنشاء الرسم البياني
def create_profit_chart(df, language):
    # تخصيص الألوان
    colors = {
        'عدد البيض 🥚': '#4CAF50',
        'عدد الطعام المطلوب 🌽': '#FF9800',
        'الربح قبل الإيجار 📊': '#2196F3',
        'دفع الإيجار 🏠': '#F44336',
        'صافي الربح 💰': '#9C27B0'
    }
    
    # إنشاء الرسم البياني
    fig = px.pie(
        df,
        values=texts[language]["value"],
        names=texts[language]["category"],
        title=texts[language]["summary"],
        color_discrete_sequence=['#4CAF50', '#FF9800', '#2196F3', '#F44336', '#9C27B0']
    )
    
    # تحديث تصميم الرسم البياني
    fig.update_traces(
        textposition='outside',
        textinfo='percent+label'
    )
    
    fig.update_layout(
        title_x=0.5,
        title_font_size=24,
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.2,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=60, l=0, r=0, b=0),
        height=500,
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    
    return fig

if calculation_type == "Chicken Profits":
    st.subheader("Chicken Profits 📈")
    col5, col6 = st.columns(2)

    with col5:
        eggs = st.text_input(
            "Number of Eggs 🥚",
            value="",
            help="Enter the number of eggs (max 580)"
        )

    with col6:
        days = st.text_input(
            "Number of Days 📅",
            value="",
            help="Enter the number of days (max 730)"
        )

    if st.button("Calculate Profits 🧮", type="primary"):
        try:
            eggs = float(eggs) if eggs else None
            days = float(days) if days else None

            if eggs is None or days is None:
                st.error("Please enter all required values! ❗️")
            elif eggs > 580:
                st.error("Number of eggs should not exceed 580! ❗️")
            elif days > 730:
                st.error("Number of days should not exceed 730! ❗️")
            else:
                # حساب الأرباح
                total_egg_price = eggs * float(new_egg_price)  # ضرب عدد البيض في سعر البيض الحالي
                total_feed_cost = (days * 2) * float(new_feed_price)  # ضرب عدد الأيام في 2 ثم في سعر العلف الحالي
                
                # حساب الإيجار
                total_rent = 6 if eggs >= 260 else 0  # 6 دولار فقط إذا كان عدد البيض 260 أو أكثر
                
                # حساب النتائج
                net_profit_before_rent = total_egg_price - total_feed_cost
                net_profit = net_profit_before_rent - total_rent

                # تحويل العملة
                if currency == "IQD":
                    total_egg_price = total_egg_price * 1480
                    total_feed_cost = total_feed_cost * 1480
                    net_profit_before_rent = net_profit_before_rent * 1480
                    total_rent = total_rent * 1480
                    net_profit = net_profit * 1480
                else:
                    total_egg_price, total_feed_cost, net_profit_before_rent, total_rent, net_profit = (
                        total_egg_price, total_feed_cost, net_profit_before_rent, total_rent, net_profit
                    )

                # تنسيق التاريخ والوقت حسب توقيت بغداد
                current_time = datetime.now() + timedelta(hours=3)  # تحويل التوقيت إلى توقيت بغداد
                date_str = current_time.strftime("%Y-%m-%d")
                time_str = current_time.strftime("%I:%M %p")

                # إنشاء نص النتائج
                results_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                  Results Summary                    ║
╠══════════════════════════════════════════════════════════════════╣
║ Calculation Time: {date_str} {time_str}
╟──────────────────────────────────────────────────────────────────╢
║ USD Results:
║ Egg Price: {format_decimal(total_egg_price)} USD
║ Feed Price: {format_decimal(total_feed_cost)} USD
║ Net Profit: {format_decimal(net_profit_before_rent)} USD
║ Rental: {format_decimal(total_rent)} USD
║ Final Profit: {format_decimal(net_profit)} USD
╟──────────────────────────────────────────────────────────────────╢
║ IQD Results:
║ Egg Price: {format_decimal(total_egg_price * 1480)} IQD
║ Feed Price: {format_decimal(total_feed_cost * 1480)} IQD
║ Net Profit: {format_decimal(net_profit_before_rent * 1480)} IQD
║ Rental: {format_decimal(total_rent * 1480)} IQD
║ Final Profit: {format_decimal(net_profit * 1480)} IQD
╚══════════════════════════════════════════════════════════════════╝"""

                # عرض النتائج
                # st.code(results_text, language="text")

                # إنشاء DataFrame للرسم البياني
                df = pd.DataFrame({
                    "Category": [
                        "🥚 Number of Eggs",
                        "🌽 Number of Food Needed",
                        "📈 Net Profit",
                        "🏠 Rental",
                        "💰 Final Profit"
                    ],
                    "Value": [
                        total_egg_price,
                        total_feed_cost,
                        net_profit_before_rent,
                        total_rent,
                        net_profit
                    ]
                })
                
                # تنسيق الجدول النهائي أولاً
                df = df.round(2)
                df["Value"] = df["Value"].apply(lambda x: f"{format_decimal(x)} {currency}")
                st.table(df)

                # عرض الرسم البياني
                chart_df = pd.DataFrame({
                    "Category": [
                        "🥚 Number of Eggs",
                        "🌽 Number of Food Needed",
                        "📈 Net Profit",
                        "🏠 Rental",
                        "💰 Final Profit"
                    ],
                    "Value": [
                        float(str(total_egg_price).replace(currency, "").strip()),
                        float(str(total_feed_cost).replace(currency, "").strip()),
                        float(str(net_profit_before_rent).replace(currency, "").strip()),
                        float(str(total_rent).replace(currency, "").strip()),
                        float(str(net_profit).replace(currency, "").strip())
                    ]
                })
                fig = create_profit_chart(chart_df, language)
                st.plotly_chart(fig, use_container_width=True)

                # عرض ملخص النتائج في النهاية
                st.markdown("### ✨ Results Summary")
                st.code(results_text)
                
        except ValueError:
            st.error("Please enter valid numbers! ❗️")
                
elif calculation_type == "Daily Rewards":
    st.subheader("Daily Rewards 📈")
    col7, col8 = st.columns(2)

    with col7:
        rewards = st.text_input(
            "Total Rewards",
            value="",
            help="Enter the number of rewards"
        )

    with col8:
        food = st.text_input(
            "Total Food Needed",
            value="",
            help="Enter the amount of food needed"
        )

    if st.button("Calculate Rewards ✨", type="primary"):
        try:
            rewards = float(rewards) if rewards else None
            food = float(food) if food else None

            if rewards is None or food is None:
                st.error("Please enter all required values! ❗️")
            else:
                # حساب الربح اليومي
                daily_profit = rewards * float(new_egg_price) - food * float(new_feed_price)

                # تحويل العملة
                if currency == "IQD":
                    daily_profit = daily_profit * 1480
                else:
                    daily_profit = daily_profit

                # تنسيق التاريخ والوقت حسب توقيت بغداد
                current_time = datetime.now() + timedelta(hours=3)  # تحويل التوقيت إلى توقيت بغداد
                date_str = current_time.strftime("%Y-%m-%d")
                time_str = current_time.strftime("%I:%M %p")

                # إنشاء نص النتائج
                results_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║ Calculation Time: {date_str} {time_str}
╟──────────────────────────────────────────────────────────────────╢
║ USD Results:
║ Egg Price: {format_decimal(rewards * float(new_egg_price))} USD
║ Feed Price: {format_decimal(food * float(new_feed_price))} USD
║ Daily Profit: {format_decimal(daily_profit)} USD
╟──────────────────────────────────────────────────────────────────╢
║ IQD Results:
║ Egg Price: {format_decimal(rewards * float(new_egg_price) * 1480)} IQD
║ Feed Price: {format_decimal(food * float(new_feed_price) * 1480)} IQD
║ Daily Profit: {format_decimal(daily_profit * 1480)} IQD
╚══════════════════════════════════════════════════════════════════╝"""

                # عرض النتائج
                # st.code(results_text, language="text")

                # إنشاء DataFrame للرسم البياني
                df = pd.DataFrame({
                    "Category": [
                        "🥚 Total Rewards",
                        "🌽 Total Food Needed",
                        "💰 Daily Profit"
                    ],
                    "Value": [
                        rewards * float(new_egg_price),
                        food * float(new_feed_price),
                        daily_profit
                    ]
                })
                
                # تنسيق القيم في الجدول
                df = df.round(2)
                df["Value"] = df["Value"].apply(lambda x: f"{format_decimal(x)} {currency}")
                st.table(df)

                # عرض الرسم البياني
                chart_df = pd.DataFrame({
                    "Category": [
                        "🥚 Total Rewards",
                        "🌽 Total Food Needed",
                        "💰 Daily Profit"
                    ],
                    "Value": [
                        float(str(rewards * float(new_egg_price)).replace(currency, "").strip()),
                        float(str(food * float(new_feed_price)).replace(currency, "").strip()),
                        float(str(daily_profit).replace(currency, "").strip())
                    ]
                })
                fig = create_profit_chart(chart_df, language)
                st.plotly_chart(fig, use_container_width=True)

                # عرض ملخص النتائج في النهاية
                st.markdown("### ✨ Results Summary")
                st.code(results_text)
                
        except ValueError:
            st.error("Please enter valid numbers! ❗️")

# زر إعادة التعيين
if st.button(texts[language]["reset"], type="secondary"):
    st.markdown(f"""
        <div class="success-message">
            {texts[language]["success_reset"]}
        </div>
    """, unsafe_allow_html=True)

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
            <img src="https://cdn-icons-png.flaticon.com/512/3059/3059997.png" alt="Website">
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
        /* تنسيق زر التمرير للأعلى */
        .scroll-to-top {
            position: fixed !important;
            bottom: min(30px, 5vh) !important;
            left: min(30px, 5vw) !important;
            width: clamp(45px, 5vw + 30px, 65px) !important;
            height: clamp(45px, 5vw + 30px, 65px) !important;
            background: linear-gradient(
                135deg,
                rgba(20, 30, 48, 0.98),
                rgba(5, 8, 15, 0.98)
            ) !important;
            border: 2px solid rgba(218, 165, 32, 0.7) !important;
            border-radius: 50% !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            cursor: pointer !important;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 
                0 4px 20px rgba(0, 0, 0, 0.4),
                0 0 30px rgba(218, 165, 32, 0.2),
                inset 0 0 20px rgba(218, 165, 32, 0.1),
                0 0 0 2px rgba(20, 30, 48, 0.5) !important;
            backdrop-filter: blur(15px) !important;
            z-index: 9999 !important;
            opacity: 0.98 !important;
            text-decoration: none !important;
            overflow: hidden !important;
            transform-style: preserve-3d !important;
            perspective: 1000px !important;
        }

        .scroll-to-top::before {
            content: '↑' !important;
            color: rgba(218, 165, 32, 0.9) !important;
            font-size: clamp(24px, 2.5vw + 16px, 32px) !important;
            font-weight: bold !important;
            text-shadow: 
                0 2px 5px rgba(0, 0, 0, 0.5),
                0 0 15px rgba(218, 165, 32, 0.5),
                0 0 30px rgba(218, 165, 32, 0.3) !important;
            transition: all 0.4s ease !important;
            position: relative !important;
            z-index: 2 !important;
        }

        .scroll-to-top::after {
            content: '' !important;
            position: absolute !important;
            top: 0 !important;
            left: -100% !important;
            width: 100% !important;
            height: 100% !important;
            background: radial-gradient(
                circle at center,
                rgba(218, 165, 32, 0.15),
                transparent 70%
            ) !important;
            animation: rotateGlow 8s linear infinite !important;
            filter: blur(5px) !important;
        }

        @keyframes rotateGlow {
            0% { transform: rotate(0deg); }
            100% { transform: rotate(360deg); }
        }

        @keyframes float {
            0% { transform: translateY(0) rotate(0deg); }
            25% { transform: translateY(-8px) rotate(3deg); }
            50% { transform: translateY(0) rotate(0deg); }
            75% { transform: translateY(-4px) rotate(-3deg); }
            100% { transform: translateY(0) rotate(0deg); }
        }

        .scroll-to-top {
            animation: float 6s ease-in-out infinite !important;
        }

        .scroll-to-top:hover {
            transform: scale(1.1) !important;
            box-shadow: 
                0 8px 30px rgba(0, 0, 0, 0.6),
                0 0 40px rgba(218, 165, 32, 0.4),
                inset 0 0 30px rgba(218, 165, 32, 0.2),
                0 0 0 2px rgba(218, 165, 32, 0.5) !important;
            border-color: rgba(218, 165, 32, 0.9) !important;
            opacity: 1 !important;
        }

        .scroll-to-top:hover::before {
            transform: scale(1.2) translateY(-3px) !important;
            text-shadow: 
                0 4px 8px rgba(0, 0, 0, 0.6),
                0 0 20px rgba(218, 165, 32, 0.6),
                0 0 40px rgba(218, 165, 32, 0.4) !important;
            color: rgba(218, 165, 32, 1) !important;
        }

        /* تنسيق التلميح */
        .scroll-to-top-wrapper {
            position: relative !important;
            display: inline-block !important;
        }

        .scroll-to-top-wrapper::after {
            content: 'Go to Top' !important;
            position: absolute !important;
            bottom: 100% !important;
            left: 50% !important;
            transform: translateX(-50%) scale(0.95) translateZ(0) !important;
            padding: clamp(8px, 1vw + 8px, 15px) clamp(12px, 1.5vw + 10px, 20px) !important;
            background: linear-gradient(
                135deg,
                rgba(20, 30, 48, 0.98),
                rgba(5, 8, 15, 0.98)
            ) !important;
            color: rgba(218, 165, 32, 0.9) !important;
            border-radius: 10px !important;
            font-size: clamp(14px, 1vw + 12px, 18px) !important;
            font-weight: 600 !important;
            white-space: nowrap !important;
            opacity: 0 !important;
            transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1) !important;
            pointer-events: none !important;
            border: 1px solid rgba(218, 165, 32, 0.3) !important;
            backdrop-filter: blur(15px) !important;
            box-shadow: 
                0 4px 20px rgba(0, 0, 0, 0.4),
                0 0 30px rgba(218, 165, 32, 0.2),
                inset 0 0 20px rgba(218, 165, 32, 0.1) !important;
            text-shadow: 
                0 2px 4px rgba(0, 0, 0, 0.4),
                0 0 10px rgba(218, 165, 32, 0.4) !important;
        }

        .scroll-to-top-wrapper:hover::after {
            opacity: 1 !important;
            bottom: 140% !important;
            transform: translateX(-50%) scale(1) translateZ(0) !important;
            border-color: rgba(218, 165, 32, 0.5) !important;
        }

        /* تحسين التجاوب مع الشاشات الصغيرة */
        @media (max-width: 768px) {
            .scroll-to-top {
                bottom: min(20px, 3vh) !important;
                left: min(20px, 3vw) !important;
            }

            .scroll-to-top-wrapper::after {
                display: none !important;
            }
        }
    </style>

    <div class="scroll-to-top-wrapper">
        <a href="https://testnewyolkcalculatortest.streamlit.app/~/+/#2e08c909" target="_self" class="scroll-to-top"></a>
    </div>
""", unsafe_allow_html=True)

st.markdown("""
    <script>
        function scrollToTop() {
            window.location.href = 'https://testnewyolkcalculatortest.streamlit.app/~/+/#2e08c909';
        }
    </script>
    <a href="https://testnewyolkcalculatortest.streamlit.app/~/+/#2e08c909" target="_self" class="scroll-to-top"></a>
""", unsafe_allow_html=True)

st.markdown("""
    <style>
        /* الألوان الأساسية */
        :root {
            --dark-primary: #0A0F1C;    /* أزرق داكن جداً */
            --dark-secondary: #1A1F35;  /* أزرق رمادي داكن */
            --accent: #2D5B85;         /* أزرق فخم */
            --highlight: #446B8C;      /* أزرق فاتح راقي */
            --gold: #9B8B6C;          /* ذهبي فخم */
            --text: #E6E9F0;          /* أبيض مائل للرمادي */
            --border: rgba(155, 139, 108, 0.15);  /* حدود ذهبية شفافة */
            --glow: rgba(155, 139, 108, 0.2);    /* توهج ذهبي خفيف */
        }

        /* تأثيرات الحركة والخلفية */
        @keyframes subtleGradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }

        .stApp {
            background: linear-gradient(
                135deg,
                var(--dark-primary),
                var(--dark-secondary),
                var(--accent),
                var(--dark-primary)
            ) !important;
            background-size: 200% 200% !important;
            animation: subtleGradient 10s ease infinite !important;
        }

        /* تنسيق الأزرار */
        .stButton > button {
            background: linear-gradient(
                135deg,
                var(--accent),
                var(--dark-secondary)
            ) !important;
            border: 1px solid var(--gold) !important;
            color: var(--text) !important;
            padding: 0.7rem 1.4rem !important;
            border-radius: 8px !important;
            font-weight: 500 !important;
            transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1) !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2) !important;
            backdrop-filter: blur(10px) !important;
        }

        .stButton > button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 8px 25px var(--glow) !important;
            border-color: var(--gold) !important;
        }

        /* تنسيق العناوين */
        .stHeader {
            position: relative !important;
            margin-bottom: 2rem !important;
            padding-bottom: 0.5rem !important;
            color: var(--text) !important;
        }

        .stHeader::after {
            content: '' !important;
            position: absolute !important;
            bottom: 0 !important;
            left: 0 !important;
            width: 100% !important;
            height: 1px !important;
            background: linear-gradient(90deg, transparent, var(--gold), transparent) !important;
            opacity: 0.5 !important;
        }

        /* تنسيق المدخلات */
        .stTextInput > div > div > input,
        div[data-baseweb="select"] {
            background: rgba(10, 15, 28, 0.7) !important;
            border: 1px solid var(--border) !important;
            color: var(--text) !important;
            border-radius: 8px !important;
            transition: all 0.3s ease !important;
            backdrop-filter: blur(10px) !important;
        }

        .stTextInput > div > div > input:focus,
        div[data-baseweb="select"]:hover {
            border-color: var(--gold) !important;
            box-shadow: 0 0 15px var(--glow) !important;
            transform: translateY(-1px) !important;
        }

        /* تنسيق الجداول والإطارات */
        .stDataFrame, pre {
            background: rgba(10, 15, 28, 0.7) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
            backdrop-filter: blur(10px) !important;
        }

        .stDataFrame:hover, pre:hover {
            border-color: var(--gold) !important;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3) !important;
        }

        /* تنسيق الرسوم البيانية */
        .js-plotly-plot {
            background: rgba(10, 15, 28, 0.7) !important;
            border: 1px solid var(--border) !important;
            border-radius: 10px !important;
            box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
            backdrop-filter: blur(10px) !important;
        }

        .js-plotly-plot:hover {
            border-color: var(--gold) !important;
            box-shadow: 0 12px 40px rgba(0, 0, 0, 0.3) !important;
        }

        /* تنسيق النصوص */
        .stMarkdown {
            color: var(--text) !important;
        }

        .dataframe {
            color: var(--text) !important;
        }

        /* إخفاء العناصر غير الضرورية */
        #MainMenu {visibility: hidden !important;}
        footer {visibility: hidden !important;}
        header {visibility: hidden !important;}

    </style>
""", unsafe_allow_html=True)
