import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# تحسين الواجهة - يجب أن يكون هذا أول أمر
st.set_page_config(
    page_title="Newyolk Chicken Calculator",
    page_icon="🐔"
)

# دالة تنسيق الأرقام العشرية
def format_decimal(number):
    """تنسيق الأرقام العشرية بشكل أنيق"""
    if isinstance(number, (int, float)):
        return f"{number:,.2f}".rstrip('0').rstrip('.')
    return str(number)

# إضافة CSS للزر العائم للتمرير إلى الأعلى
st.markdown("""
<style>
.floating-button {
    position: fixed;
    bottom: 20px;
    left: 20px;
    background-color: #4CAF50;
    color: white;
    width: 50px;
    height: 50px;
    border-radius: 25px;
    text-align: center;
    line-height: 50px;
    font-size: 24px;
    cursor: pointer;
    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.3);
    transition: all 0.3s ease;
    z-index: 999;
    display: none;
}

.floating-button:hover {
    background-color: #45a049;
    transform: scale(1.1);
    box-shadow: 3px 3px 15px rgba(0, 0, 0, 0.4);
}

.scroll-text {
    position: fixed;
    bottom: 75px;
    left: 10px;
    background-color: rgba(0, 0, 0, 0.7);
    color: white;
    padding: 5px 10px;
    border-radius: 5px;
    font-size: 12px;
    opacity: 0;
    transition: opacity 0.3s;
}

.floating-button:hover + .scroll-text {
    opacity: 1;
}
</style>

<script>
document.addEventListener('DOMContentLoaded', function() {
    var button = document.querySelector('.floating-button');
    var title = document.querySelector('h1');
    
    window.onscroll = function() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            button.style.display = "block";
        } else {
            button.style.display = "none";
        }
    };
    
    button.onclick = function() {
        title.scrollIntoView({ behavior: 'smooth' });
    };
});
</script>

<div class="floating-button">↑</div>
<div class="scroll-text">التمرير إلى الأعلى</div>
""", unsafe_allow_html=True)

# القيم الافتراضية
if 'egg_price' not in st.session_state:
    st.session_state.egg_price = 0.1155
if 'feed_price' not in st.session_state:
    st.session_state.feed_price = 0.0189
if 'eggs' not in st.session_state:
    st.session_state.eggs = ""
if 'days' not in st.session_state:
    st.session_state.days = ""
if 'rewards' not in st.session_state:
    st.session_state.rewards = ""
if 'food' not in st.session_state:
    st.session_state.food = ""

