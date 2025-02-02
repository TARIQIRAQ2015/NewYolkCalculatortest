import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta

# تحسين الواجهة
st.set_page_config(
    page_title="Newyolk - Premium Chicken Calculator",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'Get Help': None,
        'Report a bug': None,
        'About': 'Newyolk Premium Calculator 2025-2026'
    }
)

# تحسين الواجهة
st.markdown("""
    <style>
        /* تعريف المتغيرات العامة */
        :root {
            --primary-color: #2E1F4A;
            --secondary-color: #4A266A;
            --accent-color: #8A4FFF;
            --text-color: #E9E9FF;
            --background-color: #1A1A2E;
            --card-bg: #2D2D44;
            --success-color: #4CAF50;
            --warning-color: #FF9800;
            --gradient-1: linear-gradient(135deg, #2E1F4A 0%, #4A266A 100%);
            --gradient-2: linear-gradient(135deg, #8A4FFF 0%, #4A266A 100%);
            --box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        }

        /* إخفاء عناصر Streamlit الافتراضية */
        #MainMenu {visibility: hidden;}
        footer {visibility: hidden;}
        header {visibility: hidden;}

        /* تنسيق الصفحة الرئيسية */
        .stApp {
            background: var(--background-color);
            color: var(--text-color);
        }

        /* تنسيق العناوين */
        .title {
            font-size: 42px;
            font-weight: bold;
            text-align: center;
            padding: 30px;
            background: var(--gradient-1);
            border-radius: 20px;
            margin-bottom: 20px;
            box-shadow: var(--box-shadow);
            text-transform: uppercase;
            letter-spacing: 2px;
            color: var(--text-color);
        }

        .subtitle {
            font-size: 28px;
            text-align: center;
            margin-bottom: 40px;
            color: var(--accent-color);
            font-weight: 500;
        }

        /* تنسيق الأزرار */
        .stButton button {
            background: var(--gradient-2) !important;
            color: white !important;
            font-size: 18px !important;
            padding: 15px 30px !important;
            border-radius: 15px !important;
            border: none !important;
            box-shadow: var(--box-shadow) !important;
            transition: all 0.3s ease !important;
        }

        .stButton button:hover {
            transform: translateY(-2px) !important;
            box-shadow: 0 12px 40px 0 rgba(31, 38, 135, 0.5) !important;
        }

        /* تنسيق مربعات الإدخال */
        .stTextInput input, .stSelectbox select {
            background: var(--card-bg) !important;
            color: var(--text-color) !important;
            border-radius: 10px !important;
            border: 1px solid var(--accent-color) !important;
            padding: 12px !important;
            font-size: 16px !important;
        }

        .stTextInput input:focus, .stSelectbox select:focus {
            border-color: var(--accent-color) !important;
            box-shadow: 0 0 0 2px rgba(138, 79, 255, 0.3) !important;
        }

        /* تنسيق الجداول */
        .stTable {
            background: var(--card-bg) !important;
            border-radius: 15px !important;
            overflow: hidden !important;
            box-shadow: var(--box-shadow) !important;
        }

        .stTable th {
            background: var(--primary-color) !important;
            color: var(--text-color) !important;
            padding: 15px !important;
        }

        .stTable td {
            color: var(--text-color) !important;
            padding: 12px !important;
        }

        /* تنسيق البطاقات */
        div[data-testid="stVerticalBlock"] > div {
            background: var(--card-bg);
            padding: 20px;
            border-radius: 15px;
            margin-bottom: 20px;
            box-shadow: var(--box-shadow);
            border: 1px solid rgba(138, 79, 255, 0.1);
        }

        /* تنسيق النصوص */
        p, div {
            color: var(--text-color);
        }

        /* تنسيق الرسوم البيانية */
        .js-plotly-plot {
            background: var(--card-bg) !important;
            border-radius: 15px !important;
            padding: 15px !important;
            box-shadow: var(--box-shadow) !important;
        }

        /* تنسيق ملخص النتائج */
        pre {
            background: var(--gradient-1) !important;
            border-radius: 15px !important;
            padding: 20px !important;
            color: var(--text-color) !important;
            font-family: 'Courier New', monospace !important;
            box-shadow: var(--box-shadow) !important;
            border: 1px solid var(--accent-color) !important;
        }

        /* تنسيق التوقيع */
        .copyright {
            text-align: center;
            padding: 20px;
            color: var(--text-color);
            font-size: 14px;
            background: var(--gradient-1);
            border-radius: 10px;
            margin-top: 30px;
            box-shadow: var(--box-shadow);
        }

        /* تحسين التجاوب مع الأجهزة المحمولة */
        @media (max-width: 768px) {
            .title {
                font-size: 32px;
                padding: 20px;
            }
            .subtitle {
                font-size: 22px;
            }
            .stButton button {
                padding: 12px 24px !important;
                font-size: 16px !important;
            }
        }
    </style>
""", unsafe_allow_html=True)

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تعريف النصوص بجميع اللغات
texts = {
    "العربية": {
        "title": "",
        "subtitle": "",
        "language": "",
        "currency": "",
        "egg_price": "",
        "feed_price": "",
        "save_prices": "",
        "calculation_type": "",
        "chicken_profits": "",
        "daily_rewards": "",
        "eggs_input": "",
        "days_input": "",
        "food_input": "",
        "calculate_profits": "",
        "calculate_rewards": "",
        "reset": "",
        "value": "",
        "category": "",
        "net_profit": "",
        "total_rewards": "",
        "total_food_cost": "",
        "first_year_rental": "",
        "final_profit": "",
        "calculation_time": "",
        "summary": "",
        "usd_results": "",
        "iqd_results": "",
        "daily_profit": "",
        "am": "",
        "pm": "",
        "copy_results": ""
    },
    "English": {
        "title": "",
        "subtitle": "",
        "language": "",
        "currency": "",
        "egg_price": "",
        "feed_price": "",
        "save_prices": "",
        "calculation_type": "",
        "chicken_profits": "",
        "daily_rewards": "",
        "eggs_input": "",
        "days_input": "",
        "food_input": "",
        "calculate_profits": "",
        "calculate_rewards": "",
        "reset": "",
        "value": "",
        "category": "",
        "net_profit": "",
        "total_rewards": "",
        "total_food_cost": "",
        "first_year_rental": "",
        "final_profit": "",
        "calculation_time": "",
        "summary": "",
        "usd_results": "",
        "iqd_results": "",
        "daily_profit": "",
        "am": "",
        "pm": "",
        "copy_results": ""
    },
    "Română": {
        "title": "",
        "subtitle": "",
        "language": "",
        "currency": "",
        "egg_price": "",
        "feed_price": "",
        "save_prices": "",
        "calculation_type": "",
        "chicken_profits": "",
        "daily_rewards": "",
        "eggs_input": "",
        "days_input": "",
        "food_input": "",
        "calculate_profits": "",
        "calculate_rewards": "",
        "reset": "",
        "value": "",
        "category": "",
        "net_profit": "",
        "total_rewards": "",
        "total_food_cost": "",
        "first_year_rental": "",
        "final_profit": "",
        "calculation_time": "",
        "summary": "",
        "usd_results": "",
        "iqd_results": "",
        "daily_profit": "",
        "am": "",
        "pm": "",
        "copy_results": ""
    }
}

