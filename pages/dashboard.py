import streamlit as st
import pandas as pd
import os
from datetime import datetime

st.set_page_config(page_title="Dashboard | Smart Invoice AI", page_icon="📊", layout="wide")

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
# MAIN DASHBOARD CONTENT
# ==========================================
st.title("📊 Advanced Financial Dashboard")
st.markdown("Filter your data and monitor AI-detected risks.")

csv_path = os.path.join("data", "bills.csv")

try:
    if os.path.exists(csv_path):
        df = pd.read_csv(csv_path)
        
        # ----------------------------------------
        # DATA CLEANING 
        # ----------------------------------------
        if 'Type' not in df.columns:
            df['Type'] = 'Expense'
            
        df['Amount'] = pd.to_numeric(df['Amount'], errors='coerce').fillna(0)
        
        if 'Tax' in df.columns:
            df['Tax'] = pd.to_numeric(df['Tax'], errors='coerce').fillna(0)
            
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')

        for col in ['Invoice No', 'Phone', 'GSTIN', 'Category']:
            if col in df.columns:
                df[col] = df[col].astype(str).replace('nan', '').replace('0.0', '')

        # ---------------------------------------------------------
        # 🧠 HYBRID OUTLIER ENGINE (Hard Limits + Statistical)
        # ---------------------------------------------------------
        # Step 1: Pre-trained Maximum Limits (Aukaat) for each category
        CATEGORY_THRESHOLDS = {
            "Textile Wholesale & Manufacturing": 1500000, # 15 Lakh (Normal for wholesale)
            "Hardware & Plumbing": 500000,                # 5 Lakh
            "Logistics & Transport": 100000,              # 1 Lakh
            "Office Pantry": 15000,                       # 15 Hazar (Snacks ke liye max)
            "Travel & Fuel": 50000,                       # 50 Hazar
            "IT & Software": 200000,                      # 2 Lakh
            "Utility Bills": 100000,                      # 1 Lakh (Commercial bijli)
            "Stationery & Printing": 20000,               # 20 Hazar
            "Electronics & IT Assets": 300000,            # 3 Lakh (Laptops, ACs)
            "Legal & Professional": 200000,               # 2 Lakh (CA / Lawyer Fees)
            "Maintenance & Repairs": 50000,               # 50 Hazar
            "Food & Dining": 20000,                       # 20 Hazar (Client Meeting)
            "General Expense": 50000                      # Fallback
        }

        df['Risk Flag'] = "✅ Normal"
        
        if len(df) > 0:
            # Rule 1: Check Hard Limits (Fraud Alert)
            for idx in df.index:
                cat = df.loc[idx, 'Category']
                amt = df.loc[idx, 'Amount']
                max_limit = CATEGORY_THRESHOLDS.get(cat, 50000)
                
                if amt > max_limit:
                    df.loc[idx, 'Risk Flag'] = "🚩 Fraud / Over Limit"

            # Rule 2: Check Statistical Anomalies (Agar limits ke andar hai par ajeeb hai)
            for category, group in df.groupby('Category'):
                if len(group) >= 3: # Pattern pakadne ke liye kam se kam 3 bills chahiye
                    mean_val = group['Amount'].mean()
                    std_val = group['Amount'].std()
                    
                    if pd.isna(std_val) or std_val == 0:
                        std_val = mean_val * 0.2 
                        
                    # 2 Standard Deviation rule
                    stat_threshold = mean_val + (2 * std_val)
                    max_limit = CATEGORY_THRESHOLDS.get(category, 50000)
                    
                    # Chhote amounts ko ignore karne ke liye Base Minimum
                    # (e.g. Pantry limit 15k hai, toh 3k ke bill ko outlier mat bolo)
                    min_base = max_limit * 0.25 
                    
                    for idx in group.index:
                        amt = df.loc[idx, 'Amount']
                        # Agar Fraud ka thappa nahi laga hai, tabhi check karo
                        if df.loc[idx, 'Risk Flag'] == "✅ Normal":
                            if amt > stat_threshold and amt > min_base:
                                df.loc[idx, 'Risk Flag'] = "⚠️ Unusual Spike"
                            
        # ----------------------------------------
        # DYNAMIC FILTERS
        # ----------------------------------------
        st.sidebar.markdown("### 🔍 Smart Filters")
        
        min_date = df['Date'].min().date() if not df['Date'].isnull().all() else datetime.today().date()
        max_date = df['Date'].max().date() if not df['Date'].isnull().all() else datetime.today().date()
        
        date_selection = st.sidebar.date_input("Select Timeline", value=(min_date, max_date), min_value=min_date, max_value=max_date)

        types = st.sidebar.multiselect("Bill Type", df['Type'].dropna().unique(), default=df['Type'].dropna().unique())
        vendors = st.sidebar.multiselect("Select Firm / Vendor", df['Vendor Name'].dropna().unique(), default=df['Vendor Name'].dropna().unique())
        
        if len(date_selection) == 2:
            start_date, end_date = date_selection
            date_condition = (df['Date'].dt.date >= start_date) & (df['Date'].dt.date <= end_date)
        else:
            start_date = date_selection[0]
            date_condition = (df['Date'].dt.date == start_date)

        filtered_df = df[(df['Type'].isin(types)) & (df['Vendor Name'].isin(vendors)) & date_condition]

        display_df = filtered_df.copy()
        display_df['Date'] = display_df['Date'].dt.strftime('%Y-%m-%d')

        # ----------------------------------------
        # KPI CARDS
        # ----------------------------------------
        col1, col2, col3, col4 = st.columns(4)
        
        total_income = filtered_df[filtered_df['Type'] == 'Income']['Amount'].sum()
        total_expense = filtered_df[filtered_df['Type'] == 'Expense']['Amount'].sum()
        net_balance = total_income - total_expense
        total_tax = filtered_df['Tax'].sum() if 'Tax' in filtered_df.columns else 0

        col1.metric("🟢 Total Income", f"₹ {total_income:,.2f}")
        col2.metric("🔴 Total Expense", f"₹ {total_expense:,.2f}")
        col3.metric("💰 Net Balance", f"₹ {net_balance:,.2f}")
        col4.metric("🏛️ Total Tax (GST)", f"₹ {total_tax:,.2f}") 

        st.markdown("---")

        # ----------------------------------------
        # EDITABLE DATA TABLE
        # ----------------------------------------
        st.markdown("### 🧾 Interactive Database")
        
        edited_df = st.data_editor(
            display_df,
            use_container_width=True,
            hide_index=True,
            height=400,
            column_order=("Risk Flag", "Date", "Invoice No", "Vendor Name", "Items Detail", "Tax", "Amount", "Category", "Payment Status"),
            column_config={
                "Risk Flag": st.column_config.TextColumn("AI Analysis", width="medium"),
                "Payment Status": st.column_config.SelectboxColumn("Status", width="medium", options=["Pending 🔴", "Cleared 🟢"]),
                "Items Detail": st.column_config.TextColumn("Items Purchased", width="large"),
                "Amount": st.column_config.NumberColumn("Total (₹)", format="%.2f"),
                "Tax": st.column_config.NumberColumn("Tax (₹)", format="%.2f")
            }
        )

        # ----------------------------------------
        # SAVE BUTTON
        # ----------------------------------------
        if st.button("💾 Save Changes to Database", type="primary"):
            if 'Risk Flag' in edited_df.columns:
                edited_df = edited_df.drop(columns=['Risk Flag'])
                
            df.update(edited_df)
            df.to_csv(csv_path, index=False)
            st.success("✅ Data successfully updated!")
            st.rerun() 
            
    else:
        st.warning("No data found! Please upload a bill first from the Upload page.")

except Exception as e:
    st.error(f"Error loading dashboard: {e}")