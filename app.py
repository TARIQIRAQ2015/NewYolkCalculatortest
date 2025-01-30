import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# تعيين إعدادات الصفحة
st.set_page_config(
    page_title="Future Calculator",
    page_icon="🌟",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# إضافة زر تبديل الوضع وتحسين التصميم
st.markdown("""
    <style>
        /* إخفاء عناصر Streamlit */
        #MainMenu {visibility: hidden;}
        header {visibility: hidden;}
        footer {visibility: hidden;}
        
        /* تصميم عصري للصفحة */
        .stApp {
            background: linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%);
            color: white;
        }
        
        /* تصميم الحاسبة */
        .calculator-container {
            background: linear-gradient(145deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            border-radius: 25px;
            padding: 30px;
            max-width: 500px;
            margin: 20px auto;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255,255,255,0.1);
            box-shadow: 0 8px 32px rgba(0,0,0,0.2);
        }
        
        /* شاشة العرض */
        .calculator-display {
            background: linear-gradient(145deg, rgba(0,0,0,0.4) 0%, rgba(0,0,0,0.2) 100%);
            color: white;
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
            color: rgba(255,255,255,0.6);
            margin-bottom: 10px;
        }
        
        /* تصميم الأزرار */
        .stButton > button {
            background: linear-gradient(145deg, rgba(255,255,255,0.1) 0%, rgba(255,255,255,0.05) 100%);
            color: white;
            border: 1px solid rgba(255,255,255,0.1);
            border-radius: 15px;
            width: 100%;
            padding: 25px 0;
            font-size: 24px;
            margin: 5px;
            transition: all 0.3s;
            box-shadow: 0 4px 15px rgba(0,0,0,0.2);
            backdrop-filter: blur(5px);
            font-weight: 500;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            background: linear-gradient(145deg, rgba(255,255,255,0.2) 0%, rgba(255,255,255,0.1) 100%);
            box-shadow: 0 6px 20px rgba(0,0,0,0.3);
        }
        
        .stButton > button:active {
            transform: translateY(1px);
        }
        
        /* أزرار العمليات */
        .stButton > button[data-baseweb="button"] {
            background: linear-gradient(145deg, #4a90e2 0%, #357abd 100%);
        }
        
        /* زر المساواة */
        button[kind="primary"] {
            background: linear-gradient(145deg, #2ecc71 0%, #27ae60 100%) !important;
        }
        
        /* زر المسح */
        [data-testid="stHorizontalBlock"] > div:first-child button {
            background: linear-gradient(145deg, #e74c3c 0%, #c0392b 100%);
        }
        
        /* زر الرجوع */
        [data-testid="stHorizontalBlock"] > div:nth-child(2) button {
            background: linear-gradient(145deg, #f39c12 0%, #d35400 100%);
        }
        
        /* زر تبديل الوضع */
        .theme-toggle {
            position: fixed;
            top: 20px;
            left: 20px;
            z-index: 1000;
            background: rgba(255,255,255,0.1);
            border: 1px solid rgba(255,255,255,0.2);
            color: white;
            font-size: 24px;
            width: 50px;
            height: 50px;
            border-radius: 50%;
            cursor: pointer;
            transition: all 0.3s;
            backdrop-filter: blur(5px);
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        .theme-toggle:hover {
            transform: rotate(180deg);
            background: rgba(255,255,255,0.2);
        }
        
        /* تحسين المسافات */
        div[data-testid="stHorizontalBlock"] {
            gap: 0.5rem;
            padding: 0.25rem;
        }
    </style>
    
    <div class="theme-toggle" id="themeToggle" onclick="toggleTheme()">
        🌙
    </div>
    
    <script>
        function toggleTheme() {
            const body = document.querySelector('.stApp');
            const themeToggle = document.getElementById('themeToggle');
            
            if (body.style.background.includes('1a1a1a')) {
                body.style.background = 'linear-gradient(135deg, #f5f5f5 0%, #e0e0e0 100%)';
                body.style.color = '#000000';
                themeToggle.innerHTML = '☀️';
            } else {
                body.style.background = 'linear-gradient(135deg, #1a1a1a 0%, #2d2d2d 100%)';
                body.style.color = '#ffffff';
                themeToggle.innerHTML = '🌙';
            }
        }
    </script>
""", unsafe_allow_html=True)

# بداية الحاسبة
st.markdown('<div class="calculator-container">', unsafe_allow_html=True)

# تعريف النصوص بجميع اللغات
texts = {
    "العربية": {
        "title": "🐔 حاسبة الدجاج - نيويولك",
        "subtitle": "حساب أرباح الدجاج والمكافآت اليومية",
        "language": "اللغة 🌍",
        "currency": "العملة 💵",
        "egg_price": "سعر البيض الحالي 🥚",
        "feed_price": "سعر العلف الحالي 🌽",
        "save_prices": "حفظ الأسعار الجديدة 💾",
        "calculation_type": "نوع الحساب 📊",
        "chicken_profits": "أرباح الدجاج 🐔",
        "daily_rewards": "المكافآت اليومية 🥚",
        "simple_calculator": "الحاسبة البسيطة 🔢",
        "eggs_input": "عدد البيض 🥚",
        "days_input": "عدد الأيام 📅",
        "food_input": "عدد الطعام المطلوب 🌽",
        "calculate_profits": "حساب الأرباح 🧮",
        "calculate_rewards": "حساب المكافآت 🥚",
        "reset": "إعادة تعيين 🔄",
        "value": "القيمة",
        "category": "الفئة",
        "net_profit": "الربح قبل حساب الايجار 📈",
        "total_rewards": "إجمالي المكافآت 🥚",
        "total_food_cost": "اجمالي العلف 🌽",
        "first_year_rental": "الإيجار 🏠",
        "final_profit": "الربح الصافي 💰",
        "calculation_time": "وقت الحساب ⏰",
        "summary": "ملخص النتائج ✨",
        "usd_results": "النتائج بالدولار الأمريكي 💵",
        "iqd_results": "النتائج بالدينار العراقي 💵",
        "daily_profit": "الربح اليومي 📈",
        "am": "صباحاً",
        "pm": "مساءً",
        "copy_results": "نسخ النتائج"
    },
    "English": {
        "title": "🐔 Chicken Calculator - Newyolk",
        "subtitle": "Calculate Chicken Profits and Daily Rewards",
        "language": "Language 🌍",
        "currency": "Currency 💵",
        "egg_price": "Current Egg Price 🥚",
        "feed_price": "Current Feed Price 🌽",
        "save_prices": "Save New Prices 💾",
        "calculation_type": "Calculation Type 📊",
        "chicken_profits": "Chicken Profits 🐔",
        "daily_rewards": "Daily Rewards 🥚",
        "simple_calculator": "Simple Calculator 🔢",
        "eggs_input": "Number of Eggs 🥚",
        "days_input": "Number of Days 📅",
        "food_input": "Amount of Food Needed 🌽",
        "calculate_profits": "Calculate Profits 🧮",
        "calculate_rewards": "Calculate Rewards 🥚",
        "reset": "Reset 🔄",
        "value": "Value",
        "category": "Category",
        "net_profit": "Profit Before Rent 📈",
        "total_rewards": "Total Rewards ⭐",
        "total_food_cost": "Total Feed 🌽",
        "first_year_rental": "Rental 🏠",
        "final_profit": "Final Profit 💰",
        "calculation_time": "Calculation Time ⏰",
        "summary": "Results Summary ✨",
        "usd_results": "Results in USD 💵",
        "iqd_results": "Results in IQD 💵",
        "daily_profit": "Daily Profit 📈",
        "am": "AM",
        "pm": "PM",
        "copy_results": "Copy Results"
    },
    "Română": {
        "title": "🐔 Calculator de Găini - Newyolk",
        "subtitle": "Calculează Profiturile și Recompensele Zilnice",
        "language": "Limbă 🌍",
        "currency": "Monedă 💵",
        "egg_price": "Prețul Curent al Ouălor 🥚",
        "feed_price": "Prețul Curent al Furajului 🌽",
        "save_prices": "Salvează Noile Prețuri 💾",
        "calculation_type": "Tipul Calculului 📊",
        "chicken_profits": "Profituri din Găini 🐔",
        "daily_rewards": "Recompense Zilnice 🥚",
        "simple_calculator": "Calculator Simplu 🔢",
        "eggs_input": "Număr de Ouă 🥚",
        "days_input": "Număr de Zile 📅",
        "food_input": "Cantitate de Hrană Necesară 🌽",
        "calculate_profits": "Calculează Profiturile 🧮",
        "calculate_rewards": "Calculează Recompensele 🥚",
        "reset": "Resetare 🔄",
        "value": "Valoare",
        "category": "Categorie",
        "net_profit": "Profit Înainte de Chirie 📈",
        "total_rewards": "Total Recompense ⭐",
        "total_food_cost": "Total Furaje 🌽",
        "first_year_rental": "Chirie 🏠",
        "final_profit": "Profit Final 💰",
        "calculation_time": "Ora Calculului ⏰",
        "summary": "Rezumatul Rezultatelor ✨",
        "usd_results": "Rezultate în USD 💵",
        "iqd_results": "Rezultate în IQD 💵",
        "daily_profit": "Profit Zilnic 📈",
        "am": "AM",
        "pm": "PM",
        "copy_results": "Copiază Rezultatele"
    }
}

# اختيار اللغة
language = st.selectbox("اللغة | Language | Limbă 🌍", ["العربية", "English", "Română"])

# استخدام الأعمدة لتخطيط أفضل
col1, col2 = st.columns(2)

with col1:
    currency = st.selectbox(
        texts[language]["currency"],
        ["USD", "IQD"]
    )

with col2:
    calculation_type = st.selectbox(
        texts[language]["calculation_type"],
        [texts[language]["chicken_profits"], texts[language]["daily_rewards"], texts[language]["simple_calculator"]]
    )

# دالة التحقق من المدخلات
def is_number(value):
    try:
        float(value)
        return True
    except ValueError:
        return False

# قسم تعديل الأسعار
st.subheader(texts[language]["save_prices"])
col3, col4 = st.columns(2)

with col3:
    new_egg_price = st.text_input(texts[language]["egg_price"], value="0.1155")

with col4:
    new_feed_price = st.text_input(texts[language]["feed_price"], value="0.0189")

if st.button(texts[language]["save_prices"], type="secondary"):
    if not is_number(new_egg_price) or not is_number(new_feed_price):
        st.error("يرجى إدخال أرقام صحيحة ❗️" if language == "العربية" else "Please enter valid numbers! ❗️" if language == "English" else "Vă rugăm să introduceți numere valide! ❗️")
    else:
        st.success("تم حفظ الأسعار الجديدة بنجاح! ✅" if language == "العربية" else "New prices saved successfully! ✅" if language == "English" else "Prețurile noi au fost salvate cu succes! ✅")

# تحديث الأسعار بناءً على العملة
if is_number(new_egg_price) and is_number(new_feed_price):
    if currency == "IQD":
        egg_price_display = float(new_egg_price) * 1480
        feed_price_display = float(new_feed_price) * 1480
    else:
        egg_price_display = float(new_egg_price)
        feed_price_display = float(new_feed_price)

    st.write(f"{texts[language]['egg_price']}: {format_decimal(egg_price_display)} {currency}")
    st.write(f"{texts[language]['feed_price']}: {format_decimal(feed_price_display)} {currency}")

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
    <div class="calculator-display">
        <div class="operation-display">{st.session_state.display_operation}</div>
        {st.session_state.calc_result}
    </div>
""", unsafe_allow_html=True)

# صف أزرار التحكم
col_control = st.columns(4)
with col_control[0]:
    if st.button("C", use_container_width=True):
        st.session_state.calc_result = '0'
        st.session_state.prev_number = None
        st.session_state.operation = None
        st.session_state.clear_next = False
        st.session_state.display_operation = ''
        st.rerun()
with col_control[1]:
    if st.button("⌫", use_container_width=True):
        if len(st.session_state.calc_result) > 1:
            st.session_state.calc_result = st.session_state.calc_result[:-1]
        else:
            st.session_state.calc_result = '0'
        st.rerun()
with col_control[2]:
    if st.button("±", use_container_width=True):
        current = float(st.session_state.calc_result)
        st.session_state.calc_result = str(-current)
        st.rerun()
with col_control[3]:
    if st.button("÷", use_container_width=True):
        st.session_state.prev_number = float(st.session_state.calc_result)
        st.session_state.operation = '/'
        st.session_state.display_operation = f"{st.session_state.calc_result} ÷ "
        st.session_state.clear_next = True
        st.rerun()

# صف الأرقام 7-8-9
col789 = st.columns(4)
with col789[0]:
    if st.button("7", use_container_width=True):
        if st.session_state.clear_next:
            st.session_state.calc_result = '7'
            st.session_state.clear_next = False
        else:
            if st.session_state.calc_result == '0':
                st.session_state.calc_result = '7'
            else:
                st.session_state.calc_result += '7'
        st.rerun()
with col789[1]:
    if st.button("8", use_container_width=True):
        if st.session_state.clear_next:
            st.session_state.calc_result = '8'
            st.session_state.clear_next = False
        else:
            if st.session_state.calc_result == '0':
                st.session_state.calc_result = '8'
            else:
                st.session_state.calc_result += '8'
        st.rerun()
with col789[2]:
    if st.button("9", use_container_width=True):
        if st.session_state.clear_next:
            st.session_state.calc_result = '9'
            st.session_state.clear_next = False
        else:
            if st.session_state.calc_result == '0':
                st.session_state.calc_result = '9'
            else:
                st.session_state.calc_result += '9'
        st.rerun()
with col789[3]:
    if st.button("×", use_container_width=True):
        st.session_state.prev_number = float(st.session_state.calc_result)
        st.session_state.operation = '*'
        st.session_state.display_operation = f"{st.session_state.calc_result} × "
        st.session_state.clear_next = True
        st.rerun()

# صف الأرقام 4-5-6
col456 = st.columns(4)
with col456[0]:
    if st.button("4", use_container_width=True):
        if st.session_state.clear_next:
            st.session_state.calc_result = '4'
            st.session_state.clear_next = False
        else:
            if st.session_state.calc_result == '0':
                st.session_state.calc_result = '4'
            else:
                st.session_state.calc_result += '4'
        st.rerun()
with col456[1]:
    if st.button("5", use_container_width=True):
        if st.session_state.clear_next:
            st.session_state.calc_result = '5'
            st.session_state.clear_next = False
        else:
            if st.session_state.calc_result == '0':
                st.session_state.calc_result = '5'
            else:
                st.session_state.calc_result += '5'
        st.rerun()
with col456[2]:
    if st.button("6", use_container_width=True):
        if st.session_state.clear_next:
            st.session_state.calc_result = '6'
            st.session_state.clear_next = False
        else:
            if st.session_state.calc_result == '0':
                st.session_state.calc_result = '6'
            else:
                st.session_state.calc_result += '6'
        st.rerun()
with col456[3]:
    if st.button("-", use_container_width=True):
        st.session_state.prev_number = float(st.session_state.calc_result)
        st.session_state.operation = '-'
        st.session_state.display_operation = f"{st.session_state.calc_result} - "
        st.session_state.clear_next = True
        st.rerun()

# صف الأرقام 1-2-3
col123 = st.columns(4)
with col123[0]:
    if st.button("1", use_container_width=True):
        if st.session_state.clear_next:
            st.session_state.calc_result = '1'
            st.session_state.clear_next = False
        else:
            if st.session_state.calc_result == '0':
                st.session_state.calc_result = '1'
            else:
                st.session_state.calc_result += '1'
        st.rerun()
with col123[1]:
    if st.button("2", use_container_width=True):
        if st.session_state.clear_next:
            st.session_state.calc_result = '2'
            st.session_state.clear_next = False
        else:
            if st.session_state.calc_result == '0':
                st.session_state.calc_result = '2'
            else:
                st.session_state.calc_result += '2'
        st.rerun()
with col123[2]:
    if st.button("3", use_container_width=True):
        if st.session_state.clear_next:
            st.session_state.calc_result = '3'
            st.session_state.clear_next = False
        else:
            if st.session_state.calc_result == '0':
                st.session_state.calc_result = '3'
            else:
                st.session_state.calc_result += '3'
        st.rerun()
with col123[3]:
    if st.button("+", use_container_width=True):
        st.session_state.prev_number = float(st.session_state.calc_result)
        st.session_state.operation = '+'
        st.session_state.display_operation = f"{st.session_state.calc_result} + "
        st.session_state.clear_next = True
        st.rerun()

# صف الأرقام 0 والعمليات
col_last = st.columns(4)
with col_last[0]:
    if st.button("00", use_container_width=True):
        if st.session_state.clear_next:
            st.session_state.calc_result = '0'
            st.session_state.clear_next = False
        else:
            if st.session_state.calc_result != '0':
                st.session_state.calc_result += '00'
        st.rerun()
with col_last[1]:
    if st.button("0", use_container_width=True):
        if st.session_state.clear_next:
            st.session_state.calc_result = '0'
            st.session_state.clear_next = False
        else:
            if st.session_state.calc_result != '0':
                st.session_state.calc_result += '0'
        st.rerun()
with col_last[2]:
    if st.button(".", use_container_width=True):
        if st.session_state.clear_next:
            st.session_state.calc_result = '0.'
            st.session_state.clear_next = False
        else:
            if '.' not in st.session_state.calc_result:
                st.session_state.calc_result += '.'
        st.rerun()
with col_last[3]:
    if st.button("=", use_container_width=True, type="primary"):
        try:
            if st.session_state.prev_number is not None and st.session_state.operation is not None:
                num1 = st.session_state.prev_number
                num2 = float(st.session_state.calc_result)
                operation_symbol = {'+':" + ", '-':" - ", '*':" × ", '/':" ÷ "}[st.session_state.operation]
                st.session_state.display_operation = f"{num1}{operation_symbol}{num2} ="
                
                if st.session_state.operation == '+':
                    result = num1 + num2
                elif st.session_state.operation == '-':
                    result = num1 - num2
                elif st.session_state.operation == '*':
                    result = num1 * num2
                elif st.session_state.operation == '/':
                    if num2 != 0:
                        result = num1 / num2
                    else:
                        st.error("لا يمكن القسمة على صفر!")
                        result = 0
                
                if result == int(result):
                    st.session_state.calc_result = str(int(result))
                else:
                    decimal_str = str(result).split('.')
                    if len(decimal_str) > 1:
                        decimal_places = min(len(decimal_str[1]), 8)
                        st.session_state.calc_result = f"{result:.{decimal_places}f}"
                    else:
                        st.session_state.calc_result = str(result)
                
                st.session_state.prev_number = None
                st.session_state.operation = None
                st.session_state.clear_next = True
                st.rerun()
        except Exception as e:
            st.error("حدث خطأ في العملية الحسابية!")

# إغلاق حاوية الحاسبة
st.markdown('</div>', unsafe_allow_html=True)

if calculation_type == texts[language]["chicken_profits"]:
    st.subheader(texts[language]["chicken_profits"] + " 📈")
    col5, col6 = st.columns(2)

    with col5:
        eggs = st.text_input(
            texts[language]["eggs_input"],
            value="",
            help="أدخل عدد البيض (بحد أقصى 580)" if language == "العربية" else "Enter the number of eggs (max 580)" if language == "English" else ""
        )

    with col6:
        days = st.text_input(
            texts[language]["days_input"],
            value="",
            help="أدخل عدد الأيام (بحد أقصى 730)" if language == "العربية" else "Enter the number of days (max 730)" if language == "English" else ""
        )

    if st.button(texts[language]["calculate_profits"], type="primary"):
        try:
            eggs = float(eggs) if eggs else None
            days = float(days) if days else None

            if eggs is None or days is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗️" if language == "العربية" else "Please enter all required values! ❗️" if language == "English" else "")
            elif eggs > 580:
                st.error("عدد البيض يجب ألا يتجاوز 580! ❗️" if language == "العربية" else "Number of eggs should not exceed 580! ❗️" if language == "English" else "")
            elif days > 730:
                st.error("عدد الأيام يجب ألا يتجاوز 730! ❗️" if language == "العربية" else "Number of days should not exceed 730! ❗️" if language == "English" else "")
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
║                  {texts[language]['summary']}                    ║
╠══════════════════════════════════════════════════════════════════╣
║ {texts[language]['calculation_time']}: {date_str} {time_str}
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['usd_results']}:
║ {texts[language]['egg_price']}: {format_decimal(total_egg_price)} USD
║ {texts[language]['feed_price']}: {format_decimal(total_feed_cost)} USD
║ {texts[language]['net_profit']}: {format_decimal(net_profit_before_rent)} USD
║ {texts[language]['first_year_rental']}: {format_decimal(total_rent)} USD
║ {texts[language]['final_profit']}: {format_decimal(net_profit)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['iqd_results']}:
║ {texts[language]['egg_price']}: {format_decimal(total_egg_price * 1480)} IQD
║ {texts[language]['feed_price']}: {format_decimal(total_feed_cost * 1480)} IQD
║ {texts[language]['net_profit']}: {format_decimal(net_profit_before_rent * 1480)} IQD
║ {texts[language]['first_year_rental']}: {format_decimal(total_rent * 1480)} IQD
║ {texts[language]['final_profit']}: {format_decimal(net_profit * 1480)} IQD
╚══════════════════════════════════════════════════════════════════╝"""

                # عرض النتائج
                # st.code(results_text, language="text")

                # إنشاء DataFrame للرسم البياني
                df = pd.DataFrame({
                    texts[language]["category"]: [
                        f"🥚 {texts[language]['eggs_input']}",
                        f"🌽 {texts[language]['food_input']}",
                        f"📈 {texts[language]['net_profit']}",
                        f"🏠 {texts[language]['first_year_rental']}",
                        f"💰 {texts[language]['final_profit']}"
                    ],
                    texts[language]["value"]: [
                        total_egg_price,
                        total_feed_cost,
                        net_profit_before_rent,
                        total_rent,
                        net_profit
                    ]
                })
                
                # عرض الجدول النهائي أولاً
                df = df.round(2)
                df[texts[language]["value"]] = df[texts[language]["value"]].apply(lambda x: f"{format_decimal(x)} {currency}")
                st.table(df)

                # عرض الرسم البياني
                chart_df = pd.DataFrame({
                    texts[language]["category"]: [
                        f"🥚 {texts[language]['eggs_input']}",
                        f"🌽 {texts[language]['food_input']}",
                        f"📈 {texts[language]['net_profit']}",
                        f"🏠 {texts[language]['first_year_rental']}",
                        f"💰 {texts[language]['final_profit']}"
                    ],
                    texts[language]["value"]: [
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
                st.markdown(f"### ✨ {texts[language]['summary']}")
                st.code(results_text)
                
        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗️" if language == "العربية" else "Please enter valid numbers! ❗️" if language == "English" else "")

elif calculation_type == texts[language]["daily_rewards"]:
    st.subheader(texts[language]["daily_rewards"] + " 📈")
    col7, col8 = st.columns(2)

    with col7:
        rewards = st.text_input(
            texts[language]["total_rewards"],
            value="",
            help="أدخل عدد المكافآت" if language == "العربية" else "Enter the number of rewards" if language == "English" else ""
        )

    with col8:
        food = st.text_input(
            texts[language]["total_food_cost"],
            value="",
            help="أدخل عدد الطعام المطلوب" if language == "العربية" else "Enter the amount of food needed" if language == "English" else ""
        )

    if st.button(texts[language]["calculate_rewards"], type="primary"):
        try:
            rewards = float(rewards) if rewards else None
            food = float(food) if food else None

            if rewards is None or food is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗️" if language == "العربية" else "Please enter all required values! ❗️" if language == "English" else "")
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
║ {texts[language]['calculation_time']}: {date_str} {time_str}
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['usd_results']}:
║ {texts[language]['egg_price']}: {format_decimal(rewards * float(new_egg_price))} USD
║ {texts[language]['feed_price']}: {format_decimal(food * float(new_feed_price))} USD
║ {texts[language]['daily_profit']}: {format_decimal(daily_profit)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['iqd_results']}:
║ {texts[language]['egg_price']}: {format_decimal(rewards * float(new_egg_price) * 1480)} IQD
║ {texts[language]['feed_price']}: {format_decimal(food * float(new_feed_price) * 1480)} IQD
║ {texts[language]['daily_profit']}: {format_decimal(daily_profit * 1480)} IQD
╚══════════════════════════════════════════════════════════════════╝"""

                # عرض النتائج
                # st.code(results_text, language="text")

                # إنشاء DataFrame للرسم البياني
                df = pd.DataFrame({
                    texts[language]["category"]: [
                        f"🥚 {texts[language]['total_rewards']}",
                        f"🌽 {texts[language]['total_food_cost']}",
                        f"💰 {texts[language]['daily_profit']}"
                    ],
                    texts[language]["value"]: [
                        rewards * float(new_egg_price),
                        food * float(new_feed_price),
                        daily_profit
                    ]
                })
                
                # تنسيق القيم في الجدول
                df = df.round(2)
                df[texts[language]["value"]] = df[texts[language]["value"]].apply(lambda x: f"{format_decimal(x)} {currency}")
                st.table(df)

                # عرض الرسم البياني
                chart_df = pd.DataFrame({
                    texts[language]["category"]: [
                        f"🥚 {texts[language]['total_rewards']}",
                        f"🌽 {texts[language]['total_food_cost']}",
                        f"💰 {texts[language]['daily_profit']}"
                    ],
                    texts[language]["value"]: [
                        float(str(rewards * float(new_egg_price)).replace(currency, "").strip()),
                        float(str(food * float(new_feed_price)).replace(currency, "").strip()),
                        float(str(daily_profit).replace(currency, "").strip())
                    ]
                })
                fig = create_profit_chart(chart_df, language)
                st.plotly_chart(fig, use_container_width=True)

                # عرض ملخص النتائج في النهاية
                st.markdown(f"### ✨ {texts[language]['summary']}")
                st.code(results_text)
                
        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗️" if language == "العربية" else "Please enter valid numbers! ❗️" if language == "English" else "")

elif calculation_type == texts[language]["simple_calculator"]:
    st.subheader("الحاسبة البسيطة 🔢")

# زر إعادة التعيين
if st.button(texts[language]["reset"], type="secondary"):
    st.success("تم إعادة التعيين بنجاح! ✅" if language == "العربية" else "Reset successful! ✅" if language == "English" else "")

# إضافة الأيقونات والروابط
st.markdown(
    """
    <div style="text-align: center; margin-top: 30px;">
        <a href="https://farm.newyolk.io/" target="_blank" style="text-decoration: none; margin: 0 10px;">
            <img src="https://i.ibb.co/YDKWBRf/internet.png" width="32" height="32" alt="Website">
        </a>
        <a href="https://discord.gg/RYDExGGWXh" target="_blank" style="text-decoration: none; margin: 0 10px;">
            <img src="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png" width="32" height="32" alt="Discord">
        </a>
        <a href="https://t.me/newyolkfarm" target="_blank" style="text-decoration: none; margin: 0 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" width="32" height="32" alt="Telegram">
        </a>
        <a href="https://www.facebook.com/newyolkfarming" target="_blank" style="text-decoration: none; margin: 0 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" width="32" height="32" alt="Facebook">
        </a>
        <br>
        <br>
    </div>
    <style>
        a img {
            transition: transform 0.3s ease;
            filter: brightness(1);
        }
        a img:hover {
            transform: scale(1.2);
            filter: brightness(1.2);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# إضافة نص حقوق النشر والأيقونات
st.markdown(
    """
        <br>
        <br>
    </div>
    <style>
        a img:hover {
            transform: scale(1.2);
        }
    </style>
    """,
    unsafe_allow_html=True
)

# إضافة نص حقوق النشر في نهاية الصفحة
st.markdown(
    """
    <style>
    .copyright {
        text-align: center;
        padding: 20px;
        margin-top: 50px;
        font-size: 18px;
        font-weight: bold;
        opacity: 0.9;
    }
    </style>
    <div class="copyright">By Tariq Al-Yaseen 2025-2026</div>
    """,
    unsafe_allow_html=True
)

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
