import streamlit as st
import pandas as pd
import plotly.express as px

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تحسين الواجهة
st.set_page_config(
    page_title="Newyolk Chicken Calculator",
    page_icon="🐔", 
    layout="wide"
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

# النصوص للغة العربية
texts = {
    "العربية": {
        "title": "🐔 حاسبة الدجاج - Newyolk",
        "subtitle": "حساب أرباح الدجاج والمكافآت اليومية",
        "currency_select": "العملة 💰",
        "edit_prices": "تعديل الأسعار ⚙️",
        "new_egg_price": "سعر البيض الحالي 🥚",
        "new_feed_price": "سعر العلف الحالي 🌽",
        "save_prices": "حفظ الأسعار الجديدة 💾",
        "calculation_type": "نوع الحساب 📊",
        "chicken_profits": "أرباح الدجاجة",
        "daily_rewards": "أرباح المكافآت والطعام اليومي",
        "eggs_input": "عدد البيض 🥚",
        "days_input": "عدد الأيام 📅",
        "calculate_profits": "احسب أرباح الدجاجة 🧮",
        "rewards_input": "عدد المكافآت 🎁",
        "food_input": "عدد الطعام المطلوب 🌽",
        "calculate_rewards": "احسب أرباح المكافآت والطعام اليومي 🧮",
        "reset": "إعادة التعيين 🔄",
        "copyright": "by Tariq Al-Yaseen © 2025-2026"
    }
}

# تغيير اتجاه الكتابة بناءً على اللغة
st.markdown(
    f"""
    <style>
    body {{
        background: {'#ffffff' if st.session_state.theme == "Light" else 'linear-gradient(to right, #4B0082, #8A2BE2)'};
        color: {'black' if st.session_state.theme == "Light" else 'white'};
        direction: rtl;
    }}
    .title {{
        font-size: 50px;
        font-weight: bold;
        color: {'black' if st.session_state.theme == "Light" else 'white'};
        text-align: center;
        padding: 20px;
    }}
    .subtitle {{
        font-size: 30px;
        color: {'black' if st.session_state.theme == "Light" else 'white'};
        text-align: center;
        margin-bottom: 30px;
    }}
    .rtl {{
        direction: rtl;
        text-align: right;
        font-size: 24px;
        color: {'black' if st.session_state.theme == "Light" else 'white'};
    }}
    .stSelectbox, .stTextInput {{
        direction: rtl;
        text-align: right;
        font-size: 24px;
        color: {'black' if st.session_state.theme == "Light" else 'white'};
    }}
    .stButton button {{
        font-size: 24px;
    }}
    .stTable {{
        margin: 0 auto; /* توسيط الجدول */
        width: 50%; /* تحديد عرض الجدول */
        text-align: right; /* محاذاة النص إلى اليمين */
    }}
    .stTable th, .stTable td {{
        text-align: right !important; /* محاذاة النص داخل الخلايا إلى اليمين */
        direction: rtl !important; /* اتجاه النص من اليمين إلى اليسار */
    }}
    .center {{
        display: flex;
        justify-content: center;
        align-items: center;
        flex-direction: column;
    }}
    </style>
    <div class="title"> {texts["العربية"]["title"]}</div>
    <div class="subtitle">{texts["العربية"]["subtitle"]}</div>
    """,
    unsafe_allow_html=True
)

# استخدام الأعمدة لتخطيط أفضل
col1, col2 = st.columns(2)

with col1:
    currency = st.selectbox(
        texts["العربية"]["currency_select"],
        ["دولار أمريكي", "دينار عراقي"]
    )

with col2:
    calculation_type = st.selectbox(
        texts["العربية"]["calculation_type"],
        [texts["العربية"]["chicken_profits"], texts["العربية"]["daily_rewards"]]
    )

# قسم تعديل الأسعار
st.subheader(texts["العربية"]["edit_prices"])
col3, col4 = st.columns(2)

with col3:
    new_egg_price = st.text_input(texts["العربية"]["new_egg_price"], value=str(st.session_state.egg_price))

with col4:
    new_feed_price = st.text_input(texts["العربية"]["new_feed_price"], value=str(st.session_state.feed_price))

if st.button(texts["العربية"]["save_prices"], type="secondary"):
    try:
        st.session_state.egg_price = float(new_egg_price)
        st.session_state.feed_price = float(new_feed_price)
        st.success("تم حفظ الأسعار الجديدة بنجاح! ✅")
    except ValueError:
        st.error("يرجى إدخال أرقام صحيحة! ❗️")

# تحديث الأسعار بناءً على العملة
if currency == "دينار عراقي":
    egg_price_display = st.session_state.egg_price * 1480
    feed_price_display = st.session_state.feed_price * 1480
else:
    egg_price_display = st.session_state.egg_price
    feed_price_display = st.session_state.feed_price

st.write(f"سعر البيض الحالي: {format_decimal(egg_price_display)} {currency}")
st.write(f"سعر العلف الحالي: {format_decimal(feed_price_display)} {currency}")

if calculation_type == texts["العربية"]["chicken_profits"]:
    st.subheader("حساب أرباح الدجاجة 📈")
    col5, col6 = st.columns(2)

    with col5:
        eggs = st.text_input(
            texts["العربية"]["eggs_input"],
            value=st.session_state.eggs,
            help="أدخل عدد البيض (بحد أقصى 580)",
            key="eggs_input"
        )

    with col6:
        days = st.text_input(
            texts["العربية"]["days_input"],
            value=st.session_state.days,
            help="أدخل عدد الأيام (بحد أقصى 730)",
            key="days_input"
        )

    if st.button(texts["العربية"]["calculate_profits"], type="primary"):
        try:
            eggs = float(eggs) if eggs else None
            days = float(days) if days else None

            if eggs is None or days is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗️")
            elif eggs > 580:
                st.error("عدد البيض يجب ألا يتجاوز 580! ❗️")
            elif days > 730:
                st.error("عدد الأيام يجب ألا يتجاوز 730! ❗️")
            else:
                # حساب النتائج
                total_egg_price_usd = eggs * st.session_state.egg_price
                total_feed_cost_usd = (days * 2) * st.session_state.feed_price
                net_profit_before_rent_usd = total_egg_price_usd - total_feed_cost_usd

                # حساب تكلفة الإيجار بناءً على عدد البيض
                rent_cost_usd = 6.0 if eggs >= 260 else 0.0
                net_profit_usd = net_profit_before_rent_usd - rent_cost_usd

                if currency == "دينار عراقي":
                    total_egg_price = total_egg_price_usd * 1480
                    total_feed_cost = total_feed_cost_usd * 1480
                    net_profit_before_rent = net_profit_before_rent_usd * 1480
                    rent_cost = rent_cost_usd * 1480
                    net_profit = net_profit_usd * 1480
                else:
                    total_egg_price, total_feed_cost, net_profit_before_rent, rent_cost, net_profit = (
                        total_egg_price_usd, total_feed_cost_usd, net_profit_before_rent_usd, rent_cost_usd, net_profit_usd
                    )

                # إنشاء جدول للنتائج
                results = {
                    "العنصر": [
                        "سعر البيض الكلي 💰",
                        "تكلفة العلف الكلية 🌽",
                        "الربح قبل خصم الإيجار 📊",
                        "دفع الإيجار 💸",
                        "الربح الصافي 💵"
                    ],
                    "القيمة": [
                        f"{format_decimal(total_egg_price)} {currency}",
                        f"{format_decimal(total_feed_cost)} {currency}",
                        f"{format_decimal(net_profit_before_rent)} {currency}",
                        f"{format_decimal(rent_cost)} {currency}",
                        f"{format_decimal(net_profit)} {currency}"
                    ]
                }

                # عرض النتائج كجدول
                st.success("تم الحساب بنجاح! ✅")
                df = pd.DataFrame(results)
                df = df[["العنصر", "القيمة"]]  # تغيير ترتيب الأعمدة للغة العربية
                st.table(df)

                # إضافة رسم بياني شريطي
                chart_data = pd.DataFrame({
                    "الفئة": [
                        "سعر البيض الكلي",
                        "تكلفة العلف الكلية",
                        "دفع الإيجار"
                    ],
                    "القيمة": [
                        total_egg_price,
                        total_feed_cost,
                        rent_cost
                    ]
                })

                fig = px.bar(chart_data, x="الفئة", y="القيمة",
                             title="توزيع التكاليف والأرباح",
                             color="الفئة",
                             color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)

        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗️")

elif calculation_type == texts["العربية"]["daily_rewards"]:
    st.subheader("حساب أرباح المكافآت والطعام اليومي 📈")
    col7, col8 = st.columns(2)

    with col7:
        rewards = st.text_input(
            texts["العربية"]["rewards_input"],
            value=st.session_state.rewards,
            help="أدخل عدد المكافآت",
            key="rewards_input"
        )

    with col8:
        food = st.text_input(
            texts["العربية"]["food_input"],
            value=st.session_state.food,
            help="أدخل عدد الطعام المطلوب",
            key="food_input"
        )

    if st.button(texts["العربية"]["calculate_rewards"], type="primary"):
        try:
            rewards = float(rewards) if rewards else None
            food = float(food) if food else None

            if rewards is None or food is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗️")
            else:
                # حساب النتائج
                total_egg_price_usd = rewards * st.session_state.egg_price
                total_feed_cost_usd = food * st.session_state.feed_price
                net_profit_usd = total_egg_price_usd - total_feed_cost_usd

                if currency == "دينار عراقي":
                    total_egg_price = total_egg_price_usd * 1480
                    total_feed_cost = total_feed_cost_usd * 1480
                    net_profit = net_profit_usd * 1480
                else:
                    total_egg_price, total_feed_cost, net_profit = (
                        total_egg_price_usd, total_feed_cost_usd, net_profit_usd
                    )

                # إنشاء جدول للنتائج
                results = {
                    "العنصر": [
                        "سعر البيض الكلي 💰",
                        "تكلفة العلف الكلية 🌽",
                        "الربح اليومي 💵"
                    ],
                    "القيمة": [
                        f"{format_decimal(total_egg_price)} {currency}",
                        f"{format_decimal(total_feed_cost)} {currency}",
                        f"{format_decimal(net_profit)} {currency}"
                    ]
                }

                # عرض النتائج كجدول
                st.success("تم الحساب بنجاح! ✅")
                df = pd.DataFrame(results)
                df = df[["العنصر", "القيمة"]]  # تغيير ترتيب الأعمدة للغة العربية
                st.table(df)

                # إضافة رسم بياني شريطي
                chart_data = pd.DataFrame({
                    "الفئة": [
                        "سعر البيض الكلي",
                        "تكلفة العلف الكلية"
                    ],
                    "القيمة": [
                        total_egg_price,
                        total_feed_cost
                    ]
                })

                fig = px.bar(chart_data, x="الفئة", y="القيمة",
                             title="توزيع التكاليف والأرباح",
                             color="الفئة",
                             color_discrete_sequence=px.colors.qualitative.Pastel)
                st.plotly_chart(fig, use_container_width=True)

        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗️")

# زر إعادة التعيين
if st.button(texts["العربية"]["reset"], type="secondary"):
    st.session_state.egg_price = 0.1155
    st.session_state.feed_price = 0.0189
    st.session_state.eggs = ""
    st.session_state.days = ""
    st.session_state.rewards = ""
    st.session_state.food = ""
    st.success("تم إعادة التعيين بنجاح! ✅")

# إضافة نص حقوق النشر والأيقونات
st.markdown(
    """
    <div style="text-align: center; font-size: 16px; color: gray; margin-top: 30px; font-weight: bold;">
        <a href="https://www.facebook.com/newyolkfarming" target="_blank" style="text-decoration: none; color: inherit; margin: 0 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
        </a>
        <a href="https://farm.newyolk.io" target="_blank" style="text-decoration: none; color: inherit; margin: 0 10px;">
            <img src="https://i.ibb.co/YDKWBRf/internet.png" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
        </a>
        <a href="https://t.me/newyolkfarm" target="_blank" style="text-decoration: none; color: inherit; margin: 0 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" alt="Telegram" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
        </a>
        <a href="https://discord.gg/RYDExGGWXh" target="_blank" style="text-decoration: none; color: inherit; margin: 0 10px;">
            <img src="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png" alt="Discord" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
        </a>
        <br>
        <br>
        by Tariq Al-Yaseen © 2025-2026
    </div>
    <style>
        a img:hover {
            transform: scale(1.2);
        }
    </style>
    """,
    unsafe_allow_html=True
)
