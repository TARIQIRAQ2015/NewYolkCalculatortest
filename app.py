import streamlit as st
import pandas as pd
import plotly.express as px

# Format decimal numbers
def format_decimal(number):
    return f"{number:.10f}".rstrip('0').rstrip('.') if '.' in f"{number}" else f"{number}"

# Improve interface
st.set_page_config(page_title="Newyolk Chicken Calculator", page_icon="🐔", layout="wide")

# Language state (English, Romanian)
if "language" not in st.session_state:
    st.session_state.language = "English"

# Theme state (Dark or Light)
if "theme" not in st.session_state:
    st.session_state.theme = "Dark"

# Language selection in the sidebar
language = st.sidebar.selectbox("Choose Language / Alegeți limba", ["English", "Română"])

# Initial prices
if "egg_price" not in st.session_state:
    st.session_state.egg_price = 0.1155
if "feed_price" not in st.session_state:
    st.session_state.feed_price = 0.0189

# Field states (for reset)
if "eggs" not in st.session_state:
    st.session_state.eggs = ""
if "days" not in st.session_state:
    st.session_state.days = ""
if "rewards" not in st.session_state:
    st.session_state.rewards = ""
if "food" not in st.session_state:
    st.session_state.food = ""

# Change text direction based on language
if language == "English":
    st.markdown(
        f"""
        <style>
        body {{
            background: {'#ffffff' if st.session_state.theme == "Light" else 'linear-gradient(to right, #4B0082, #8A2BE2)'};
            color: {'black' if st.session_state.theme == "Light" else 'white'};
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
        .ltr {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stSelectbox, .stTextInput {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stButton button {{
            font-size: 24px;
        }}
        .stTable {{
            margin: 0 auto; /* Center the table */
            width: 50%; /* Set table width */
            text-align: left; /* Align text to the left */
        }}
        .scroll-top {{
            display: none;
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99;
            font-size: 18px;
            border: none;
            outline: none;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            padding: 15px;
            border-radius: 50%;
        }}
        .scroll-top:hover {{
            background-color: #45a049;
        }}
        </style>
        <div class="title">🐔 Newyolk - Chicken Calculator</div>
        <div class="subtitle">Calculate Chicken Profits and Daily Rewards</div>
        """,
        unsafe_allow_html=True
    )
else:  # Romanian language
    st.markdown(
        f"""
        <style>
        body {{
            background: {'#ffffff' if st.session_state.theme == "Light" else 'linear-gradient(to right, #4B0082, #8A2BE2)'};
            color: {'black' if st.session_state.theme == "Light" else 'white'};
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
        .ltr {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stSelectbox, .stTextInput {{
            direction: ltr;
            text-align: left;
            font-size: 24px;
            color: {'black' if st.session_state.theme == "Light" else 'white'};
        }}
        .stButton button {{
            font-size: 24px;
        }}
        .stTable {{
            margin: 0 auto; /* Center the table */
            width: 50%; /* Set table width */
            text-align: left; /* Align text to the left */
        }}
        .scroll-top {{
            display: none;
            position: fixed;
            bottom: 20px;
            right: 20px;
            z-index: 99;
            font-size: 18px;
            border: none;
            outline: none;
            background-color: #4CAF50;
            color: white;
            cursor: pointer;
            padding: 15px;
            border-radius: 50%;
        }}
        .scroll-top:hover {{
            background-color: #45a049;
        }}
        </style>
        <div class="title">🐔 Newyolk - Calculator de Pui</div>
        <div class="subtitle">Calculează Profiturile și Recompensele Zilnice</div>
        """,
        unsafe_allow_html=True
    )

# Scroll to top button
st.markdown(
    """
    <button onclick="scrollToTop()" class="scroll-top" id="scrollTopBtn" title="Go to top">↑</button>
    <script>
    // Show button when scrolling down
    window.onscroll = function() {scrollFunction()};
    function scrollFunction() {
        if (document.body.scrollTop > 20 || document.documentElement.scrollTop > 20) {
            document.getElementById("scrollTopBtn").style.display = "block";
        } else {
            document.getElementById("scrollTopBtn").style.display = "none";
        }
    }
    // Scroll to top
    function scrollToTop() {
        document.body.scrollTop = 0;
        document.documentElement.scrollTop = 0;
    }
    </script>
    """,
    unsafe_allow_html=True
)

# Use columns for better layout
col1, col2 = st.columns(2)

with col1:
    currency = st.selectbox(
        "💰 Currency" if language == "English" else "💰 Monedă",
        ["USD", "IQD"]
    )

with col2:
    calculation_type = st.selectbox(
        "📊 Calculation Type" if language == "English" else "📊 Tip de Calcul",
        ["Chicken Profits" if language == "English" else "Profituri Pui", "Daily Rewards and Food" if language == "English" else "Recompense Zilnice și Mâncare"]
    )

