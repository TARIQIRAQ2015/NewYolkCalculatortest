import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime, timedelta
import sqlite3
import bcrypt
import json
import os
from pathlib import Path

# إعداد الإعدادات الأولية للتطبيق
st.set_page_config(
    page_title="New Yolk Calculator | حاسبة نيويولك",
    page_icon="🐔",
    layout="wide",
    initial_sidebar_state="expanded"
)

# تهيئة قاعدة البيانات وإنشاء الجداول
def init_db():
    conn = sqlite3.connect('newyolk.db')
    c = conn.cursor()
    
    # جدول المستخدمين
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  username TEXT UNIQUE NOT NULL,
                  password TEXT NOT NULL,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
    
    # جدول الحسابات المحفوظة
    c.execute('''CREATE TABLE IF NOT EXISTS calculations
                 (id INTEGER PRIMARY KEY AUTOINCREMENT,
                  user_id INTEGER,
                  calculation_data TEXT,
                  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                  FOREIGN KEY (user_id) REFERENCES users(id))''')
    
    conn.commit()
    conn.close()

# دوال المصادقة
def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def verify_password(password, hashed):
    return bcrypt.checkpw(password.encode(), hashed)

def format_number(number, decimals=2):
    """تنسيق الأرقام بشكل جميل"""
    try:
        return f"{float(number):,.{decimals}f}"
    except (ValueError, TypeError):
        return "0.00"

# تهيئة قاعدة البيانات
init_db()

# تعريف الألوان والأنماط
COLORS = {
    'primary': '#1e88e5',
    'secondary': '#00b0ff',
    'success': '#00c853',
    'error': '#ff1744',
    'warning': '#ffd600'
}