# تعريف النصوص
texts = {
    "العربية": {
        "title": "🐔 حاسبة الدجاج - Newyolk",
        "subtitle": "حساب أرباح الدجاج والمكافآت اليومية",
        "currency_select": "اختر العملة",
        "calculation_type": "اختر نوع الحساب",
        "chicken_profits": "أرباح الدجاج",
        "daily_rewards": "المكافآت اليومية",
        "new_egg_price": "سعر البيض الجديد",
        "new_feed_price": "سعر العلف الجديد",
        "edit_prices": "تعديل الأسعار",
        "save_prices": "حفظ الأسعار",
        "eggs_input": "عدد البيض",
        "days_input": "عدد الأيام",
        "calculate_profits": "حساب الأرباح",
        "rewards_input": "عدد المكافآت",
        "food_input": "عدد الطعام",
        "calculate_rewards": "حساب المكافآت",
        "reset": "إعادة التعيين",
        "results_title": "نتائج الحساب",
        "calculation_date": "تاريخ الحساب",
        "calculation_details": "تفاصيل الحساب",
        "current_prices": "الأسعار الحالية",
        "current_egg_price": "سعر البيض الحالي",
        "current_feed_price": "سعر العلف الحالي",
        "usd_results": "النتائج بالدولار",
        "iqd_results": "النتائج بالدينار",
        "net_profit": "الربح الصافي",
        "profit_before_rent": "الربح قبل الإيجار",
        "rent_payment": "دفع الإيجار",
        "am": "ص",
        "pm": "م",
        "scroll_top": "التمرير إلى الأعلى"
    },
    "English": {
        "title": "🐔 Chicken Calculator - Newyolk",
        "subtitle": "Calculate Chicken Profits and Daily Rewards",
        "currency_select": "Select Currency",
        "calculation_type": "Select Calculation Type",
        "chicken_profits": "Chicken Profits",
        "daily_rewards": "Daily Rewards",
        "new_egg_price": "New Egg Price",
        "new_feed_price": "New Feed Price",
        "edit_prices": "Edit Prices",
        "save_prices": "Save Prices",
        "eggs_input": "Number of Eggs",
        "days_input": "Number of Days",
        "calculate_profits": "Calculate Profits",
        "rewards_input": "Number of Rewards",
        "food_input": "Amount of Food",
        "calculate_rewards": "Calculate Rewards",
        "reset": "Reset",
        "results_title": "Calculation Results",
        "calculation_date": "Calculation Date",
        "calculation_details": "Calculation Details",
        "current_prices": "Current Prices",
        "current_egg_price": "Current Egg Price",
        "current_feed_price": "Current Feed Price",
        "usd_results": "USD Results",
        "iqd_results": "IQD Results",
        "net_profit": "Net Profit",
        "profit_before_rent": "Profit Before Rent",
        "rent_payment": "Rent Payment",
        "am": "AM",
        "pm": "PM",
        "scroll_top": "Scroll to Top"
    },
    "Română": {
        "title": "🐔 Calculator de pui - Newyolk",
        "subtitle": "Calculul profiturilor de pui și recompenselor zilnice",
        "currency_select": "Selectați moneda",
        "calculation_type": "Selectați tipul de calcul",
        "chicken_profits": "Profiturile de pui",
        "daily_rewards": "Recompensele zilnice",
        "new_egg_price": "Noul preț al ouălor",
        "new_feed_price": "Noul preț al hranei",
        "edit_prices": "Editează prețurile",
        "save_prices": "Salvează prețurile",
        "eggs_input": "Numărul de ouă",
        "days_input": "Numărul de zile",
        "calculate_profits": "Calculează profiturile",
        "rewards_input": "Numărul de recompense",
        "food_input": "Cantitatea de hrană",
        "calculate_rewards": "Calculează recompensele",
        "reset": "Resetează",
        "results_title": "Rezultatele calculului",
        "calculation_date": "Data calculului",
        "calculation_details": "Detalii calcul",
        "current_prices": "Prețurile actuale",
        "current_egg_price": "Prețul actual al ouălor",
        "current_feed_price": "Prețul actual al hranei",
        "usd_results": "Rezultatele în USD",
        "iqd_results": "Rezultatele în IQD",
        "net_profit": "Profitul net",
        "profit_before_rent": "Profitul înainte de chirie",
        "rent_payment": "Plata chiriei",
        "am": "AM",
        "pm": "PM",
        "scroll_top": "Derulați spre sus"
    },
    "Français": {
        "title": "🐔 Calculatrice de poulet - Newyolk",
        "subtitle": "Calcul des profits de poulet et des récompenses quotidiennes",
        "currency_select": "Sélectionnez la devise",
        "calculation_type": "Sélectionnez le type de calcul",
        "chicken_profits": "Profits de poulet",
        "daily_rewards": "Récompenses quotidiennes",
        "new_egg_price": "Nouveau prix des œufs",
        "new_feed_price": "Nouveau prix de la nourriture",
        "edit_prices": "Éditez les prix",
        "save_prices": "Enregistrez les prix",
        "eggs_input": "Nombre d'œufs",
        "days_input": "Nombre de jours",
        "calculate_profits": "Calculez les profits",
        "rewards_input": "Nombre de récompenses",
        "food_input": "Quantité de nourriture",
        "calculate_rewards": "Calculez les récompenses",
        "reset": "Réinitialisez",
        "results_title": "Résultats du calcul",
        "calculation_date": "Date du calcul",
        "calculation_details": "Détails du calcul",
        "current_prices": "Prix actuels",
        "current_egg_price": "Prix actuel des œufs",
        "current_feed_price": "Prix actuel de la nourriture",
        "usd_results": "Résultats en USD",
        "iqd_results": "Résultats en IQD",
        "net_profit": "Bénéfice net",
        "profit_before_rent": "Bénéfice avant loyer",
        "rent_payment": "Paiement du loyer",
        "am": "AM",
        "pm": "PM",
        "scroll_top": "Défilez vers le haut"
    },
    "Español": {
        "title": "🐔 Calculadora de pollo - Newyolk",
        "subtitle": "Cálculo de ganancias de pollo y recompensas diarias",
        "currency_select": "Seleccione la moneda",
        "calculation_type": "Seleccione el tipo de cálculo",
        "chicken_profits": "Ganancias de pollo",
        "daily_rewards": "Recompensas diarias",
        "new_egg_price": "Nuevo precio de los huevos",
        "new_feed_price": "Nuevo precio de la comida",
        "edit_prices": "Editar precios",
        "save_prices": "Guardar precios",
        "eggs_input": "Número de huevos",
        "days_input": "Número de días",
        "calculate_profits": "Calcular ganancias",
        "rewards_input": "Número de recompensas",
        "food_input": "Cantidad de comida",
        "calculate_rewards": "Calcular recompensas",
        "reset": "Reiniciar",
        "results_title": "Resultados del cálculo",
        "calculation_date": "Fecha del cálculo",
        "calculation_details": "Detalles del cálculo",
        "current_prices": "Precios actuales",
        "current_egg_price": "Precio actual de los huevos",
        "current_feed_price": "Precio actual de la comida",
        "usd_results": "Resultados en USD",
        "iqd_results": "Resultados en IQD",
        "net_profit": "Beneficio neto",
        "profit_before_rent": "Beneficio antes de alquiler",
        "rent_payment": "Pago de alquiler",
        "am": "AM",
        "pm": "PM",
        "scroll_top": "Desplazarse hacia arriba"
    },
    "日本語": {
        "title": "🐔 ニューヨーク鶏計算機",
        "subtitle": "鶏の利益と日次報酬の計算",
        "currency_select": "通貨を選択",
        "calculation_type": "計算タイプを選択",
        "chicken_profits": "鶏の利益",
        "daily_rewards": "日次報酬",
        "new_egg_price": "新しい卵の価格",
        "new_feed_price": "新しい飼料の価格",
        "edit_prices": "価格を編集",
        "save_prices": "価格を保存",
        "eggs_input": "卵の数",
        "days_input": "日数",
        "calculate_profits": "利益を計算",
        "rewards_input": "報酬の数",
        "food_input": "飼料の量",
        "calculate_rewards": "報酬を計算",
        "reset": "リセット",
        "results_title": "計算結果",
        "calculation_date": "計算日",
        "calculation_details": "計算詳細",
        "current_prices": "現在の価格",
        "current_egg_price": "現在の卵の価格",
        "current_feed_price": "現在の飼料の価格",
        "usd_results": "USD結果",
        "iqd_results": "IQD結果",
        "net_profit": "純利益",
        "profit_before_rent": "家賃前の利益",
        "rent_payment": "家賃の支払い",
        "am": "AM",
        "pm": "PM",
        "scroll_top": "上にスクロール"
    }
}