# Calculation section
if calculation_type == "Chicken Profits" or calculation_type == "Profituri Pui":
    st.subheader("📈 Chicken Profits Calculation" if language == "English" else "📈 Calcul Profituri Pui")
    col3, col4 = st.columns(2)

    with col3:
        eggs = st.text_input(
            "🥚 Number of Eggs" if language == "English" else "🥚 Numărul de Ouă",
            value=st.session_state.eggs,
            help="Enter the number of eggs (max 580)" if language == "English" else "Introduceți numărul de ouă (max 580)",
            key="eggs_input"
        )

    with col4:
        days = st.text_input(
            "📅 Number of Days" if language == "English" else "📅 Numărul de Zile",
            value=st.session_state.days,
            help="Enter the number of days (max 730)" if language == "English" else "Introduceți numărul de zile (max 730)",
            key="days_input"
        )

    if st.button("🧮 Calculate Chicken Profits" if language == "English" else "🧮 Calculează Profiturile Pui", type="primary"):
        try:
            eggs = float(eggs) if eggs else None
            days = float(days) if days else None

            if eggs is None or days is None:
                st.error("❗ Please enter all required values!" if language == "English" else "❗ Vă rugăm să introduceți toate valorile necesare!")
            elif eggs > 580:
                st.error("❗ Number of eggs must not exceed 580!" if language == "English" else "❗ Numărul de ouă nu trebuie să depășească 580!")
            elif days > 730:
                st.error("❗ Number of days must not exceed 730!" if language == "English" else "❗ Numărul de zile nu trebuie să depășească 730!")
            else:
                # Calculate results
                total_egg_price_usd = eggs * st.session_state.egg_price
                total_feed_cost_usd = (days * 2) * st.session_state.feed_price
                net_profit_before_rent_usd = total_egg_price_usd - total_feed_cost_usd

                # Calculate rent cost only if days >= 365
                rent_cost_usd = 6.0 if days >= 365 else 0.0
                net_profit_usd = net_profit_before_rent_usd - rent_cost_usd

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

                # Create results table
                results = {
                    "Item" if language == "English" else "Element": [
                        "💰 Total Egg Price" if language == "English" else "💰 Prețul Total al Ouălor",
                        "🌽 Total Feed Cost" if language == "English" else "🌽 Costul Total al Furajului",
                        "📊 Net Profit Before Rent" if language == "English" else "📊 Profit Net înainte de Chirii",
                        "🏠 Rent Cost for Second Year" if language == "English" else "🏠 Costul Chiriei pentru Anul Doi",
                        "💵 Net Profit" if language == "English" else "💵 Profit Net"
                    ],
                    "Value" if language == "English" else "Valoare": [
                        f"{format_decimal(total_egg_price)} {currency}",
                        f"{format_decimal(total_feed_cost)} {currency}",
                        f"{format_decimal(net_profit_before_rent)} {currency}",
                        f"{format_decimal(rent_cost)} {currency}",
                        f"{format_decimal(net_profit)} {currency}"
                    ]
                }

                # Display results as a table
                st.success("✅ Calculation completed successfully!" if language == "English" else "✅ Calcul finalizat cu succes!")
                df = pd.DataFrame(results)
                st.table(df)

                # Add a pie chart
                chart_data = pd.DataFrame({
                    "Category" if language == "English" else "Categorie": [
                        "Total Egg Price" if language == "English" else "Prețul Total al Ouălor",
                        "Total Feed Cost" if language == "English" else "Costul Total al Furajului",
                        "Rent Cost" if language == "English" else "Costul Chiriei"
                    ],
                    "Value" if language == "English" else "Valoare": [
                        total_egg_price,
                        total_feed_cost,
                        rent_cost
                    ]
                })

                fig = px.pie(chart_data, values="Value", names="Category",
                             title="Distribution of Costs and Profits" if language == "English" else "Distribuția Costurilor și Profiturilor",
                             color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig, use_container_width=True)

        except ValueError:
            st.error("❗ Please enter valid numbers!" if language == "English" else "❗ Vă rugăm să introduceți numere valide!")

