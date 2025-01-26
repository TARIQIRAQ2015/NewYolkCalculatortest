import streamlit as st
import pandas as pd
import plotly.express as px

# تنسيق الأرقام العشرية
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# تحسين الواجهة
st.set_page_config(page_title="Newyolk Chicken Calculator", page_icon="🐔", layout="wide")

# حالة اللغة (العربية، الإنجليزية، الرومانية)
if "language" not in st.session_state:
    st.session_state.language = "العربية"

# حالة الوضع (Dark أو Light)
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# اختيار اللغة في السايد بار
language = st.sidebar.selectbox("اختر اللغة / Choose Language / Alegeți limba", ["العربية", "English", "Română"])

# تبديل الوضع بين الفاتح والداكن
if st.sidebar.button("🌌 " + ("الوضع الداكن" if st.session_state.theme == "Light" else "الوضع الفاتح")):
    st.session_state.theme = "Light" if st.session_state.theme == "Dark" else "Dark"

# تحديث الألوان بناءً على الوضع الحالي
bg_color = "#ffffff" if st.session_state.theme == "Light" else "#121212"
font_color = "black" if st.session_state.theme == "Light" else "white"

# إعداد التصميم الديناميكي
st.markdown(
    f"""
    <style>
    body {{
        background-color: {bg_color};
        color: {font_color};
    }}
    .title {{
        font-size: 50px;
        font-weight: bold;
        color: {font_color};
        text-align: center;
        padding: 20px;
    }}
    .subtitle {{
        font-size: 30px;
        color: {font_color};
        text-align: center;
        margin-bottom: 30px;
    }}
    </style>
    <div class="title">🐔 {"حاسبة الدجاج - Newyolk" if language == "العربية" else "Newyolk - Chicken Calculator" if language == "English" else "Newyolk - Calculator de Pui"}</div>
    <div class="subtitle">{"حساب أرباح الدجاج والمكافآت اليومية" if language == "العربية" else "Calculate Chicken Profits and Daily Rewards" if language == "English" else "Calculează Profiturile și Recompensele Zilnice"}</div>
    """,
    unsafe_allow_html=True
)

# إدخال البيانات الديناميكية
col1, col2 = st.columns(2)

with col1:
    eggs = st.number_input(
        "عدد البيض 🥚" if language == "العربية" else "🥚 Number of Eggs",
        min_value=0,
        max_value=580,
        step=1,
        key="eggs"
    )

with col2:
    days = st.number_input(
        "عدد الأيام 📅" if language == "العربية" else "📅 Number of Days",
        min_value=0,
        max_value=730,
        step=1,
        key="days"
    )

if st.button("احسب" if language == "العربية" else "Calculate"):
    try:
        total_egg_price_usd = eggs * 0.1155
        total_feed_cost_usd = (days * 2) * 0.0189
        net_profit_usd = total_egg_price_usd - total_feed_cost_usd

        results = {
            "Item": ["Total Egg Price", "Total Feed Cost", "Net Profit"],
            "Value": [total_egg_price_usd, total_feed_cost_usd, net_profit_usd]
        }
        df = pd.DataFrame(results)

        # عرض النتائج
        st.table(df)

        # رسم بياني دائري
        fig = px.pie(
            data_frame=df, 
            values="Value", 
            names="Item",
            title="Cost Distribution",
            color_discrete_sequence=px.colors.sequential.RdBu
        )
        st.plotly_chart(fig, use_container_width=True)

    except Exception as e:
        st.error("حدث خطأ أثناء الحساب: " + str(e))

st.markdown(
    """
    <footer style="text-align:center; margin-top:20px; color:gray;">
        جميع الحقوق محفوظة 2025 &copy; by Tariq Al-Yaseen
    </footer>
    """,
    unsafe_allow_html=True
)
