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
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تعريف النصوص بجميع اللغات
texts = {
    "العربية": {
        "title": "🐔 حاسبة الدجاج - نيويولك",
        "subtitle": "حساب أرباح الدجاج والمكافآت اليومية",
        "language": "اللغة 🌐",
        "currency": "العملة 💰",
        "egg_price": "سعر البيض 🥚",
        "feed_price": "سعر العلف 🌾",
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
        "total_food_cost": "إجمالي تكلفة العلف 🌾",
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
        "feed_price": "Feed Price 🌾",
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
        "total_food_cost": "Total Food Cost 🌾",
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
        "feed_price": "Prețul Furajului 🌾",
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
        "total_food_cost": "Cost Total Furaje 🌾",
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

# تعيين اللغة الافتراضية
if 'language' not in st.session_state:
    st.session_state.language = "العربية"

# اختيار اللغة
language = st.selectbox("اللغة | Language | Limbă 🌐", ["العربية", "English", "Română"])
st.session_state.language = language

# عرض الواجهة المناسبة حسب اللغة المختارة
if language == "العربية":
    st.markdown("""
        <style>
            .stApp {
                direction: rtl;
            }
            .title {
                font-size: 36px;
                font-weight: bold;
                text-align: center;
                padding: 20px;
            }
            .subtitle {
                font-size: 24px;
                text-align: center;
                margin-bottom: 30px;
            }
            .stButton {
                direction: rtl;
                text-align: right;
            }
            .stSelectbox, .stTextInput {
                direction: rtl;
                text-align: right;
            }
            [data-testid="stMarkdownContainer"] {
                direction: rtl;
                text-align: right;
            }
        </style>
        <div class="title">🐔 حاسبة الدجاج - نيويولك</div>
        <div class="subtitle">حساب أرباح الدجاج والمكافآت اليومية</div>
    """, unsafe_allow_html=True)

def show_english_interface():
    st.markdown("""
        <style>
            .stApp {
                direction: ltr;
            }
            .title {
                font-size: 36px;
                font-weight: bold;
                text-align: center;
                padding: 20px;
            }
            .subtitle {
                font-size: 24px;
                text-align: center;
                margin-bottom: 30px;
            }
            .stButton {
                direction: ltr;
                text-align: left;
            }
            .stSelectbox, .stTextInput {
                direction: ltr;
                text-align: left;
            }
            [data-testid="stMarkdownContainer"] {
                direction: ltr;
                text-align: left;
            }
        </style>
        <div class="title">🐔 Chicken Calculator - Newyolk</div>
        <div class="subtitle">Calculate Chicken Profits and Daily Rewards</div>
    """, unsafe_allow_html=True)

def show_romanian_interface():
    st.markdown("""
        <style>
            .stApp {
                direction: ltr;
            }
            .title {
                font-size: 36px;
                font-weight: bold;
                text-align: center;
                padding: 20px;
            }
            .subtitle {
                font-size: 24px;
                text-align: center;
                margin-bottom: 30px;
            }
            .stButton {
                direction: ltr;
                text-align: left;
            }
            .stSelectbox, .stTextInput {
                direction: ltr;
                text-align: left;
            }
            [data-testid="stMarkdownContainer"] {
                direction: ltr;
                text-align: left;
            }
        </style>
        <div class="title">🐔 Calculator de Găini - Newyolk</div>
        <div class="subtitle">Calculează Profiturile și Recompensele Zilnice</div>
    """, unsafe_allow_html=True)

# عرض الواجهة المناسبة حسب اللغة المختارة
if language == "العربية":
    show_arabic_interface()
elif language == "English":
    show_english_interface()
else:
    show_romanian_interface()

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

# قسم تعديل الأسعار
st.subheader(texts[language]["save_prices"])
col3, col4 = st.columns(2)

with col3:
    new_egg_price = st.text_input(texts[language]["egg_price"], value="0.1155")

with col4:
    new_feed_price = st.text_input(texts[language]["feed_price"], value="0.0189")

if st.button(texts[language]["save_prices"], type="secondary"):
    try:
        new_egg_price = float(new_egg_price)
        new_feed_price = float(new_feed_price)
        st.success("تم حفظ الأسعار الجديدة بنجاح! ✅" if language == "العربية" else "New prices saved successfully! ✅" if language == "English" else "")
    except ValueError:
        st.error("يرجى إدخال أرقام صحيحة! ❗️" if language == "العربية" else "Please enter valid numbers! ❗️" if language == "English" else "")

# تحديث الأسعار بناءً على العملة
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
    # تخصيص الألوان
    colors = {
        'عدد البيض 🥚': '#4CAF50',
        'عدد الطعام المطلوب 🌾': '#FF9800',
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
                # حساب الإيجار
                if days > 365:  # السنة الثانية
                    rent_cost = 6  # دفع الإيجار للسنة الثانية
                else:
                    rent_cost = 0  # لا يوجد إيجار في السنة الأولى

                # حساب النتائج
                total_egg_price_usd = eggs * float(new_egg_price)
                total_feed_cost_usd = (days * 2) * float(new_feed_price)  # تصحيح حساب تكلفة العلف
                net_profit_before_rent_usd = total_egg_price_usd - total_feed_cost_usd
                rent_cost_usd = rent_cost
                net_profit_usd = net_profit_before_rent_usd - rent_cost_usd

                # تحويل العملة
                if currency == "IQD":
                    total_egg_price = total_egg_price_usd * 1480
                    total_feed_cost = total_feed_cost_usd * 1480
                    net_profit_before_rent = net_profit_before_rent_usd * 1480
                    rent_cost = rent_cost_usd * 1480
                    net_profit = net_profit_usd * 1480
                else:
                    total_egg_price, total_feed_cost, net_profit_before_rent, rent_cost, net_profit = (
                        total_egg_price_usd, total_feed_cost_usd, net_profit_before_rent_usd, rent_cost_usd, net_profit_usd
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
║ {texts[language]['net_profit']}: {format_decimal(net_profit)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['iqd_results']}:
║ {texts[language]['egg_price']}: {format_decimal(total_egg_price * 1480)} IQD
║ {texts[language]['feed_price']}: {format_decimal(total_feed_cost * 1480)} IQD
║ {texts[language]['net_profit']}: {format_decimal(net_profit * 1480)} IQD
╚══════════════════════════════════════════════════════════════════╝"""

                # عرض النتائج
                # st.code(results_text, language="text")

                # إنشاء DataFrame للرسم البياني
                df = pd.DataFrame({
                    texts[language]["category"]: [
                        f"🥚 {texts[language]['eggs_input']}",
                        f"🌾 {texts[language]['food_input']}",
                        f"📊 {texts[language]['net_profit']}",
                        f"🏠 {texts[language]['first_year_rental']}",
                        f"💰 {texts[language]['net_profit']}"
                    ],
                    texts[language]["value"]: [
                        total_egg_price,
                        total_feed_cost,
                        net_profit_before_rent,
                        rent_cost,
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
                        f"🌾 {texts[language]['food_input']}",
                        f"📊 {texts[language]['net_profit']}",
                        f"🏠 {texts[language]['first_year_rental']}",
                        f"💰 {texts[language]['net_profit']}"
                    ],
                    texts[language]["value"]: [
                        float(str(total_egg_price).replace(currency, "").strip()),
                        float(str(total_feed_cost).replace(currency, "").strip()),
                        float(str(net_profit_before_rent).replace(currency, "").strip()),
                        float(str(rent_cost).replace(currency, "").strip()),
                        float(str(net_profit).replace(currency, "").strip())
                    ]
                })
                fig = create_profit_chart(chart_df, language)
                st.plotly_chart(fig, use_container_width=True)

                # عرض ملخص النتائج في النهاية
                st.markdown(f"### 📊 {texts[language]['summary']}")
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
                        f"🌾 {texts[language]['total_food_cost']}",
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
                        f"🌾 {texts[language]['total_food_cost']}",
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
    <div class="copyright">By Tariq Al-Yaseen 🐔 2025-2026</div>
    """,
    unsafe_allow_html=True
)
