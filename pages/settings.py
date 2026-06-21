import streamlit as st
import os

st.set_page_config(page_title="Settings | Smart Invoice AI", page_icon="⚙️", layout="wide")

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

csv_path = os.path.join("data", "bills.csv")

st.title("⚙️ Application Settings")
st.markdown("Manage your database preferences here.")

st.info("🔒 Your API key is securely managed via environment variables (.env) and is not exposed in the UI.")
st.markdown("---")

st.markdown("### ⚠️ Danger Zone")
st.caption("Be careful! These actions cannot be undone.")

if st.button("🗑️ Clear Entire Database (Delete bills.csv)"):
    if os.path.exists(csv_path):
        os.remove(csv_path)
        st.success("✅ Database has been completely cleared. You can start fresh now.")
    else:
        st.warning("Database is already empty. Nothing to delete.")