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

# تنسيق الأرقام العشرية
def format_number(number):
    try:
        return "{:,.2f}".format(float(number))
    except:
        return str(number)

# تعريف النصوص بجميع اللغات
texts = {
    "العربية": {
        "title": "🐔 حاسبة الدجاج - نيويولك",
        "subtitle": "حساب أرباح الدجاج والمكافآت اليومية",
        "language": "اللغة 🌐",
        "currency": "العملة 💰",
        "egg_price": "سعر البيض الحالي🥚",
        "feed_price": "سعر العلف الحالي🌽",
        "save_prices": "حفظ الأسعار الجديدة 💾",
        "calculation_type": "نوع الحساب 📊",
        "chicken_profits": "أرباح الدجاج",
        "daily_rewards": "المكافآت اليومية وأرباح العلف",
        "eggs_input": "عدد البيض 🥚",
        "days_input": "عدد الأيام 📅",
        "calculate_profits": "حساب أرباح الدجاج 🧮",
        "food_input": "كمية العلف المطلوبة 🌽",
        "calculate_rewards": "حساب المكافآت وأرباح العلف 🧮",
        "reset": "إعادة تعيين 🔄",
        "copyright": "By Tariq Al-Yaseen ©️ 2025-2026",
        "value": "القيمة",
        "category": "الفئة",
        "net_profit": "صافي الربح 💰",
        "total_rewards": "إجمالي المكافآت 🎁",
        "total_food_cost": "إجمالي تكلفة العلف 🌽",
        "first_year_rental": "إيجار السنة الأولى 🏠",
        "second_year_rental": "إيجار السنة الثانية 🏠",
        "calculation_time": "وقت الحساب ⏰",
        "am": "صباحاً",
        "pm": "مساءً",
        "summary": "ملخص النتائج",
        "copy_results": "نسخ النتائج",
        "daily_profit": "الربح اليومي",
        "usd_results": "بالدولار الأمريكي",
        "iqd_results": "بالدينار العراقي"
    },
    "English": {
        "title": "🐔 Chicken Calculator - Newyolk",
        "subtitle": "Calculate Chicken Profits and Daily Rewards",
        "language": "Language 🌐",
        "currency": "Currency 💰",
        "egg_price": "Egg Price 🥚",
        "feed_price": "Feed Price 🌽",
        "save_prices": "Save New Prices 💾",
        "calculation_type": "Calculation Type 📊",
        "chicken_profits": "Chicken Profits",
        "daily_rewards": "Daily Rewards and Feed Profits",
        "eggs_input": "Number of Eggs 🥚",
        "days_input": "Number of Days 📅",
        "calculate_profits": "Calculate Chicken Profits 🧮",
        "food_input": "Required Feed Amount 🌽",
        "calculate_rewards": "Calculate Rewards and Feed Profits 🧮",
        "reset": "Reset 🔄",
        "copyright": "By Tariq Al-Yaseen ©️ 2025-2026",
        "value": "Value",
        "category": "Category",
        "net_profit": "Net Profit 💰",
        "total_rewards": "Total Rewards 🎁",
        "total_food_cost": "Total Food Cost 🌽",
        "first_year_rental": "First Year Rental 🏠",
        "second_year_rental": "Second Year Rental 🏠",
        "calculation_time": "Calculation Time ⏰",
        "am": "AM",
        "pm": "PM",
        "summary": "Results Summary",
        "copy_results": "Copy Results",
        "daily_profit": "Daily Profit",
        "usd_results": "In USD",
        "iqd_results": "In IQD"
    },
    "Română": {
        "title": "🐔 Calculator de Găini - Newyolk",
        "subtitle": "Calculează Profiturile și Recompensele Zilnice",
        "language": "Limbă 🌐",
        "currency": "Monedă 💰",
        "egg_price": "Prețul Ouălor 🥚",
        "feed_price": "Prețul Furajului 🌽",
        "save_prices": "Salvează Noile Prețuri 💾",
        "calculation_type": "Tipul Calculului 📊",
        "chicken_profits": "Profituri din Găini",
        "daily_rewards": "Recompense Zilnice și Profituri din Mâncare",
        "eggs_input": "Numărul de Ouă 🥚",
        "days_input": "Numărul de Zile 📅",
        "calculate_profits": "Calculează Profiturile din Găini 🧮",
        "food_input": "Cantitatea de Mâncare Necesară 🌽",
        "calculate_rewards": "Calculează Recompensele și Profiturile din Mâncare 🧮",
        "reset": "Resetează 🔄",
        "copyright": "By Tariq Al-Yaseen ©️ 2025-2026",
        "value": "Valoare",
        "category": "Categorie",
        "net_profit": "Profit Net 💰",
        "total_rewards": "Total Recompense 🎁",
        "total_food_cost": "Cost Total Furaje 🌽",
        "first_year_rental": "Chirie Primul An 🏠",
        "second_year_rental": "Chirie Al Doilea An 🏠",
        "calculation_time": "Ora Calculului ⏰",
        "am": "AM",
        "pm": "PM",
        "summary": "Rezumatul Rezultatelor",
        "copy_results": "Copiază Rezultatele",
        "daily_profit": "Profit Zilnic",
        "usd_results": "În USD",
        "iqd_results": "În IQD"
    }
}