elif calculation_type == "Daily Rewards and Food" or calculation_type == "Recompense Zilnice și Mâncare":
    st.subheader("📈 Daily Rewards and Food Calculation" if language == "English" else "📈 Calcul Recompense Zilnice și Mâncare")
    col5, col6 = st.columns(2)

    with col5:
        rewards = st.text_input(
            "🎁 Number of Rewards" if language == "English" else "🎁 Numărul de Recompense",
            value=st.session_state.rewards,
            help="Enter the number of rewards" if language == "English" else "Introduceți numărul de recompense",
            key="rewards_input"
        )

    with col6:
        food = st.text_input(
            "🌽 Amount of Food Required" if language == "English" else "🌽 Cantitatea de Mâncare Necesară",
            value=st.session_state.food,
            help="Enter the amount of food required" if language == "English" else "Introduceți cantitatea de mâncare necesară",
            key="food_input"
        )

    if st.button("🧮 Calculate Daily Rewards and Food" if language == "English" else "🧮 Calculează Recompense Zilnice și Mâncare", type="primary"):
        try:
            rewards = float(rewards) if rewards else None
            food = float(food) if food else None

            if rewards is None or food is None:
                st.error("❗ Please enter all required values!" if language == "English" else "❗ Vă rugăm să introduceți toate valorile necesare!")
            else:
                # Calculate results
                total_egg_price_usd = rewards * st.session_state.egg_price
                total_feed_cost_usd = food * st.session_state.feed_price
                net_profit_usd = total_egg_price_usd - total_feed_cost_usd

                if currency == "IQD":
                    total_egg_price = total_egg_price_usd * 1480
                    total_feed_cost = total_feed_cost_usd * 1480
                    net_profit = net_profit_usd * 1480
                else:
                    total_egg_price, total_feed_cost, net_profit = (
                        total_egg_price_usd, total_feed_cost_usd, net_profit_usd
                    )

                # Create results table
                results = {
                    "Item" if language == "English" else "Element": [
                        "💰 Total Egg Price" if language == "English" else "💰 Prețul Total al Ouălor",
                        "🌽 Total Feed Cost" if language == "English" else "🌽 Costul Total al Furajului",
                        "💵 Daily Profit" if language == "English" else "💵 Profit Zilnic"
                    ],
                    "Value" if language == "English" else "Valoare": [
                        f"{format_decimal(total_egg_price)} {currency}",
                        f"{format_decimal(total_feed_cost)} {currency}",
                        f"{format_decimal(net_profit)} {currency}"
                    ]
                }

                # Display results as a table
                st.success("✅ Calculation completed successfully!" if language == "English" else "✅ Calcul finalizat cu succes!")
                df = pd.DataFrame(results)
                st.table(df)

                # Add a pie chart
                chart_data = pd.DataFrame({
                    "Category" if language == "English" else "Categorie": [
                        "Total Egg Price" if language == "English" else "Prețul Total al Ouălor",
                        "Total Feed Cost" if language == "English" else "Costul Total al Furajului"
                    ],
                    "Value" if language == "English" else "Valoare": [
                        total_egg_price,
                        total_feed_cost
                    ]
                })

                fig = px.pie(chart_data, values="Value", names="Category",
                             title="Distribution of Costs and Profits" if language == "English" else "Distribuția Costurilor și Profiturilor",
                             color_discrete_sequence=px.colors.sequential.RdBu)
                st.plotly_chart(fig, use_container_width=True)

        except ValueError:
            st.error("❗ Please enter valid numbers!" if language == "English" else "❗ Vă rugăm să introduceți numere valide!")

# Price adjustment section
with st.expander("⚙️ Edit Prices" if language == "English" else "⚙️ Editează Prețuri"):
    st.subheader("⚙️ Edit Prices" if language == "English" else "⚙️ Editează Prețuri")
    new_egg_price = st.text_input("🥚 New Egg Price" if language == "English" else "🥚 Prețul Nou al Ouălor", value=str(st.session_state.egg_price))
    new_feed_price = st.text_input("🌽 New Feed Price" if language == "English" else "🌽 Prețul Nou al Furajului", value=str(st.session_state.feed_price))

    if st.button("💾 Save New Prices" if language == "English" else "💾 Salvează Prețurile Noi", type="secondary"):
        try:
            st.session_state.egg_price = float(new_egg_price)
            st.session_state.feed_price = float(new_feed_price)
            st.success("✅ New prices saved successfully!" if language == "English" else "✅ Prețurile noi au fost salvate cu succes!")
        except ValueError:
            st.error("❗ Please enter valid numbers!" if language == "English" else "❗ Vă rugăm să introduceți numere valide!")

# Reset button
if st.button("🔄 Reset" if language == "English" else "🔄 Resetează", type="secondary"):
    st.session_state.egg_price = 0.1155
    st.session_state.feed_price = 0.0189
    st.session_state.eggs = ""
    st.session_state.days = ""
    st.session_state.rewards = ""
    st.session_state.food = ""
    st.success("✅ Reset completed successfully!" if language == "English" else "✅ Resetare finalizată cu succes!")

# Add copyright text
st.markdown(
    """
    <div style="text-align: center; font-size: 16px; color: gray; margin-top: 50px; font-weight: bold;">
       © 2025 by Tariq Al-Yaseen. All rights reserved.
    </div>
    """,
    unsafe_allow_html=True
)
