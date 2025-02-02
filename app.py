import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# تحسين الواجهة
st.set_page_config(
    page_title="Chicken Calculator - Newyolk",
    page_icon="🐔",
    layout="wide"
)

# إخفاء أزرار التحكم بالمظهر
st.markdown("""
    <style>
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# تحسين الواجهة
st.markdown("""
    <style>
        /* تحسينات عامة */
        .stApp {
            background: linear-gradient(135deg, #0a192f 0%, #112240 100%);
            color: #e2e2e2;
            position: relative;
            overflow: hidden;
        }
        
        .stApp::before {
            content: '';
            position: absolute;
            top: -50%;
            left: -50%;
            width: 200%;
            height: 200%;
            background: radial-gradient(circle, rgba(100, 255, 218, 0.1) 0%, transparent 50%);
            animation: rotate 30s linear infinite;
            z-index: 0;
        }
        
        @keyframes rotate {
            from { transform: rotate(0deg); }
            to { transform: rotate(360deg); }
        }
        
        /* جعل المحتوى فوق الخلفية المتحركة */
        .stApp > * {
            position: relative;
            z-index: 1;
        }
        
        /* تنسيق القوائم المنسدلة */
        .stSelectbox [data-baseweb="select"] {
            background-color: rgba(10, 25, 47, 0.3) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(100, 255, 218, 0.2) !important;
            border-radius: 15px !important;
        }
        
        .stSelectbox [data-baseweb="select"]:hover {
            border-color: rgba(100, 255, 218, 0.5) !important;
            box-shadow: 0 0 15px rgba(100, 255, 218, 0.2);
        }
        
        .stSelectbox [data-baseweb="popover"] {
            background-color: rgba(10, 25, 47, 0.95) !important;
            backdrop-filter: blur(10px) !important;
            border: 1px solid rgba(100, 255, 218, 0.2) !important;
            border-radius: 10px !important;
        }
        
        .stSelectbox [data-baseweb="select"] * {
            color: #e2e2e2 !important;
        }
        
        /* إضافة تأثير اللمعان */
        .stButton > button::before {
            content: '';
            position: absolute;
            top: 0;
            left: -100%;
            width: 50%;
            height: 100%;
            background: linear-gradient(
                120deg,
                transparent,
                rgba(100, 255, 218, 0.3),
                transparent
            );
            transition: 0.5s;
            transform: skewX(-15deg);
        }
        
        .stButton > button:hover::before {
            left: 100%;
        }
        
        .stButton > button {
            position: relative;
            overflow: hidden;
        }
        
        /* تحسين تأثير الضوء للعناصر */
        .stTextInput > div > div:focus-within {
            box-shadow: 0 0 20px rgba(100, 255, 218, 0.3);
        }
        
        .title {
            text-shadow: 0 0 10px rgba(100, 255, 218, 0.3);
        }
        
        /* تحسينات عامة */
        .stApp {
            background: linear-gradient(135deg, #0a192f 0%, #112240 100%);
            color: #e2e2e2;
        }
        
        /* تنسيق الأقسام */
        [data-testid="stSidebar"] {
            background-color: rgba(17, 34, 64, 0.8) !important;
            backdrop-filter: blur(10px);
        }
        
        .stSelectbox > div,
        .stTextInput > div {
            background-color: rgba(255, 255, 255, 0.05) !important;
            backdrop-filter: blur(10px);
            border: 1px solid rgba(255, 255, 255, 0.1) !important;
            border-radius: 15px !important;
            color: #e2e2e2 !important;
            transition: all 0.3s ease;
        }
        
        .stSelectbox > div:hover,
        .stTextInput > div:hover {
            border-color: rgba(74, 144, 226, 0.5) !important;
            box-shadow: 0 0 15px rgba(74, 144, 226, 0.2);
        }
        
        /* تنسيق العنوان والعنوان الفرعي */
        .title {
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            padding: 25px;
            margin-bottom: 10px;
            background: linear-gradient(120deg, #64ffda, #00bfa5);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
        }
        
        .subtitle {
            font-size: 28px;
            text-align: center;
            margin-bottom: 35px;
            color: #8892b0;
            font-weight: 300;
        }
        
        /* تنسيق الأزرار */
        .stButton > button {
            background: linear-gradient(135deg, #64ffda 0%, #00bfa5 100%);
            color: #0a192f;
            border: none;
            padding: 12px 30px;
            border-radius: 15px;
            font-size: 18px;
            font-weight: 600;
            box-shadow: 0 4px 15px rgba(100, 255, 218, 0.3);
            transition: all 0.3s ease;
        }
        
        .stButton > button:hover {
            transform: translateY(-2px);
            box-shadow: 0 6px 20px rgba(100, 255, 218, 0.4);
        }
        
        /* تنسيق النتائج */
        pre {
            background: rgba(10, 25, 47, 0.7);
            border: 1px solid rgba(100, 255, 218, 0.2);
            border-radius: 15px;
            padding: 20px;
            color: #e2e2e2;
            font-family: 'Consolas', monospace;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(10px);
        }
        
        /* تنسيق العناوين الفرعية */
        h3 {
            color: #64ffda;
            font-size: 24px;
            font-weight: 500;
            margin: 25px 0 15px 0;
            padding-bottom: 8px;
            border-bottom: 2px solid rgba(100, 255, 218, 0.3);
        }
        
        /* تنسيق الجداول */
        .stTable {
            background: rgba(10, 25, 47, 0.7);
            border-radius: 15px;
            overflow: hidden;
            backdrop-filter: blur(10px);
        }
        
        .stTable th {
            background: rgba(100, 255, 218, 0.1);
            color: #64ffda;
            font-weight: 500;
        }
        
        .stTable td {
            border-color: rgba(255, 255, 255, 0.05);
            color: #e2e2e2;
        }
        
        /* تنسيق الإشعارات */
        .stAlert {
            background: rgba(10, 25, 47, 0.7) !important;
            border: 1px solid rgba(100, 255, 218, 0.2) !important;
            border-radius: 15px !important;
            color: #e2e2e2 !important;
            backdrop-filter: blur(10px);
        }
        
        /* تحسين التوافق مع الأجهزة المحمولة */
        @media (max-width: 768px) {
            .title {
                font-size: 32px;
                padding: 15px;
            }
            
            .subtitle {
                font-size: 22px;
                margin-bottom: 25px;
            }
        }
        
        /* تنسيق الرسوم البيانية */
        .js-plotly-plot {
            background: rgba(10, 25, 47, 0.7) !important;
            border-radius: 15px !important;
            padding: 15px !important;
            box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
            backdrop-filter: blur(10px);
        }
        
        /* تنسيق حقوق النشر */
        .copyright {
            text-align: center;
            padding: 20px;
            color: #8892b0;
            font-size: 14px;
            margin-top: 40px;
        }
    </style>
""", unsafe_allow_html=True)

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تعريف النصوص بجميع اللغات
texts = {
    "العربية": {
        "title": "🐔 حاسبة الدجاج - نيويولك",
        "subtitle": "حساب أرباح الدجاج والمكافآت اليومية",
        "language": "اللغة 🌍",
        "currency": "العملة 💵",
        "egg_price": "قيمة البيض الكلية 🥚",
        "feed_price": "قيمة العلف الكلية 🌽",
        "save_prices": "حفظ الأسعار الجديدة 💾",
        "calculation_type": "نوع الحساب 📊",
        "chicken_profits": "أرباح الدجاج 🐔",
        "daily_rewards": "المكافآت اليومية ✨",
        "eggs_input": "عدد البيض 🥚",
        "days_input": "عدد الأيام 📅",
        "food_input": "عدد الطعام المطلوب 🌽",
        "calculate_profits": "حساب الأرباح 🧮",
        "calculate_rewards": "حساب المكافآت ✨",
        "reset": "إعادة تعيين 🔄",
        "value": "القيمة",
        "category": "الفئة",
        "net_profit": "الربح قبل حساب الايجار 📈",
        "total_rewards": "إجمالي المكافآت ⭐",
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
        "egg_price": "Total Egg Value 🥚",
        "feed_price": "Total Feed Value 🌽",
        "save_prices": "Save New Prices 💾",
        "calculation_type": "Calculation Type 📊",
        "chicken_profits": "Chicken Profits 🐔",
        "daily_rewards": "Daily Rewards ✨",
        "eggs_input": "Number of Eggs 🥚",
        "days_input": "Number of Days 📅",
        "food_input": "Amount of Food Needed 🌽",
        "calculate_profits": "Calculate Profits 🧮",
        "calculate_rewards": "Calculate Rewards ✨",
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
        "egg_price": "Valoarea Totală a Ouălor 🥚",
        "feed_price": "Valoarea Totală a Furajului 🌽",
        "save_prices": "Salvează Noile Prețuri 💾",
        "calculation_type": "Tipul Calculului 📊",
        "chicken_profits": "Profituri din Găini 🐔",
        "daily_rewards": "Recompense Zilnice ✨",
        "eggs_input": "Număr de Ouă 🥚",
        "days_input": "Număr de Zile 📅",
        "food_input": "Cantitate de Hrană Necesară 🌽",
        "calculate_profits": "Calculează Profiturile 🧮",
        "calculate_rewards": "Calculează Recompensele ✨",
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
    <div class="title">{texts[language]["title"]}</div>
    <div class="subtitle">{texts[language]["subtitle"]}</div>
    """,
    unsafe_allow_html=True
)

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
        [texts[language]["chicken_profits"], texts[language]["daily_rewards"]]
    )

# دالة التحقق من المدخلات
def is_number(value):
    if not value:  # التحقق من القيم الفارغة
        return False
    try:
        # إزالة الفواصل والمسافات
        cleaned_value = str(value).replace(',', '').replace(' ', '')
        float(cleaned_value)
        return True
    except (ValueError, TypeError):
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

# دالة إنشاء الرسم البياني
def create_profit_chart(df, language):
    fig = px.line(df, x='category', y='value',
                  title=texts[language]["summary"],
                  labels={'value': texts[language]["value"],
                         'category': texts[language]["category"]})
    
    # تحديث مظهر الرسم البياني
    fig.update_layout(
        plot_bgcolor='rgba(10, 25, 47, 0.7)',
        paper_bgcolor='rgba(10, 25, 47, 0)',
        font=dict(color='#e2e2e2', family='Arial, sans-serif'),
        title=dict(
            font=dict(size=24, color='#64ffda'),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.2)',
            tickfont=dict(size=12),
            title_font=dict(color='#8892b0')
        ),
        yaxis=dict(
            gridcolor='rgba(255, 255, 255, 0.1)',
            linecolor='rgba(255, 255, 255, 0.2)',
            tickfont=dict(size=12),
            title_font=dict(color='#8892b0')
        ),
        showlegend=False,
        hovermode='x unified',
        margin=dict(t=80, b=40, l=40, r=40)
    )
    
    # تحديث خط الرسم البياني
    fig.update_traces(
        line=dict(color='#64ffda', width=3),
        mode='lines+markers',
        marker=dict(
            size=8,
            color='#00bfa5',
            line=dict(color='#64ffda', width=2)
        ),
        hovertemplate='%{y:,.2f}<extra></extra>'
    )
    
    return fig

if calculation_type == texts[language]["chicken_profits"]:
    st.subheader(texts[language]["chicken_profits"] + " 📈")
    col5, col6 = st.columns(2)

    with col5:
        eggs = st.text_input(
            texts[language]["eggs_input"],
            value="30",
            help="أدخل عدد البيض (بحد أقصى 580)" if language == "العربية" else "Enter the number of eggs (max 580)" if language == "English" else ""
        )

    with col6:
        days = st.text_input(
            texts[language]["days_input"],
            value="30",
            help="أدخل عدد الأيام (بحد أقصى 730)" if language == "العربية" else "Enter the number of days (max 730)" if language == "English" else ""
        )

    if st.button(texts[language]["calculate_profits"]):
        if not is_number(eggs) or not is_number(days) or not is_number(new_egg_price) or not is_number(new_feed_price):
            st.error("يرجى إدخال أرقام صحيحة ❗️" if language == "العربية" else "Please enter valid numbers! ❗️" if language == "English" else "Vă rugăm să introduceți numere valide! ❗️")
        else:
            # تحويل المدخلات إلى أرقام
            eggs = float(str(eggs).replace(',', '').replace(' ', ''))
            days = float(str(days).replace(',', '').replace(' ', ''))
            new_egg_price = float(str(new_egg_price).replace(',', '').replace(' ', ''))
            new_feed_price = float(str(new_feed_price).replace(',', '').replace(' ', ''))

            # حساب الأرباح
            total_egg_price = eggs * new_egg_price  # ضرب عدد البيض في سعر البيض الحالي
            total_feed_cost = (days * 2) * new_feed_price  # ضرب عدد الأيام في 2 ثم في سعر العلف الحالي
            
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
            
            # تنسيق القيم في الجدول
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

    if st.button(texts[language]["calculate_rewards"]):
        if not is_number(rewards) or not is_number(food) or not is_number(new_egg_price) or not is_number(new_feed_price):
            st.error("يرجى إدخال أرقام صحيحة ❗️" if language == "العربية" else "Please enter valid numbers! ❗️" if language == "English" else "Vă rugăm să introduceți numere valide! ❗️")
        else:
            # تحويل المدخلات إلى أرقام
            rewards = float(str(rewards).replace(',', '').replace(' ', ''))
            food = float(str(food).replace(',', '').replace(' ', ''))
            new_egg_price = float(str(new_egg_price).replace(',', '').replace(' ', ''))
            new_feed_price = float(str(new_feed_price).replace(',', '').replace(' ', ''))

            # حساب الربح اليومي
            daily_profit = rewards * new_egg_price - food * new_feed_price

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
║ {texts[language]['egg_price']}: {format_decimal(rewards * new_egg_price)} USD
║ {texts[language]['feed_price']}: {format_decimal(food * new_feed_price)} USD
║ {texts[language]['daily_profit']}: {format_decimal(daily_profit)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['iqd_results']}:
║ {texts[language]['egg_price']}: {format_decimal(rewards * new_egg_price * 1480)} IQD
║ {texts[language]['feed_price']}: {format_decimal(food * new_feed_price * 1480)} IQD
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
                    rewards * new_egg_price,
                    food * new_feed_price,
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
                    float(str(rewards * new_egg_price).replace(currency, "").strip()),
                    float(str(food * new_feed_price).replace(currency, "").strip()),
                    float(str(daily_profit).replace(currency, "").strip())
                ]
            })
            fig = create_profit_chart(chart_df, language)
            st.plotly_chart(fig, use_container_width=True)

            # عرض ملخص النتائج في النهاية
            st.markdown(f"### ✨ {texts[language]['summary']}")
            st.code(results_text)
                
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
        color: #8892b0;
        font-size: 14px;
        margin-top: 40px;
    }
    </style>
    <div class="copyright">By Tariq Al-Yaseen © 2025-2026</div>
    """,
    unsafe_allow_html=True
)
