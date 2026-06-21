import streamlit as st

# ==========================================
# PAGE CONFIGURATION
# ==========================================
st.set_page_config(
    page_title="Smart Invoice AI", 
    page_icon="🚀", 
    layout="wide", 
    initial_sidebar_state="collapsed"
)

# ==========================================
# ADVANCED CSS OVERRIDES
# ==========================================
st.markdown("""
    <style>
    /* 1. Hide the default sidebar on the landing page for a true website look */
    [data-testid="stSidebar"] { display: none !important; }
    [data-testid="collapsedControl"] { display: none !important; }
    header { visibility: hidden !important; }
    
    /* 2. Custom Purple Gradient Button (Overriding Streamlit Default) */
    div.stButton > button {
        background: linear-gradient(90deg, #6366F1 0%, #A855F7 100%) !important;
        color: white !important;
        border: none !important;
        border-radius: 30px !important;
        padding: 10px 25px !important;
        font-size: 1.2rem !important;
        font-weight: 600 !important;
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.4) !important;
        transition: all 0.3s ease !important;
        display: block;
        margin-top: 10px;
    }
    div.stButton > button:hover {
        transform: scale(1.05) !important;
        box-shadow: 0 6px 20px rgba(168, 85, 247, 0.6) !important;
    }
    
    /* 3. Sleek Dynamic Feature Cards */
    .feature-box {
        background-color: var(--secondary-background-color); /* Auto-adapts to Light/Dark */
        padding: 25px 20px;
        border-radius: 16px;
        border: 1px solid var(--primary-color);
        text-align: center;
        transition: transform 0.3s ease, box-shadow 0.3s ease;
    }
    .feature-box:hover {
        transform: translateY(-5px);
        box-shadow: 0 4px 15px rgba(168, 85, 247, 0.2);
    }
    .feature-title { color: var(--text-color); font-weight: 600; font-size: 1.1rem; margin-top: 15px; margin-bottom: 5px; }
    .feature-desc { color: var(--text-color); opacity: 0.8; font-size: 0.9rem; margin-bottom: 0px; }
    </style>
""", unsafe_allow_html=True)

# ==========================================
# HERO SECTION (Dynamic Text Colors)
# ==========================================
col1, col2 = st.columns([1.2, 1], gap="large")

with col1:
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown('<p style="color: var(--text-color); font-size: 2.2rem; font-weight: 700; margin-bottom: -20px; font-family: sans-serif;">Welcome to</p>', unsafe_allow_html=True)
    st.markdown('<h1 style="font-size: 4.5rem; font-weight: 900; background: -webkit-linear-gradient(45deg, #818CF8, #C084FC); -webkit-background-clip: text; -webkit-text-fill-color: transparent; margin-bottom: 10px; line-height: 1.1; font-family: sans-serif;">Smart Invoice AI</h1>', unsafe_allow_html=True)
    st.markdown('<p style="color: var(--text-color); opacity: 0.8; font-size: 1.15rem; line-height: 1.6; margin-bottom: 30px; font-family: sans-serif;">Say goodbye to manual data entry. Let advanced Artificial Intelligence extract, categorize, and analyze your business bills in seconds.</p>', unsafe_allow_html=True)
    
    # Navigation Button
    if st.button("Manage Your Bills ➔", key="hero_btn"):
        st.switch_page("pages/upload_bill.py")

with col2:
    st.image("https://images.unsplash.com/photo-1551288049-bebda4e38f71?auto=format&fit=crop&q=80&w=1000", use_container_width=True)

st.markdown("<br><br><br>", unsafe_allow_html=True)

# ==========================================
# FEATURES SECTION
# ==========================================
c1, c2, c3, c4 = st.columns(4)

features = [
    ("📄", "AI Bill Extraction", "Extract data in seconds automatically."),
    ("🧠", "Smart Categorization", "Auto-categorize complex expenses."),
    ("🚨", "Anomaly Detection", "Detect unusual patterns & fraud."),
    ("📊", "Insightful Analytics", "Visualize deep business insights.")
]

for col, (icon, title, desc) in zip([c1, c2, c3, c4], features):
    with col:
        st.markdown(f"""
        <div class="feature-box">
            <h1 style="margin:0; font-size: 2.5rem;">{icon}</h1>
            <p class="feature-title">{title}</p>
            <p class="feature-desc">{desc}</p>
        </div>
        """, unsafe_allow_html=True)