# اختيار اللغة
language = st.selectbox("", ["", "", ""])

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

# قسم تعديل الأسعار
st.subheader(texts[language]["save_prices"])
col3, col4 = st.columns(2)

with col3:
    new_egg_price = st.text_input(texts[language]["egg_price"], value="0.1155")

with col4:
    new_feed_price = st.text_input(texts[language]["feed_price"], value="0.0189")

if st.button(texts[language]["save_prices"], type="secondary"):
    if not is_number(new_egg_price) or not is_number(new_feed_price):
        st.error("" if language == "" else "" if language == "" else "")
    else:
        st.success("" if language == "" else "" if language == "" else "")

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
    # تخصيص الألوان
    colors = {
        '': '#4CAF50',
        '': '#FF9800',
        '': '#2196F3',
        '': '#F44336',
        '': '#9C27B0'
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
    st.subheader(texts[language]["chicken_profits"] + "")
    col5, col6 = st.columns(2)

    with col5:
        eggs = st.text_input(
            texts[language]["eggs_input"],
            value="",
            help="" if language == "" else "" if language == "" else ""
        )

    with col6:
        days = st.text_input(
            texts[language]["days_input"],
            value="",
            help="" if language == "" else "" if language == "" else ""
        )

    if st.button(texts[language]["calculate_profits"], type="primary"):
        try:
            eggs = float(eggs) if eggs else None
            days = float(days) if days else None

            if eggs is None or days is None:
                st.error("" if language == "" else "" if language == "" else "")
            elif eggs > 580:
                st.error("" if language == "" else "" if language == "" else "")
            elif days > 730:
                st.error("" if language == "" else "" if language == "" else "")
            else:
                # حساب الأرباح
                total_egg_price = eggs * float(new_egg_price)  
                total_feed_cost = (days * 2) * float(new_feed_price)  
                
                # حساب الإيجار
                total_rent = 6 if eggs >= 260 else 0  
                
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
                current_time = datetime.now() + timedelta(hours=3)  
                date_str = current_time.strftime("%Y-%m-%d")
                time_str = current_time.strftime("%I:%M %p")

                # إنشاء نص النتائج
                results_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                  {}                    ║
╠══════════════════════════════════════════════════════════════════╣
║ {}: {} {}
╟──────────────────────────────────────────────────────────────────╢
║ {}:
║ {}: {} USD
║ {}: {} USD
║ {}: {} USD
║ {}: {} USD
║ {}: {} USD
╟──────────────────────────────────────────────────────────────────╢
║ {}:
║ {}: {} IQD
║ {}: {} IQD
║ {}: {} IQD
║ {}: {} IQD
║ {}: {} IQD
╚══════════════════════════════════════════════════════════════════╝"""

                # عرض النتائج
                # st.code(results_text, language="text")

                # إنشاء DataFrame للرسم البياني
                df = pd.DataFrame({
                    texts[language]["category"]: [
                        f" {}",
                        f" {}",
                        f" ",
                        f" ",
                        f" "
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
                        f" {}",
                        f" {}",
                        f" ",
                        f" ",
                        f" "
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
                st.markdown(f"### {}")
                st.code(results_text)
                
        except ValueError:
            st.error("" if language == "" else "" if language == "" else "")

elif calculation_type == texts[language]["daily_rewards"]:
    st.subheader(texts[language]["daily_rewards"] + "")
    col7, col8 = st.columns(2)

    with col7:
        rewards = st.text_input(
            texts[language]["total_rewards"],
            value="",
            help="" if language == "" else "" if language == "" else ""
        )

    with col8:
        food = st.text_input(
            texts[language]["total_food_cost"],
            value="",
            help="" if language == "" else "" if language == "" else ""
        )

    if st.button(texts[language]["calculate_rewards"], type="primary"):
        try:
            rewards = float(rewards) if rewards else None
            food = float(food) if food else None

            if rewards is None or food is None:
                st.error("" if language == "" else "" if language == "" else "")
            else:
                # حساب الربح اليومي
                daily_profit = rewards * float(new_egg_price) - food * float(new_feed_price)

                # تحويل العملة
                if currency == "IQD":
                    daily_profit = daily_profit * 1480
                else:
                    daily_profit = daily_profit

                # تنسيق التاريخ والوقت حسب توقيت بغداد
                current_time = datetime.now() + timedelta(hours=3)  
                date_str = current_time.strftime("%Y-%m-%d")
                time_str = current_time.strftime("%I:%M %p")

                # إنشاء نص النتائج
                results_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║ {}: {} {}
╟──────────────────────────────────────────────────────────────────╢
║ {}:
║ {}: {} USD
║ {}: {} USD
║ {}: {} USD
╟──────────────────────────────────────────────────────────────────╢
║ {}:
║ {}: {} IQD
║ {}: {} IQD
║ {}: {} IQD
╚══════════════════════════════════════════════════════════════════╝"""

                # عرض النتائج
                # st.code(results_text, language="text")

                # إنشاء DataFrame للرسم البياني
                df = pd.DataFrame({
                    texts[language]["category"]: [
                        f" {}",
                        f" {}",
                        f" "
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
                        f" {}",
                        f" {}",
                        f" "
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
                st.markdown(f"### {}")
                st.code(results_text)
                
        except ValueError:
            st.error("" if language == "" else "" if language == "" else "")

# زر إعادة التعيين
if st.button(texts[language]["reset"], type="secondary"):
    st.success("" if language == "" else "" if language == "" else "")

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
