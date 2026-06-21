import streamlit as st
import pandas as pd
import plotly.express as px
import os

st.set_page_config(page_title="Analytics | Smart Invoice AI", page_icon="📈", layout="wide")

# ==========================================
# CUSTOM PRO-SIDEBAR & THEME
# ==========================================
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none !important;}
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## ⚡ Smart Invoice AI")
st.sidebar.page_link("app.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/upload_bill.py", label="Upload Bill", icon="📄")
st.sidebar.page_link("pages/dashboard.py", label="Dashboard", icon="📊")
st.sidebar.page_link("pages/analytics.py", label="Analytics", icon="📈")
st.sidebar.page_link("pages/reports.py", label="Reports", icon="📑")
st.sidebar.page_link("pages/settings.py", label="Settings", icon="⚙️")
st.sidebar.divider()

# ==========================================
# MAIN ANALYTICS CONTENT
# ==========================================
# ... (Upar ka sidebar code same rahega) ...

# ==========================================
# MAIN ANALYTICS CONTENT
# ==========================================
st.title("📈 Business Analytics")
st.markdown("Visualize your income, expenses, and overall profit/loss trends.")

csv_path = os.path.join("data", "bills.csv")

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)
    
    # ----------------------------------------
    # THE BUG FIXER (Data Cleaning)
    # ----------------------------------------
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
    
    if 'Type' not in df.columns:
        df['Type'] = 'Expense'
        
    # FIX 1: Agar purane bills mein Payment Status nahi hai, toh default dal do
    if 'Payment Status' not in df.columns:
        df['Payment Status'] = 'Pending 🔴'

    # ----------------------------------------
    # TIME FILTER (Day / Month / Year)
    # ----------------------------------------
    st.markdown("### ⏳ Select Trend Timeline")
    time_view = st.radio("View Data By:", ["Daily", "Monthly", "Yearly"], horizontal=True)

    if time_view == "Daily":
        df['Time'] = df['Date'].dt.strftime('%Y-%m-%d')
    elif time_view == "Monthly":
        df['Time'] = df['Date'].dt.strftime('%Y-%m')
    else:
        df['Time'] = df['Date'].dt.strftime('%Y')

    # ----------------------------------------
    # CHART 1: MAIN BAR CHART (Income vs Expense)
    # ----------------------------------------
    st.markdown("---")
    st.markdown(f"### 📊 Income vs Expense Trend ({time_view})")
    
    trend_data = df.groupby(['Time', 'Type'])['Amount'].sum().reset_index()
    
    if not trend_data.empty:
        fig_trend = px.bar(
            trend_data, 
            x='Time', 
            y='Amount', 
            color='Type', 
            barmode='group',
            color_discrete_map={'Income': '#00C853', 'Expense': '#D50000'}
        )
        # FIX 2: Plotly ko batao ki Time ko as it is dikhaye, ajeeb numbers na banaye
        fig_trend.update_xaxes(type='category') 
        st.plotly_chart(fig_trend, use_container_width=True)
    else:
        st.info("Not enough data to show trends.")

    # ----------------------------------------
    # CHART 2 & 3: PIE CHARTS (Category & Status)
    # ----------------------------------------
    st.markdown("---")
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("### 🍩 Where is the money going?")
        st.caption("Expense breakdown by Firm/Vendor")
        expense_df = df[df['Type'] == 'Expense']
        
        if not expense_df.empty:
            cat_data = expense_df.groupby('Vendor Name')['Amount'].sum().reset_index()
            fig_pie = px.pie(cat_data, values='Amount', names='Vendor Name', hole=0.4)
            st.plotly_chart(fig_pie, use_container_width=True)
        else:
            st.info("No expense data available.")

    with col2:
        st.markdown("### 🏦 Payment Status Overview")
        st.caption("Pending vs Cleared Dues")
        
        status_data = df.groupby('Payment Status')['Amount'].sum().reset_index()
        fig_status = px.pie(
            status_data, 
            values='Amount', 
            names='Payment Status', 
            color='Payment Status',
            color_discrete_map={'Pending 🔴': '#FF5252', 'Cleared 🟢': '#4CAF50'}
        )
        st.plotly_chart(fig_status, use_container_width=True)

else:
    st.warning("No data found! Please upload some bills from the Upload page to see analytics.")