# تحسين المظهر العام
st.markdown("""
<style>
    /* الخلفية والمظهر العام */
    .stApp {
        background: linear-gradient(135deg, #1e3c72, #2a5298);
        color: white;
    }
    
    /* تحسين الأزرار */
    .stButton > button {
        width: 100%;
        padding: 0.75rem !important;
        background: linear-gradient(45deg, #2196F3, #1976D2) !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 1.1rem !important;
        font-weight: 500 !important;
        transition: all 0.3s ease !important;
        box-shadow: 0 4px 6px rgba(0,0,0,0.1) !important;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 12px rgba(0,0,0,0.15) !important;
    }
    
    /* تحسين مربعات الإدخال */
    .stTextInput > div > div {
        background: rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
        border: 1px solid rgba(255,255,255,0.2) !important;
        color: white !important;
        transition: all 0.3s ease;
    }
    
    .stTextInput > div > div:hover {
        border-color: rgba(255,255,255,0.4) !important;
        background: rgba(255,255,255,0.15) !important;
    }
    
    /* تحسين التبويبات */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background-color: rgba(255,255,255,0.1);
        padding: 10px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: transparent !important;
        color: white !important;
        border-radius: 8px !important;
        padding: 10px 20px !important;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background-color: rgba(255,255,255,0.1) !important;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: rgba(255,255,255,0.2) !important;
    }
    
    /* تحسين الرسائل */
    .stAlert {
        background-color: rgba(255,255,255,0.1) !important;
        border: none !important;
        border-radius: 10px !important;
    }
    
    /* تحسين القوائم المنسدلة */
    .stSelectbox > div > div {
        background: rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
    }
    
    /* تحسين العناوين */
    h1, h2, h3 {
        color: white !important;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    /* تحسين الجداول */
    .dataframe {
        background: rgba(255,255,255,0.1) !important;
        border-radius: 10px !important;
    }
    
    /* إخفاء العناصر غير الضرورية */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# إدارة حالة الجلسة
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['user_id'] = None
    st.session_state['username'] = None
    st.session_state['language'] = 'ar'
    st.session_state['currency'] = 'IQD'
    st.session_state['theme'] = 'dark'

def save_calculation(user_id, data):
    """حفظ الحسابات للمستخدم"""
    conn = sqlite3.connect('newyolk.db')
    c = conn.cursor()
    c.execute("INSERT INTO calculations (user_id, calculation_data) VALUES (?, ?)",
             (user_id, json.dumps(data)))
    conn.commit()
    conn.close()

def get_user_calculations(user_id):
    """استرجاع حسابات المستخدم"""
    conn = sqlite3.connect('newyolk.db')
    c = conn.cursor()
    c.execute("SELECT calculation_data, created_at FROM calculations WHERE user_id = ? ORDER BY created_at DESC", (user_id,))
    results = c.fetchall()
    conn.close()
    return [(json.loads(data), created_at) for data, created_at in results]

def login_user(username, password):
    """تسجيل دخول المستخدم"""
    conn = sqlite3.connect('newyolk.db')
    c = conn.cursor()
    c.execute("SELECT id, password FROM users WHERE username = ?", (username,))
    result = c.fetchone()
    conn.close()
    
    if result and verify_password(password, result[1]):
        st.session_state['logged_in'] = True
        st.session_state['user_id'] = result[0]
        st.session_state['username'] = username
        return True
    return False

def register_user(username, password):
    """تسجيل مستخدم جديد"""
    if not username or not password:
        return False, "الرجاء إدخال اسم المستخدم وكلمة المرور"
    
    conn = sqlite3.connect('newyolk.db')
    c = conn.cursor()
    try:
        hashed = hash_password(password)
        c.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, hashed))
        conn.commit()
        return True, "تم إنشاء الحساب بنجاح!"
    except sqlite3.IntegrityError:
        return False, "اسم المستخدم موجود مسبقاً"
    finally:
        conn.close()

def calculate_profits(chickens, feed_price, egg_price, days):
    """حساب الأرباح"""
    total_feed = chickens * 0.12 * days  # 120 جرام لكل دجاجة يومياً
    total_eggs = chickens * 0.8 * days   # 80% نسبة إنتاج البيض
    
    total_feed_cost = total_feed * feed_price
    total_egg_revenue = total_eggs * egg_price
    
    return {
        'total_feed': total_feed,
        'total_eggs': total_eggs,
        'total_feed_cost': total_feed_cost,
        'total_egg_revenue': total_egg_revenue,
        'net_profit': total_egg_revenue - total_feed_cost
    }

# واجهة المستخدم
if not st.session_state['logged_in']:
    col1, col2, col3 = st.columns([1,2,1])
    with col2:
        st.title("حاسبة نيويولك 🐔")
        st.markdown("##### الحاسبة الأفضل لمشاريع الدواجن")
        
        tab1, tab2 = st.tabs(["✨ تسجيل الدخول", "📝 حساب جديد"])
        
        with tab1:
            with st.form("login_form"):
                username = st.text_input("اسم المستخدم")
                password = st.text_input("كلمة المرور", type="password")
                submit = st.form_submit_button("تسجيل الدخول")
                
                if submit:
                    if login_user(username, password):
                        st.success("تم تسجيل الدخول بنجاح!")
                        st.rerun()
                    else:
                        st.error("خطأ في اسم المستخدم أو كلمة المرور")
        
        with tab2:
            with st.form("register_form"):
                new_username = st.text_input("اسم المستخدم الجديد")
                new_password = st.text_input("كلمة المرور الجديدة", type="password")
                confirm_password = st.text_input("تأكيد كلمة المرور", type="password")
                submit = st.form_submit_button("إنشاء حساب")
                
                if submit:
                    if new_password != confirm_password:
                        st.error("كلمات المرور غير متطابقة")
                    else:
                        success, message = register_user(new_username, new_password)
                        if success:
                            st.success(message)
                        else:
                            st.error(message)

else:
    # الشريط الجانبي
    with st.sidebar:
        st.write(f"👋 مرحباً، {st.session_state['username']}")
        st.divider()
        
        menu = st.radio(
            "القائمة الرئيسية",
            ["🏠 الرئيسية", "📊 حساب جديد", "📋 الحسابات السابقة", "⚙️ الإعدادات"]
        )
        
        st.divider()
        if st.button("تسجيل الخروج", key="logout"):
            st.session_state['logged_in'] = False
            st.session_state['user_id'] = None
            st.session_state['username'] = None
            st.rerun()
    
    if menu == "🏠 الرئيسية":
        st.title("لوحة التحكم الرئيسية 🐔")
        
        # إحصائيات سريعة
        col1, col2, col3 = st.columns(3)
        calculations = get_user_calculations(st.session_state['user_id'])
        
        with col1:
            st.metric("عدد الحسابات", len(calculations))
        with col2:
            if calculations:
                latest = json.loads(calculations[0][0])
                st.metric("آخر حساب للأرباح", f"{format_number(latest.get('net_profit', 0))} {st.session_state['currency']}")
        with col3:
            if calculations:
                total_profit = sum(json.loads(calc[0]).get('net_profit', 0) for calc in calculations)
                st.metric("إجمالي الأرباح المحسوبة", f"{format_number(total_profit)} {st.session_state['currency']}")
    
    elif menu == "📊 حساب جديد":
        st.title("حساب جديد 📊")
        
        with st.form("calculation_form"):
            col1, col2 = st.columns(2)
            
            with col1:
                chickens = st.number_input("عدد الدجاج", min_value=1, value=100)
                feed_price = st.number_input("سعر الكيلو من العلف", min_value=0.0, value=1.0)
            
            with col2:
                egg_price = st.number_input("سعر البيضة", min_value=0.0, value=0.25)
                days = st.number_input("عدد الأيام", min_value=1, value=30)
            
            submit = st.form_submit_button("حساب الأرباح")
            
            if submit:
                results = calculate_profits(chickens, feed_price, egg_price, days)
                save_calculation(st.session_state['user_id'], results)
                
                st.success("تم حساب النتائج بنجاح!")
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("إجمالي العلف المستهلك", f"{format_number(results['total_feed'])} كجم")
                    st.metric("إجمالي تكلفة العلف", f"{format_number(results['total_feed_cost'])} {st.session_state['currency']}")
                
                with col2:
                    st.metric("إجمالي البيض المنتج", f"{format_number(results['total_eggs'])} بيضة")
                    st.metric("صافي الربح", f"{format_number(results['net_profit'])} {st.session_state['currency']}")
                
                # رسم بياني للنتائج
                fig = px.pie(
                    values=[results['total_feed_cost'], results['total_egg_revenue']],
                    names=['تكاليف العلف', 'إيرادات البيض'],
                    title='تحليل التكاليف والإيرادات'
                )
                st.plotly_chart(fig, use_container_width=True)
    
    elif menu == "📋 الحسابات السابقة":
        st.title("الحسابات السابقة 📋")
        
        calculations = get_user_calculations(st.session_state['user_id'])
        if calculations:
            for data, date in calculations:
                with st.expander(f"حساب بتاريخ {date}"):
                    col1, col2 = st.columns(2)
                    with col1:
                        st.metric("إجمالي العلف المستهلك", f"{format_number(data['total_feed'])} كجم")
                        st.metric("إجمالي تكلفة العلف", f"{format_number(data['total_feed_cost'])} {st.session_state['currency']}")
                    
                    with col2:
                        st.metric("إجمالي البيض المنتج", f"{format_number(data['total_eggs'])} بيضة")
                        st.metric("صافي الربح", f"{format_number(data['net_profit'])} {st.session_state['currency']}")
        else:
            st.info("لا توجد حسابات سابقة")
    
    elif menu == "⚙️ الإعدادات":
        st.title("الإعدادات ⚙️")
        
        currency = st.selectbox(
            "العملة",
            options=['IQD', 'USD', 'EUR', 'SAR', 'AED'],
            index=['IQD', 'USD', 'EUR', 'SAR', 'AED'].index(st.session_state['currency'])
        )
        
        if currency != st.session_state['currency']:
            st.session_state['currency'] = currency
            st.success("تم تحديث العملة بنجاح!")