# اختيار اللغة
language = st.selectbox("Select Language", ["العربية", "English", "Română", "Français", "Español", "日本語"])

# عرض العنوان الرئيسي
st.markdown(f"""
    <div class="main-title">
        <h1>{texts[language]['title']}</h1>
        <p>{texts[language]['subtitle']}</p>
    </div>
""", unsafe_allow_html=True)

# إضافة CSS لتحسين الواجهة
st.markdown("""
<style>
    .main-title {
        text-align: center;
        padding: 2rem 0;
        margin-bottom: 2rem;
        background: linear-gradient(120deg, #f1f8e9, #c8e6c9);
        border-radius: 10px;
    }
    
    .main-title h1 {
        color: #2e7d32;
        font-size: 2.5rem;
        font-weight: bold;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
        margin-bottom: 1rem;
    }
    
    .main-title p {
        color: #1b5e20;
        font-size: 1.2rem;
        margin: 0;
    }
    
    /* باقي التنسيقات */
</style>
""", unsafe_allow_html=True)

# استخدام الأعمدة لتخطيط أفضل
col1, col2 = st.columns(2)

with col1:
    currency = st.selectbox(
        texts[language]["currency_select"],
        ["دولار أمريكي", "دينار عراقي"] if language == "العربية" else ["USD", "IQD"] if language == "English" else ["USD", "IQD"] if language == "Română" else ["EUR", "USD"] if language == "Français" else ["EUR", "USD"] if language == "Español" else ["JPY", "USD"]
    )

with col2:
    calculation_type = st.selectbox(
        texts[language]["calculation_type"],
        [texts[language]["chicken_profits"], texts[language]["daily_rewards"]]
    )

# قسم تعديل الأسعار
st.subheader(texts[language]["edit_prices"])
col3, col4 = st.columns(2)

with col3:
    new_egg_price = st.text_input(texts[language]["new_egg_price"], value=str(st.session_state.egg_price))

with col4:
    new_feed_price = st.text_input(texts[language]["new_feed_price"], value=str(st.session_state.feed_price))

if st.button(texts[language]["save_prices"], type="secondary"):
    try:
        st.session_state.egg_price = float(new_egg_price)
        st.session_state.feed_price = float(new_feed_price)
        st.success("تم حفظ الأسعار الجديدة بنجاح! ✅" if language == "العربية" else "New prices saved successfully! ✅" if language == "English" else "Prețurile noi au fost salvate cu succes! ✅" if language == "Română" else "Les nouveaux prix ont été sauvegardés avec succès! ✅" if language == "Français" else "Los nuevos precios se han guardado con éxito! ✅" if language == "Español" else "新しい価格が正常に保存されました! ✅")
    except ValueError:
        st.error("يرجى إدخال أرقام صحيحة! ❗️" if language == "العربية" else "Please enter valid numbers! ❗️" if language == "English" else "Vă rugăm să introduceți numere valide! ❗️" if language == "Română" else "Veuillez entrer des nombres valides! ❗️" if language == "Français" else "Por favor, introduzca números válidos! ❗️" if language == "Español" else "有効な数字を入力してください! ❗️")

# تحديث الأسعار بناءً على العملة
if currency in ["دينار عراقي", "IQD"]:
    egg_price_display = st.session_state.egg_price * 1480
    feed_price_display = st.session_state.feed_price * 1480
elif currency in ["EUR"]:
    egg_price_display = st.session_state.egg_price * 0.88
    feed_price_display = st.session_state.feed_price * 0.88
elif currency in ["JPY"]:
    egg_price_display = st.session_state.egg_price * 110.45
    feed_price_display = st.session_state.feed_price * 110.45
