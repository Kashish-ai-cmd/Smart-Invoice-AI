import streamlit as st
import pandas as pd
from PIL import Image
import os
import re
from datetime import datetime

from utils.gemini_extractor import extract_invoice_details
from utils.ml_model import predict_category  

st.set_page_config(page_title="Upload Bill | Smart Invoice AI", page_icon="📤", layout="wide")

# 🚨 THE THEME CLASH FIX 🚨
st.markdown("""
    <style>
    [data-testid="stSidebarNav"] {display: none !important;}
    /* Yahan se hardcoded dark background hata diya gaya hai */
    </style>
""", unsafe_allow_html=True)

st.sidebar.markdown("## ⚡ Smart Invoice AI")
st.sidebar.page_link("app.py", label="Home", icon="🏠")
st.sidebar.page_link("pages/upload_bill.py", label="Upload Bill", icon="📄")
st.sidebar.page_link("pages/dashboard.py", label="Dashboard", icon="📊")
st.sidebar.page_link("pages/analytics.py", label="Analytics", icon="📈")
st.sidebar.page_link("pages/reports.py", label="Reports", icon="📑")
st.sidebar.page_link("pages/settings.py", label="Settings", icon="⚙️")

# ----------------------------------------
# 🛠️ SMART NUMBER CLEANER & VALIDATION
# ----------------------------------------
def clean_number(value):
    try:
        nums = re.findall(r'\d+\.\d+|\d+', str(value).replace(',', ''))
        return float(nums[-1]) if nums else 0.0
    except:
        return 0.0

def validate_bill(amount, vendor):
    if amount <= 0:
        return False, "Amount cannot be zero or negative!"
    if len(vendor.strip()) < 3:
        return False, "Vendor name is too short/invalid!"
    return True, "Valid"

# ----------------------------------------
# MAIN UPLOAD PAGE
# ----------------------------------------
st.title("📤 Upload & Process Bills")
st.markdown("Upload your physical or digital invoices here.")

st.markdown("### Step 1: Select Bill Type")
bill_type = st.radio("Yeh bill kis cheez ka hai?", ["🔴 Expense (Maal Aaya / Karcha)", "🟢 Income (Maal Bika / Sale)"], horizontal=True)

st.markdown("### Step 2: Upload Image")
uploaded_file = st.file_uploader("Drop your bill image here (JPG, PNG)", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption="Uploaded Bill", width=450)
    
    if st.button("Process Bill with AI & ML 🧠", type="primary"):
        with st.spinner("AI is reading and ML is categorizing... Please wait."):
            extracted_data = extract_invoice_details(image)
            
            if "error" in extracted_data:
                st.error(f"❌ Failed to read bill: {extracted_data['error']}")
            else:
                st.success("✅ Bill processed successfully!")
                st.json(extracted_data) 
                
                try:
                    final_type = "Expense" if "Expense" in bill_type else "Income"
                    
                    shop_details = extracted_data.get("Shop Details", {})
                    bill_info = extracted_data.get("Bill Info", {})
                    financials = extracted_data.get("Financials", {})
                    
                    items_list = extracted_data.get("Items List", extracted_data.get("All Items", []))
                    item_names = ", ".join([str(item.get("Item Name", item.get("Particulars", ""))) for item in items_list])
                    
                    vendor = shop_details.get("Vendor Name", extracted_data.get("Vendor Name", "Unknown"))
                    
                    # ML CATEGORIZATION
                    predicted_cat = predict_category(vendor, item_names)
                    
                    # CLEANING TAX AND AMOUNT
                    raw_tax = financials.get("Tax Amount", extracted_data.get("Tax Amount", "0"))
                    raw_amount = financials.get("Total Amount", extracted_data.get("Total Amount", "0"))
                    
                    clean_tax = clean_number(raw_tax)
                    clean_amount = clean_number(raw_amount)
                    
                    # 🚀 VALIDATION STEP (Prevents Fraud/Negative Bills)
                    is_valid, msg = validate_bill(clean_amount, vendor)
                    
                    if not is_valid:
                        st.error(f"❌ Data Validation Failed: {msg}")
                    else:
                        new_row = pd.DataFrame([{
                            "Date": bill_info.get("Date", extracted_data.get("Date", datetime.today().strftime('%Y-%m-%d'))),
                            "Invoice No": bill_info.get("Invoice Number", bill_info.get("Bill No", "")),
                            "Vendor Name": vendor,
                            "GSTIN": shop_details.get("GSTIN", extracted_data.get("GSTIN", "")),
                            "Phone": shop_details.get("Phone Numbers", ""),
                            "Items Detail": item_names,
                            "Tax": clean_tax, 
                            "Amount": clean_amount,
                            "Type": final_type,
                            "Category": predicted_cat,
                            "Payment Status": "Pending 🔴"
                        }])
                        
                        csv_path = os.path.join("data", "bills.csv")
                        
                        if not os.path.exists(csv_path):
                            new_row.to_csv(csv_path, index=False)
                        else:
                            new_row.to_csv(csv_path, mode='a', header=False, index=False)
                            
                        st.info(f"💾 AI categorized this as **{predicted_cat}** and saved ₹{clean_tax} Tax successfully!")
                    
                except Exception as e:
                    st.error(f"Error saving to database: {e}")