# اختيار اللغة
language = st.selectbox("اللغة | Language | Limbă 🌐", ["العربية", "English", "Română"])

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
    try:
        float(value)
        return True
    except ValueError:
        return False

if calculation_type == texts[language]["chicken_profits"]:
    st.subheader(texts[language]["chicken_profits"] + " 📈")
    col5, col6 = st.columns(2)

    with col5:
        eggs_input = st.text_input(texts[language]["eggs_input"])
        if eggs_input and not is_number(eggs_input):
            st.error("الرجاء إدخال أرقام فقط")
            eggs_input = "0"
        eggs = float(eggs_input) if eggs_input else 0

    with col6:
        days_input = st.text_input(texts[language]["days_input"])
        if days_input and not is_number(days_input):
            st.error("الرجاء إدخال أرقام فقط")
            days_input = "0"
        days = float(days_input) if days_input else 0

    if st.button(texts[language]["calculate_profits"] + " 🧮"):
        if eggs > 0 and days > 0:
            # حساب الأرباح
            egg_price = 0.25 if currency == "USD" else 370
            feed_price = 0.50 if currency == "USD" else 740
            total_egg_price = eggs * egg_price
            total_feed_cost = (eggs * 0.12) * feed_price
            
            # حساب الإيجار
            daily_rent = 6 if currency == "USD" else 8880  # 6 دولار يومياً
            total_rent = daily_rent * days if eggs >= 260 else 0
            
            net_profit = total_egg_price - total_feed_cost - total_rent

            # إنشاء DataFrame للنتائج
            df = pd.DataFrame({
                texts[language]["category"]: [
                    f"🥚 {texts[language]['eggs_input']}",
                    f"🌽 {texts[language]['food_input']}",
                    f"📊 {texts[language]['net_profit']}",
                    f"🏠 {texts[language]['first_year_rental']}",
                    f"💰 {texts[language]['net_profit']}"
                ],
                texts[language]["value"]: [
                    format_number(eggs),
                    format_number(eggs * 0.12),
                    format_number(total_egg_price - total_feed_cost),
                    format_number(total_rent),
                    format_number(net_profit)
                ]
            })
            
            # عرض الجدول النهائي أولاً
            df = df.round(2)
            df[texts[language]["value"]] = df[texts[language]["value"]].apply(lambda x: f"{x} {currency}")
            st.table(df)

            # عرض الرسم البياني
            chart_df = pd.DataFrame({
                texts[language]["category"]: [
                    f"🥚 {texts[language]['eggs_input']}",
                    f"🌽 {texts[language]['food_input']}",
                    f"📊 {texts[language]['net_profit']}",
                    f"🏠 {texts[language]['first_year_rental']}",
                    f"💰 {texts[language]['net_profit']}"
                ],
                texts[language]["value"]: [
                    float(eggs),
                    float(eggs * 0.12),
                    float(total_egg_price - total_feed_cost),
                    float(total_rent),
                    float(net_profit)
                ]
            })
            fig = create_profit_chart(chart_df, language)
            st.plotly_chart(fig, use_container_width=True)

            # عرض ملخص النتائج في النهاية
            st.markdown(f"### 📊 {texts[language]['summary']}")
            st.code(f"""
╔══════════════════════════════════════════════════════════════════╗
║                  {texts[language]['summary']}                    ║
╠══════════════════════════════════════════════════════════════════╣
║ {texts[language]['calculation_time']}: {datetime.now().strftime("%Y-%m-%d %I:%M %p")}
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['usd_results']}:
║ {texts[language]['egg_price']}: {format_number(total_egg_price)} USD
║ {texts[language]['feed_price']}: {format_number(total_feed_cost)} USD
║ {texts[language]['net_profit']}: {format_number(net_profit)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['iqd_results']}:
║ {texts[language]['egg_price']}: {format_number(total_egg_price * 1480)} IQD
║ {texts[language]['feed_price']}: {format_number(total_feed_cost * 1480)} IQD
║ {texts[language]['net_profit']}: {format_number(net_profit * 1480)} IQD
╚══════════════════════════════════════════════════════════════════╝""")

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
║ {texts[language]['egg_price']}: {format_number(rewards * float(new_egg_price))} USD
║ {texts[language]['feed_price']}: {format_number(food * float(new_feed_price))} USD
║ {texts[language]['daily_profit']}: {format_number(daily_profit)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['iqd_results']}:
║ {texts[language]['egg_price']}: {format_number(rewards * float(new_egg_price) * 1480)} IQD
║ {texts[language]['feed_price']}: {format_number(food * float(new_feed_price) * 1480)} IQD
║ {texts[language]['daily_profit']}: {format_number(daily_profit * 1480)} IQD
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
                        format_number(rewards * float(new_egg_price)),
                        format_number(food * float(new_feed_price)),
                        format_number(daily_profit)
                    ]
                })
                
                # تنسيق القيم في الجدول
                df = df.round(2)
                df[texts[language]["value"]] = df[texts[language]["value"]].apply(lambda x: f"{x} {currency}")
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
                st.markdown(f"### 📊 {texts[language]['summary']}")
                st.code(results_text)
                
        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗️" if language == "العربية" else "Please enter valid numbers! ❗️" if language == "English" else "")

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