else:
    egg_price_display = st.session_state.egg_price
    feed_price_display = st.session_state.feed_price

st.write(f"{texts[language]['new_egg_price']}: {format_decimal(egg_price_display)} {currency}")
st.write(f"{texts[language]['new_feed_price']}: {format_decimal(feed_price_display)} {currency}")

# دالة مساعدة لإنشاء زر النسخ
def create_copy_button(text_to_copy, button_text):
    # إنشاء معرف فريد للنص
    button_id = f"copy_button_{hash(text_to_copy)}"
    
    # JavaScript لنسخ النص
    js_code = f"""
    <script>
    function copyText{button_id}() {{
        const el = document.createElement('textarea');
        el.value = `{text_to_copy}`;
        document.body.appendChild(el);
        el.select();
        document.execCommand('copy');
        document.body.removeChild(el);
    }}
    </script>
    """
    
    # HTML لزر النسخ
    button_html = f"""
    {js_code}
    <button 
        onclick="copyText{button_id}()"
        style="
            background-color: #4CAF50;
            border: none;
            color: white;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 16px;
            margin: 4px 2px;
            cursor: pointer;
            border-radius: 4px;
            transition: background-color 0.3s;
        "
        onmouseover="this.style.backgroundColor='#45a049'"
        onmouseout="this.style.backgroundColor='#4CAF50'"
    >
        {button_text} 📋
    </button>
    """
    
    return button_html

def create_custom_chart(df, language):
    # تخصيص الألوان والتصميم
    custom_colors = ['#4CAF50', '#FF9800', '#2196F3', '#F44336', '#9C27B0']
    
    # إنشاء رسم بياني دائري متقدم
    fig = px.pie(
        df,
        values=texts[language]["value"],
        names=texts[language]["category"],
        hole=0.6,  # جعل الرسم البياني دائري مع فراغ في المنتصف
        color_discrete_sequence=custom_colors
    )
    
    # تخصيص تصميم الرسم البياني
    fig.update_traces(
        textposition='outside',
        textinfo='percent+label',
        hovertemplate="<b>%{label}</b><br>" +
                     f"{texts[language]['value']}: %{{value:,.2f}}<br>" +
                     "النسبة: %{percent}<br><extra></extra>"
    )
    
    # تحديث تخطيط الرسم البياني
    fig.update_layout(
        showlegend=True,
        legend=dict(
            orientation="h",
            yanchor="bottom",
            y=-0.3,
            xanchor="center",
            x=0.5
        ),
        margin=dict(t=60, l=0, r=0, b=0),
        height=500,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(size=14),
        title=dict(
            text=texts[language]["results_title"],
            y=0.95,
            x=0.5,
            xanchor='center',
            yanchor='top',
            font=dict(size=20)
        ),
        annotations=[
            dict(
                text=texts[language]["net_profit"],
                x=0.5,
                y=0.5,
                font=dict(size=16),
                showarrow=False
            )
        ]
    )
    
    return fig

