import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تعيين إعدادات الصفحة
st.set_page_config(
    page_title="حاسبة نيويورك",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# إضافة CSS للتحكم في المظهر
st.markdown("""
    <style>
        /* إخفاء عناصر Streamlit */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* تصميم عام للصفحة */
        .stApp {
            background: var(--background-color);
            color: var(--text-color);
        }
        
        /* متغيرات الألوان للوضع الداكن */
        [data-theme="dark"] {
            --background-color: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            --text-color: #ffffff;
            --calculator-bg: rgba(255,255,255,0.1);
            --button-bg: rgba(255,255,255,0.1);
            --button-hover: rgba(255,255,255,0.2);
            --display-bg: rgba(0,0,0,0.3);
        }
        
        /* متغيرات الألوان للوضع الفاتح */
        [data-theme="light"] {
            --background-color: linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%);
            --text-color: #000000;
            --calculator-bg: rgba(0,0,0,0.05);
            --button-bg: rgba(0,0,0,0.1);
            --button-hover: rgba(0,0,0,0.2);
            --display-bg: rgba(255,255,255,0.9);
        }
        
        /* تصميم الحاسبة */
        .calculator-container {
            display: none;
            background: var(--calculator-bg);
            border-radius: 25px;
            padding: 30px;
            max-width: 500px;
            margin: 20px auto;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        }
        
        /* إظهار الحاسبة فقط في قسم الحاسبة البسيطة */
        .show-calculator .calculator-container {
            display: block;
        }
        
        /* شاشة العرض */
        .calculator-display {
            background: var(--display-bg);
            color: var(--text-color);
            padding: 30px;
            border-radius: 20px;
            margin-bottom: 25px;
            text-align: right;
            font-family: 'Roboto Mono', monospace;
            font-size: 40px;
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: inset 0 2px 10px rgba(0,0,0,0.2);
        }
        
        .operation-display {
            font-size: 20px;
            color: var(--text-color);
            opacity: 0.7;
            margin-bottom: 10px;
        }
        
        /* تصميم الأزرار */
        .stButton > button {
            background: var(--button-bg) !important;
            color: var(--text-color) !important;
            border: 1px solid rgba(255,255,255,0.1) !important;
            border-radius: 15px !important;
            width: 100% !important;
            padding: 25px 0 !important;
            font-size: 24px !important;
            margin: 5px !important;
            transition: all 0.3s !important;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2) !important;
            backdrop-filter: blur(5px) !important;
        }
        
        .stButton > button:hover {
            background: var(--button-hover) !important;
            transform: translateY(-2px) !important;
        }
        
        /* تحسين المسافات */
        div[data-testid="stHorizontalBlock"] {
            gap: 0.5rem !important;
            padding: 0.25rem !important;
        }
        
        /* تخصيص أزرار العمليات */
        .operation-button {
            background: linear-gradient(145deg, #4a90e2, #357abd) !important;
            color: white !important;
        }
        
        /* زر المساواة */
        .equals-button {
            background: linear-gradient(145deg, #2ecc71, #27ae60) !important;
            color: white !important;
        }
        
        /* زر المسح */
        .clear-button {
            background: linear-gradient(145deg, #e74c3c, #c0392b) !important;
            color: white !important;
        }
    </style>
""", unsafe_allow_html=True)

# تحديد الوضع الافتراضي
if 'theme' not in st.session_state:
    st.session_state.theme = 'light'

# تعريف النصوص
texts = {
    "العربية": {
        "title": "حاسبة نيويورك",
        "subtitle": "حساب أرباح الدجاج والمكافآت اليومية",
        "egg_price": "سعر البيض الحالي",
        "feed_price": "سعر العلف الحالي",
        "save_prices": "حفظ الأسعار الجديدة",
        "select_calculation": "اختر نوع الحساب",
        "chicken_profits": "حساب أرباح الدجاج",
        "simple_calculator": "الحاسبة البسيطة",
        "eggs_input": "عدد البيض",
        "days_input": "عدد الأيام",
        "calculate_profits": "حساب الأرباح",
        "reset": "إعادة تعيين",
        "theme_toggle": "تبديل المظهر ",
        "currency": "العملة"
    },
    "English": {
        "title": "Newyolk Calculator",
        "subtitle": "Calculate Chicken Profits and Daily Rewards",
        "egg_price": "Current Egg Price",
        "feed_price": "Current Feed Price",
        "save_prices": "Save New Prices",
        "select_calculation": "Select Calculation Type",
        "chicken_profits": "Chicken Profits",
        "simple_calculator": "Simple Calculator",
        "eggs_input": "Number of Eggs",
        "days_input": "Number of Days",
        "calculate_profits": "Calculate Profits",
        "reset": "Reset",
        "theme_toggle": "Toggle Theme ",
        "currency": "Currency"
    }
}

# اختيار اللغة
language = st.selectbox("اللغة | Language", ["العربية", "English"])

# زر تبديل الوضع
if st.sidebar.button(texts[language]["theme_toggle"]):
    st.session_state.theme = 'dark' if st.session_state.theme == 'light' else 'light'
    st.markdown(f"""
        <script>
            document.documentElement.setAttribute('data-theme', '{st.session_state.theme}');
        </script>
    """, unsafe_allow_html=True)

# اختيار نوع الحساب
calculation_type = st.selectbox(
    texts[language]["select_calculation"],
    [texts[language]["chicken_profits"], texts[language]["simple_calculator"]]
)

# إضافة class للتحكم في إظهار الحاسبة
if calculation_type == texts[language]["simple_calculator"]:
    st.markdown('<div class="show-calculator">', unsafe_allow_html=True)

    # متغيرات الحاسبة
    if 'calc_result' not in st.session_state:
        st.session_state.calc_result = '0'
    if 'prev_number' not in st.session_state:
        st.session_state.prev_number = None
    if 'operation' not in st.session_state:
        st.session_state.operation = None
    if 'clear_next' not in st.session_state:
        st.session_state.clear_next = False
    if 'display_operation' not in st.session_state:
        st.session_state.display_operation = ''

    # شاشة العرض
    st.markdown(f"""
        <div class="calculator-container">
            <div class="calculator-display">
                <div class="operation-display">{st.session_state.display_operation}</div>
                {st.session_state.calc_result}
            </div>
        </div>
    """, unsafe_allow_html=True)

    # أزرار التحكم
    col_control = st.columns(4)
    with col_control[0]:
        if st.button("C", key="clear", use_container_width=True):
            st.session_state.calc_result = '0'
            st.session_state.prev_number = None
            st.session_state.operation = None
            st.session_state.clear_next = False
            st.session_state.display_operation = ''
            st.rerun()

    with col_control[1]:
        if st.button("", key="backspace", use_container_width=True):
            if len(st.session_state.calc_result) > 1:
                st.session_state.calc_result = st.session_state.calc_result[:-1]
            else:
                st.session_state.calc_result = '0'
            st.rerun()

    with col_control[2]:
        if st.button("", key="sign", use_container_width=True):
            current = float(st.session_state.calc_result)
            st.session_state.calc_result = str(-current)
            st.rerun()

    with col_control[3]:
        if st.button("", key="divide", use_container_width=True):
            st.session_state.prev_number = float(st.session_state.calc_result)
            st.session_state.operation = '/'
            st.session_state.display_operation = f"{st.session_state.calc_result} "
            st.session_state.clear_next = True
            st.rerun()

    # صفوف الأرقام والعمليات
    for row, numbers in enumerate([['7', '8', '9', ''], ['4', '5', '6', '-'], ['1', '2', '3', '+'], ['0', '.', '00', '=']]):
        cols = st.columns(4)
        for i, num in enumerate(numbers):
            with cols[i]:
                key = f"button_{num}_{row}_{i}"
                if st.button(num, key=key, use_container_width=True):
                    if num == '=':
                        try:
                            if st.session_state.prev_number is not None and st.session_state.operation is not None:
                                num1 = st.session_state.prev_number
                                num2 = float(st.session_state.calc_result)
                                
                                if st.session_state.operation == '/' and num2 == 0:
                                    st.error("")
                                    result = 0
                                else:
                                    result = eval(f"{num1}{st.session_state.operation}{num2}")
                                
                                st.session_state.calc_result = str(result)
                                st.session_state.prev_number = None
                                st.session_state.operation = None
                                st.session_state.clear_next = True
                        except Exception as e:
                            st.error("")
                    elif num in ['+', '-', '', '']:
                        st.session_state.prev_number = float(st.session_state.calc_result)
                        st.session_state.operation = {'': '*', '': '/'}[num] if num in ['', ''] else num
                        st.session_state.display_operation = f"{st.session_state.calc_result} {num}"
                        st.session_state.clear_next = True
                    else:
                        if st.session_state.clear_next:
                            st.session_state.calc_result = num
                            st.session_state.clear_next = False
                        else:
                            if st.session_state.calc_result == '0' and num != '.':
                                st.session_state.calc_result = num
                            else:
                                if num == '.' and '.' in st.session_state.calc_result:
                                    pass
                                else:
                                    st.session_state.calc_result += num
                    st.rerun()

    st.markdown('</div>', unsafe_allow_html=True)

elif calculation_type == texts[language]["chicken_profits"]:
    st.subheader(texts[language]["chicken_profits"])
    
    # هنا يمكنك إضافة حساب أرباح الدجاج

# زر إعادة التعيين
if st.button(texts[language]["reset"]):
    st.success("" if language == "العربية" else "Reset successful")
    st.rerun()
