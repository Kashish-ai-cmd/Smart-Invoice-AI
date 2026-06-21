import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Reports | Smart Invoice AI", page_icon="📑", layout="wide")

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
# MAIN REPORTS CONTENT
# ==========================================
st.title("📑 Generate CA Reports")
st.markdown("Export your business data in a clean, CA-ready format.")

csv_path = os.path.join("data", "bills.csv")

if os.path.exists(csv_path):
    df = pd.read_csv(csv_path)

    st.markdown("### 📋 Data Preview")
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.markdown("### 📥 Download Report")
    st.info("💡 Click the button below to download the complete database. Your CA can open this directly in Microsoft Excel.")

    # Data ko CSV format mein convert karna download ke liye
    csv_data = df.to_csv(index=False).encode('utf-8')

    # Streamlit ka magic download button
    st.download_button(
        label="📊 Download Data for CA (.csv)",
        data=csv_data,
        file_name="Smart_Invoice_Report.csv",
        mime="text/csv",
        type="primary"
    )
else:
    st.warning("No data found! Upload some bills from the Upload page to generate a report.")