if calculation_type == texts[language]["chicken_profits"]:
    st.subheader(texts[language]["chicken_profits"] + " 📈")
    col5, col6 = st.columns(2)

    with col5:
        eggs = st.text_input(
            texts[language]["eggs_input"],
            value=st.session_state.eggs,
            help="أدخل عدد البيض (بحد أقصى 580)" if language == "العربية" else "Enter the number of eggs (max 580)" if language == "English" else "Introduceți numărul de ouă (maxim 580)" if language == "Română" else "Entrez le nombre d'œufs (max 580)" if language == "Français" else "Introduzca el número de huevos (máximo 580)" if language == "Español" else "卵の数を入力してください (最大580)",
            key="eggs_input"
        )

    with col6:
        days = st.text_input(
            texts[language]["days_input"],
            value=st.session_state.days,
            help="أدخل عدد الأيام (بحد أقصى 730)" if language == "العربية" else "Enter the number of days (max 730)" if language == "English" else "Introduceți numărul de zile (maxim 730)" if language == "Română" else "Entrez le nombre de jours (max 730)" if language == "Français" else "Introduzca el número de días (máximo 730)" if language == "Español" else "日数を入力してください (最大730)",
            key="days_input"
        )

    if st.button(texts[language]["calculate_profits"], type="primary"):
        try:
            eggs = float(eggs) if eggs else None
            days = float(days) if days else None

            if eggs is None or days is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗️" if language == "العربية" else "Please enter all required values! ❗️" if language == "English" else "Vă rugăm să introduceți toate valorile necesare! ❗️" if language == "Română" else "Veuillez entrer toutes les valeurs requises! ❗️" if language == "Français" else "Por favor, introduzca todos los valores necesarios! ❗️" if language == "Español" else "すべての必要な値を入力してください! ❗️")
            elif eggs > 580:
                st.error("عدد البيض يجب ألا يتجاوز 580! ❗️" if language == "العربية" else "Number of eggs should not exceed 580! ❗️" if language == "English" else "Numărul de ouă nu trebuie să depășească 580! ❗️" if language == "Română" else "Le nombre d'œufs ne doit pas dépasser 580! ❗️" if language == "Français" else "El número de huevos no debe exceder 580! ❗️" if language == "Español" else "卵の数は580を超えることはできません! ❗️")
            elif days > 730:
                st.error("عدد الأيام يجب ألا يتجاوز 730! ❗️" if language == "العربية" else "Number of days should not exceed 730! ❗️" if language == "English" else "Numărul de zile nu trebuie să depășească 730! ❗️" if language == "Română" else "Le nombre de jours ne doit pas dépasser 730! ❗️" if language == "Français" else "El número de días no debe exceder 730! ❗️" if language == "Español" else "日数は730を超えることはできません! ❗️")
            else:
                # حساب النتائج
                total_egg_price_usd = eggs * st.session_state.egg_price
                total_feed_cost_usd = (days * 0.15) * st.session_state.feed_price
                net_profit_before_rent_usd = total_egg_price_usd - total_feed_cost_usd
                rent_cost_usd = days * 0.0082
                net_profit_usd = net_profit_before_rent_usd - rent_cost_usd

                # تحويل العملة
                if currency in ["دينار عراقي", "IQD"]:
                    total_egg_price = total_egg_price_usd * 1480
                    total_feed_cost = total_feed_cost_usd * 1480
                    net_profit_before_rent = net_profit_before_rent_usd * 1480
                    rent_cost = rent_cost_usd * 1480
                    net_profit = net_profit_usd * 1480
                elif currency in ["EUR"]:
                    total_egg_price = total_egg_price_usd * 0.88
                    total_feed_cost = total_feed_cost_usd * 0.88
                    net_profit_before_rent = net_profit_before_rent_usd * 0.88
                    rent_cost = rent_cost_usd * 0.88
                    net_profit = net_profit_usd * 0.88
                elif currency in ["JPY"]:
                    total_egg_price = total_egg_price_usd * 110.45
                    total_feed_cost = total_feed_cost_usd * 110.45
                    net_profit_before_rent = net_profit_before_rent_usd * 110.45
                    rent_cost = rent_cost_usd * 110.45
                    net_profit = net_profit_usd * 110.45
                else:
                    total_egg_price, total_feed_cost, net_profit_before_rent, rent_cost, net_profit = (
                        total_egg_price_usd, total_feed_cost_usd, net_profit_before_rent_usd, rent_cost_usd, net_profit_usd
                    )

                # تعديل طريقة عرض النتائج
                st.markdown("""
                <style>
                .result-container {
                    background: linear-gradient(120deg, #1a1a1a, #2d2d2d);
                    border-radius: 15px;
                    padding: 20px;
                    margin: 20px 0;
                    color: white;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                .result-item {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 15px;
                    border-bottom: 1px solid #3d3d3d;
                    transition: all 0.3s ease;
                }
                .result-item:last-child {
                    border-bottom: none;
                }
                .result-item:hover {
                    background: rgba(255, 255, 255, 0.05);
                    transform: translateX(5px);
                }
                .result-label {
                    font-size: 18px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                .result-value {
                    font-size: 18px;
                    font-weight: bold;
                    color: #4CAF50;
                }
                </style>
                """, unsafe_allow_html=True)

                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                
                # عرض سعر البيض الحالي
                st.markdown(f"""
                    <div class="result-item">
                        <div class="result-label">
                            💰 🥚 {texts[language]['current_egg_price']}
                        </div>
                        <div class="result-value">
                            {format_decimal(st.session_state.egg_price)} {texts[language]['currency']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # عرض سعر العلف الحالي
                st.markdown(f"""
                    <div class="result-item">
                        <div class="result-label">
                            🌾 🌾 {texts[language]['current_feed_price']}
                        </div>
                        <div class="result-value">
                            {format_decimal(st.session_state.feed_price)} {texts[language]['currency']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # عرض الربح قبل الإيجار
                st.markdown(f"""
                    <div class="result-item">
                        <div class="result-label">
                            📊 📊 {texts[language]['profit_before_rent']}
                        </div>
                        <div class="result-value">
                            {format_decimal(net_profit_before_rent)} {texts[language]['currency']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # عرض دفع الإيجار
                st.markdown(f"""
                    <div class="result-item">
                        <div class="result-label">
                            💎 🏠 {texts[language]['rent_payment']}
                        </div>
                        <div class="result-value">
                            {format_decimal(rent_cost)} {texts[language]['currency']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # عرض صافي الربح
                st.markdown(f"""
                    <div class="result-item">
                        <div class="result-label">
                            💹 💰 {texts[language]['net_profit']}
                        </div>
                        <div class="result-value">
                            {format_decimal(net_profit)} {texts[language]['currency']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

                # تنسيق التاريخ والوقت بنظام 12 ساعة
                current_time = datetime.now()
                hour = current_time.hour
                am_pm = texts[language]["am"] if hour < 12 else texts[language]["pm"]
                if hour > 12:
                    hour -= 12
                elif hour == 0:
                    hour = 12
                formatted_time = current_time.strftime(f"%Y-%m-%d {hour}:%M") + f" {am_pm}"

                # إنشاء نص النتائج بتنسيق جديد وأنيق
                results_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                  {texts[language]['results_title']}                    ║
╠══════════════════════════════════════════════════════════════════╣
║ {texts[language]['calculation_date']}: {formatted_time}
║ {texts[language]['calculation_details']}: {texts[language]['chicken_profits']}
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['current_prices']}:
║ ▸ {texts[language]['current_egg_price']}: {format_decimal(st.session_state.egg_price)} USD
║ ▸ {texts[language]['current_feed_price']}: {format_decimal(st.session_state.feed_price)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['usd_results']}:
║ ▸ {texts[language]['eggs_input']}: {format_decimal(total_egg_price_usd)} USD
║ ▸ {texts[language]['food_input']}: {format_decimal(total_feed_cost_usd)} USD
║ ▸ {texts[language]['profit_before_rent']}: {format_decimal(net_profit_before_rent_usd)} USD
║ ▸ {texts[language]['rent_payment']}: {format_decimal(rent_cost_usd)} USD
║ ▸ {texts[language]['net_profit']}: {format_decimal(net_profit_usd)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['iqd_results']}:
║ ▸ {texts[language]['eggs_input']}: {format_decimal(total_egg_price_usd * 1480)} IQD
║ ▸ {texts[language]['food_input']}: {format_decimal(total_feed_cost_usd * 1480)} IQD
║ ▸ {texts[language]['profit_before_rent']}: {format_decimal(net_profit_before_rent_usd * 1480)} IQD
║ ▸ {texts[language]['rent_payment']}: {format_decimal(rent_cost_usd * 1480)} IQD
║ ▸ {texts[language]['net_profit']}: {format_decimal(net_profit_usd * 1480)} IQD
╚══════════════════════════════════════════════════════════════════╝"""

                # عرض النتائج
                st.code(results_text, language="text")

                # إنشاء DataFrame للرسم البياني
                chart_data = {
                    texts[language]["category"]: [
                        texts[language]["eggs_input"],
                        texts[language]["food_input"],
                        texts[language]["profit_before_rent"],
                        texts[language]["rent_payment"],
                        texts[language]["net_profit"]
                    ],
                    texts[language]["value"]: [
                        total_egg_price_usd,
                        total_feed_cost_usd,
                        net_profit_before_rent_usd,
                        rent_cost_usd,
                        net_profit_usd
                    ]
                }
                df = pd.DataFrame(chart_data)
                
                # إنشاء وعرض الرسم البياني المخصص
                fig = create_custom_chart(df, language)
                st.plotly_chart(fig, use_container_width=True)

        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗️" if language == "العربية" else "Please enter valid numbers! ❗️" if language == "English" else "Vă rugăm să introduceți numere valide! ❗️" if language == "Română" else "Veuillez entrer des nombres valides! ❗️" if language == "Français" else "Por favor, introduzca números válidos! ❗️" if language == "Español" else "有効な数字を入力してください! ❗️")

elif calculation_type == texts[language]["daily_rewards"]:
    st.subheader(texts[language]["daily_rewards"] + " 📈")
    col7, col8 = st.columns(2)

    with col7:
        rewards = st.text_input(
            texts[language]["rewards_input"],
            value=st.session_state.rewards,
            help="أدخل عدد المكافآت" if language == "العربية" else "Enter the number of rewards" if language == "English" else "Introduceți numărul de recompense" if language == "Română" else "Entrez le nombre de récompenses" if language == "Français" else "Introduzca el número de recompensas" if language == "Español" else "報酬の数を入力してください",
            key="rewards_input"
        )

    with col8:
        food = st.text_input(
            texts[language]["food_input"],
            value=st.session_state.food,
            help="أدخل عدد الطعام المطلوب" if language == "العربية" else "Enter the amount of food needed" if language == "English" else "Introduceți cantitatea de mâncare necesară" if language == "Română" else "Entrez la quantité de nourriture nécessaire" if language == "Français" else "Introduzca la cantidad de alimento necesaria" if language == "Español" else "必要な餌の量を入力してください",
            key="food_input"
        )

    if st.button(texts[language]["calculate_rewards"], type="primary"):
        try:
            rewards = float(rewards) if rewards else None
            food = float(food) if food else None

            if rewards is None or food is None:
                st.error("يرجى إدخال جميع القيم المطلوبة! ❗️" if language == "العربية" else "Please enter all required values! ❗️" if language == "English" else "Vă rugăm să introduceți toate valorile necesare! ❗️" if language == "Română" else "Veuillez entrer toutes les valeurs requises! ❗️" if language == "Français" else "Por favor, introduzca todos los valores necesarios! ❗️" if language == "Español" else "すべての必要な値を入力してください! ❗️")
            else:
                # حساب النتائج
                total_egg_price_usd = rewards * st.session_state.egg_price
                total_feed_cost_usd = food * st.session_state.feed_price
                net_profit_usd = total_egg_price_usd - total_feed_cost_usd

                # تحويل العملة
                if currency in ["دينار عراقي", "IQD"]:
                    total_egg_price = total_egg_price_usd * 1480
                    total_feed_cost = total_feed_cost_usd * 1480
                    net_profit = net_profit_usd * 1480
                elif currency in ["EUR"]:
                    total_egg_price = total_egg_price_usd * 0.88
                    total_feed_cost = total_feed_cost_usd * 0.88
                    net_profit = net_profit_usd * 0.88
                elif currency in ["JPY"]:
                    total_egg_price = total_egg_price_usd * 110.45
                    total_feed_cost = total_feed_cost_usd * 110.45
                    net_profit = net_profit_usd * 110.45
                else:
                    total_egg_price, total_feed_cost, net_profit = (
                        total_egg_price_usd, total_feed_cost_usd, net_profit_usd
                    )

                # تعديل طريقة عرض النتائج
                st.markdown("""
                <style>
                .result-container {
                    background: linear-gradient(120deg, #1a1a1a, #2d2d2d);
                    border-radius: 15px;
                    padding: 20px;
                    margin: 20px 0;
                    color: white;
                    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
                }
                .result-item {
                    display: flex;
                    justify-content: space-between;
                    align-items: center;
                    padding: 15px;
                    border-bottom: 1px solid #3d3d3d;
                    transition: all 0.3s ease;
                }
                .result-item:last-child {
                    border-bottom: none;
                }
                .result-item:hover {
                    background: rgba(255, 255, 255, 0.05);
                    transform: translateX(5px);
                }
                .result-label {
                    font-size: 18px;
                    display: flex;
                    align-items: center;
                    gap: 10px;
                }
                .result-value {
                    font-size: 18px;
                    font-weight: bold;
                    color: #4CAF50;
                }
                </style>
                """, unsafe_allow_html=True)

                st.markdown('<div class="result-container">', unsafe_allow_html=True)
                
                # عرض سعر البيض الحالي
                st.markdown(f"""
                    <div class="result-item">
                        <div class="result-label">
                            💰 🥚 {texts[language]['current_egg_price']}
                        </div>
                        <div class="result-value">
                            {format_decimal(st.session_state.egg_price)} {texts[language]['currency']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # عرض سعر العلف الحالي
                st.markdown(f"""
                    <div class="result-item">
                        <div class="result-label">
                            🌾 🌾 {texts[language]['current_feed_price']}
                        </div>
                        <div class="result-value">
                            {format_decimal(st.session_state.feed_price)} {texts[language]['currency']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                # عرض الربح الصافي
                st.markdown(f"""
                    <div class="result-item">
                        <div class="result-label">
                            💹 💰 {texts[language]['net_profit']}
                        </div>
                        <div class="result-value">
                            {format_decimal(net_profit)} {texts[language]['currency']}
                        </div>
                    </div>
                """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)

                # تنسيق التاريخ والوقت بنظام 12 ساعة
                current_time = datetime.now()
                hour = current_time.hour
                am_pm = texts[language]["am"] if hour < 12 else texts[language]["pm"]
                if hour > 12:
                    hour -= 12
                elif hour == 0:
                    hour = 12
                formatted_time = current_time.strftime(f"%Y-%m-%d {hour}:%M") + f" {am_pm}"

                # إنشاء نص النتائج بتنسيق جديد وأنيق
                results_text = f"""
╔══════════════════════════════════════════════════════════════════╗
║                  {texts[language]['results_title']}                    ║
╠══════════════════════════════════════════════════════════════════╣
║ {texts[language]['calculation_date']}: {formatted_time}
║ {texts[language]['calculation_details']}: {texts[language]['daily_rewards']}
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['current_prices']}:
║ ▸ {texts[language]['current_egg_price']}: {format_decimal(st.session_state.egg_price)} USD
║ ▸ {texts[language]['current_feed_price']}: {format_decimal(st.session_state.feed_price)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['usd_results']}:
║ ▸ {texts[language]['rewards_input']}: {format_decimal(total_egg_price_usd)} USD
║ ▸ {texts[language]['food_input']}: {format_decimal(total_feed_cost_usd)} USD
║ ▸ {texts[language]['net_profit']}: {format_decimal(net_profit_usd)} USD
╟──────────────────────────────────────────────────────────────────╢
║ {texts[language]['iqd_results']}:
║ ▸ {texts[language]['rewards_input']}: {format_decimal(total_egg_price_usd * 1480)} IQD
║ ▸ {texts[language]['food_input']}: {format_decimal(total_feed_cost_usd * 1480)} IQD
║ ▸ {texts[language]['net_profit']}: {format_decimal(net_profit_usd * 1480)} IQD
╚══════════════════════════════════════════════════════════════════╝"""

                # عرض النتائج
                st.code(results_text, language="text")

                # إنشاء DataFrame للرسم البياني
                chart_data = {
                    texts[language]["category"]: [
                        texts[language]["rewards_input"],
                        texts[language]["food_input"]
                    ],
                    texts[language]["value"]: [
                        total_egg_price_usd,
                        total_feed_cost_usd
                    ]
                }
                df = pd.DataFrame(chart_data)
                
                # إنشاء وعرض الرسم البياني المخصص
                fig = create_custom_chart(df, language)
                st.plotly_chart(fig, use_container_width=True)

        except ValueError:
            st.error("يرجى إدخال أرقام صحيحة! ❗️" if language == "العربية" else "Please enter valid numbers! ❗️" if language == "English" else "Vă rugăm să introduceți numere valide! ❗️" if language == "Română" else "Veuillez entrer des nombres valides! ❗️" if language == "Français" else "Por favor, introduzca números válidos! ❗️" if language == "Español" else "有効な数字を入力してください! ❗️")

# تعديل عرض النتائج
if 'results' in st.session_state:
    # عرض النتائج كنص فقط
    st.success("تم الحساب بنجاح! ✅" if language == "العربية" else 
              "Calculation successful! ✅" if language == "English" else 
              "Calcul reușit! ✅" if language == "Română" else 
              "Le calcul a été effectué avec succès! ✅" if language == "Français" else 
              "El cálculo se ha realizado con éxito! ✅" if language == "Español" else 
              "計算が正常に完了しました! ✅")

    # تنسيق التاريخ والوقت
    current_time = datetime.now()
    am_pm = texts[language]["am"] if current_time.hour < 12 else texts[language]["pm"]
    hour_12 = current_time.hour if current_time.hour <= 12 else current_time.hour - 12
    if hour_12 == 0:
        hour_12 = 12
    formatted_time = f"{hour_12}:{current_time.minute:02d} {am_pm}"
    formatted_date = current_time.strftime("%Y-%m-%d")
    
    st.write(f"{texts[language]['calculation_date']}: {formatted_date} {formatted_time}")

    # إنشاء الرسم البياني
    fig = create_custom_chart(df, language)
    st.plotly_chart(fig, use_container_width=True)

    # عرض الجدول النهائي بتنسيق أنيق
    st.markdown("""
    <style>
    .dataframe {
        font-size: 14px !important;
        text-align: center !important;
    }
    .dataframe th {
        background-color: #4CAF50 !important;
        color: white !important;
        font-weight: bold !important;
        text-align: center !important;
    }
    .dataframe td {
        text-align: center !important;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # تنظيم البيانات في الجدول
    df = df.round(2)  # تقريب الأرقام إلى رقمين عشريين
    df[texts[language]["value"]] = df[texts[language]["value"]].apply(lambda x: f"{x:,.2f} {texts[language]['currency']}")
    st.table(df)

# زر إعادة التعيين
if st.button(texts[language]["reset"], type="secondary"):
    st.session_state.egg_price = 0.1155
    st.session_state.feed_price = 0.0189
    st.session_state.eggs = ""
    st.session_state.days = ""
    st.session_state.rewards = ""
    st.session_state.food = ""
    st.success("تم إعادة التعيين بنجاح! ✅" if language == "العربية" else "Reset successful! ✅" if language == "English" else "Resetare reușită! ✅" if language == "Română" else "Réinitialisation réussie! ✅" if language == "Français" else "Reinicio exitoso! ✅" if language == "Español" else "リセットが正常に完了しました! ✅")

# تحديث نص زر التمرير حسب اللغة
scroll_text = texts[language].get("scroll_top", "Scroll to Top")
st.markdown(f"""
<script>
document.querySelector('.scroll-text').innerText = "{scroll_text}";
</script>
""", unsafe_allow_html=True)

# إضافة نص حقوق النشر والأيقونات
st.markdown(
    """
    <div style="text-align: center; font-size: 16px; color: gray; margin-top: 30px; font-weight: bold;">
            <img src="https://i.ibb.co/YDKWBRf/internet.png" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
        </a>
        <a href="https://discord.gg/RYDExGGWXh" target="_blank" style="text-decoration: none; color: inherit; margin: 0 10px;">
            <img src="https://assets-global.website-files.com/6257adef93867e50d84d30e2/636e0a6a49cf127bf92de1e2_icon_clyde_blurple_RGB.png" alt="Discord" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
         </a>
        <a href="https://t.me/newyolkfarm" target="_blank" style="text-decoration: none; color: inherit; margin: 0 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/8/82/Telegram_logo.svg" alt="Telegram" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
        </a>
        <a href="https://www.facebook.com/newyolkfarming" target="_blank" style="text-decoration: none; color: inherit; margin: 0 10px;">
            <img src="https://upload.wikimedia.org/wikipedia/commons/5/51/Facebook_f_logo_%282019%29.svg" alt="Facebook" style="width: 24px; height: 24px; vertical-align: middle; transition: transform 0.3s ease;">
        </a>
        <br>
        <br>
        by Tariq Al-Yaseen &copy; 2025-2026
    </div>
    <style>
        a img:hover {
            transform: scale(1.2);
        }
    </style>
    """,
    unsafe_allow_html=True
)
