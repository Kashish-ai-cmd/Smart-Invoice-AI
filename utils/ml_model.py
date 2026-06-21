from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import make_pipeline

# ==========================================
# PERFECTLY BALANCED TRAINING DATASET
# ==========================================
TRAIN_DATA = [
    # 1. Textile Wholesale & Manufacturing
    ("SURAT FABRICS", "Cotton Thaan, Silk Rolls, Fabric, Premium Cotton", "Textile Wholesale & Manufacturing"),
    ("RAYMOND", "Premium Suiting, Shirting Material", "Textile Wholesale & Manufacturing"),
    
    # 2. IT & Software
    ("SMART AI SOLUTIONS", "Software Development, Cloud Server Setup, IT, Web", "IT & Software"),
    ("AMAZON WEB SERVICES", "Cloud Hosting, Database, Server", "IT & Software"),
    
    # 3. Hardware & Plumbing
    ("SUPREME PIPES", "PVC Pipes, Water Tanks, Hardware, Plumbing", "Hardware & Plumbing"),
    
    # 4. Electronics & IT Assets
    ("CROMA ELECTRONICS", "Dell XPS Laptop, Wireless Mouse, Electronics", "Electronics & IT Assets"),
    
    # 5. Office Pantry
    ("LOCAL KIRANA MART", "Tea, Coffee, Snacks, Biscuits, Cold Drinks bulk", "Office Pantry"),
    ("RELIANCE SMART", "Milk packets, Sugar, Tea powder, Groceries", "Office Pantry"),
    
    # 6. Stationery & Printing
    ("CLASSMATE DEPOT", "A4 Paper Rims, Premium Parker Pens, Registers", "Stationery & Printing"),
    
    # 7. Travel & Fuel
    ("MAKEMYTRIP", "Flight Ticket, Travel, Cab, Hotel", "Travel & Fuel"),
    
    # 8. Utility Bills
    ("UPPCL ELECTRICITY BOARD", "Commercial Power Bill, Electricity, Units", "Utility Bills"),
    
    # 9. Legal & Professional
    ("MISHRA & ASSOCIATES CA", "Annual Audit Fees, GST Filing Charges", "Legal & Professional"),
    
    # 10. Logistics & Transport
    ("BVC LOGISTICS", "Transport, Shipping, Courier", "Logistics & Transport")
]

def predict_category(vendor_name, items_detail):
    try:
        X_train = [f"{row[0]} {row[1]}" for row in TRAIN_DATA]
        y_train = [row[2] for row in TRAIN_DATA]

        # Model pipeline with English stop words removed
        model = make_pipeline(TfidfVectorizer(stop_words='english'), MultinomialNB())
        model.fit(X_train, y_train)

        input_text = f"{vendor_name} {items_detail}"
        prediction = model.predict([input_text])

        return prediction[0]
    except Exception as e:
        print(f"ML Error: {e}")
        return "General Expense"