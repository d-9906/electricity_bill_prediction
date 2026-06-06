import streamlit as st
import pandas as pd
import pickle

st.set_page_config(
    page_title="Electricity Bill Prediction",
    page_icon="⚡",
    layout="wide"
)


st.markdown("""
<style>
        


            

/* MAIN BACKGROUND IMAGE */
.stApp {
    background-image: url("https://thumbs.dreamstime.com/z/home-appliances-background-home-appliances-background-vector-seamless-pattern-home-kitchen-machines-graphic-design-165534348.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* DARK OVERLAY (makes text readable) */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(0,0,0, 0.75);
    z-index: 0;
    pointer-events: none;
}

/* BRING CONTENT ABOVE OVERLAY */
.main, .block-container {
    position: relative;
    z-index: 1;
}


[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stSidebar"] {
    background: transparent !important;
}

   body, .stApp {
    color: #e5e7eb !important;
}         
.main, .block-container {
    background: transparent !important;
}

h1, h2, h3, h4, h5, h6, p, label, span, div {
    color: inherit !important;
}

.title {
    text-align: center;
    font-size: 50px;
    font-weight: 800;
    margin-bottom: 10px;
    color:#e6d0ad !important;
}


.subtitle {
    text-align: center;
    font-size: 20px;
    margin-bottom: 25px;
    color: #e6d0ad !important;
}



.bill-card {
    background: rgba(17, 24, 39, 0.75);
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0px 0px 18px rgba(0,0,0,0.10);
    border-left: 10px solid #38BDF8;
    backdrop-filter: blur(8px);
    color: #f1f5f9 !important;
}



.footer {
    text-align: center;
    padding: 10px;
    color: inherit !important;
}
input, textarea {
    color: #ffffff !important;
    background: rgba(0,0,0,0.55) !important;
    border: 1px solid rgba(255,255,255,0.2) !important;
}
div[data-baseweb="select"] * {
    color: #ffffff !important;
    fill: #ffffff !important;
}

/* Selected value (main fix) */
div[data-baseweb="select"] span {
    color: #ffffff !important;
}

/* Input container */
div[data-baseweb="select"] > div {
    background: rgba(0,0,0,0.55) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 10px !important;
}

/* Arrow icon fix */
div[data-baseweb="select"] svg {
    fill: #ffffff !important;
}
.decor-row {
    text-align: center;
    font-size: 34px;
    letter-spacing: 10px;
    margin: 10px 0 18px 0;
}
            
           
/* =========================
   BUTTON STYLING
========================= */
.stButton > button {
    background: linear-gradient(135deg, #38bdf8, #6366f1) !important;
    color: white !important;
    border: none !important;
    padding: 10px 20px !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    transition: 0.3s ease !important;
}

.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 15px rgba(56,189,248,0.5);
}

/* =========================
   INFO CARDS (b1, b2, b3 + st.info)
========================= */
div[data-testid="stAlert"] {
    background: rgba(17, 24, 39, 0.75) !important;
    color: #e5e7eb !important;
    border-radius: 12px !important;
    border: 1px solid rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(10px);
}

/* =========================
   ABOUT MODEL SECTION CARD
========================= */
.stInfo {
    background: rgba(17, 24, 39, 0.75) !important;
    color: #e5e7eb !important;
}

/* =========================
   HEADERS INSIDE INFO BOXES
========================= */
div[data-testid="stAlert"] p {
    color: #e5e7eb !important;
}

/* =========================
   RESULT BILL CARD (your custom card)
========================= */
.bill-card {
    background: rgba(17, 24, 39, 0.85) !important;
    backdrop-filter: blur(12px);
    border-radius: 20px;
    border: 1px solid rgba(255,255,255,0.12);
    color: #f1f5f9 !important;
}

/* =========================
   GENERAL TEXT FIX
========================= */
h1, h2, h3, p, label {
    color: #f1f5f9 !important;
}
            
            div[data-testid="stSuccess"] {
    background: rgba(0,0,0,0.65) !important;
    color: #ffffff !important;
    border: 1px solid rgba(56,189,248,0.4) !important;
}
            
            div[data-testid="stSuccess"] * {
    color: #ffffff !important;
}
</style>
""", unsafe_allow_html=True)


model = pickle.load(open("model.pkl", "rb"))
scaler = pickle.load(open("scaler.pkl", "rb"))
df = pd.read_csv("electricity_bill_dataset.csv")

city_list = sorted(df["City"].unique())
company_list = sorted(df["Company"].unique())
month_list = sorted(df["Month"].unique())

city_mapping = {city: idx for idx, city in enumerate(city_list)}
company_mapping = {company: idx for idx, company in enumerate(company_list)}

st.markdown("<div style='text-align:center;font-size:20px,color:e6d0ad'>◉ Electricity Bill Prediction System ◉</div>", unsafe_allow_html=True)
st.markdown("<div class='title'> What Will Be My Next Electricity Bill?</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>Predict your upcoming electricity bill using Machine Learning</div>", unsafe_allow_html=True)
st.divider()


st.subheader("🏠 Appliance Usage Details")
col1, col2 = st.columns(2)

with col1:
    fan = st.number_input("🌀 Fan Usage", min_value=0.0, value=5.0)
    refrigerator = st.number_input("❄ Refrigerator Usage", min_value=0.0, value=10.0)
    ac = st.number_input("🌬 Air Conditioner Usage", min_value=0.0, value=2.0)

with col2:
    television = st.number_input("📺 Television Usage", min_value=0.0, value=4.0)
    monitor = st.number_input("🖥 Monitor Usage", min_value=0.0, value=3.0)
    motorpump = st.number_input("🚰 Motor Pump Usage", min_value=0.0, value=1.0)

st.divider()
st.subheader("📋 Billing Details")
col3, col4 = st.columns(2)

with col3:
    month = st.selectbox("📅 Month", month_list)
    city = st.selectbox("🏙 City", city_list)

with col4:
    company = st.selectbox("🏢 Electricity Company", company_list)
    tariff_rate = st.number_input("💰 Tariff Rate", min_value=0.0, value=5.0)

monthly_hours = st.number_input("⏰ Monthly Hours", min_value=0.0, value=120.0)

st.divider()

if st.button("🔮 Predict My Electricity Bill"):
    total_appliance_load = (
        fan * 1.0 +
        refrigerator * 3.0 +
        ac * 5.0 +
        television * 2.0 +
        monitor * 1.5 +
        motorpump * 4.0
    )

    city_encoded = city_mapping[city]
    company_encoded = company_mapping[company]

    input_df = pd.DataFrame([[
        city_encoded,
        company_encoded,
        fan,
        refrigerator,
        ac,
        television,
        monitor,
        motorpump,
        month,
        monthly_hours,
        tariff_rate
    ]], columns=[
        "City",
        "Company",
        "Fan",
        "Refrigerator",
        "AirConditioner",
        "Television",
        "Monitor",
        "MotorPump",
        "Month",
        "MonthlyHours",
        "TariffRate"
    ])

    numeric_cols = [
        "Fan",
        "Refrigerator",
        "AirConditioner",
        "Television",
        "Monitor",
        "MotorPump",
        "Month",
        "MonthlyHours",
        "TariffRate"
    ]

    input_df[numeric_cols] = scaler.transform(input_df[numeric_cols])
    prediction = model.predict(input_df)[0]

    if prediction < 2000:
        category = "🟢 Low Consumption"
    elif prediction < 5000:
        category = "🟡 Moderate Consumption"
    else:
        category = "🔴 High Consumption"

    tips = []
    if ac > 8:
        tips.append("Reduce AC usage during peak hours.")
    if total_appliance_load > 30:
        tips.append("Unplug unused appliances when not needed.")
    if prediction < 3000:
        tips.append("Great job! Continue efficient usage.")
    if not tips:
        tips.append("Maintain current energy-saving habits.")

    st.divider()
    st.markdown(f"""
    <div class='bill-card'>
        <h2>📄 ELECTRICITY BILL</h2>
        <hr>
        <h3>Predicted Amount</h3>
        <h1 style='color:green'>₹ {prediction:,.2f}</h1>
        <h3>Consumption Category</h3>
        <p style='font-size:22px'>{category}</p>
    </div>
    """, unsafe_allow_html=True)

    st.progress(min(int(prediction / 100), 100))
    st.subheader("💡 Smart Energy Tips")
    for tip in tips:
        st.success(tip)

st.divider()

b1, b2, b3 = st.columns(3)
with b1:
    st.info("💡 Save energy with smarter choices")
with b2:
    st.info("🌀 Track appliance usage")
with b3:
    st.info("⚡ Predict your next bill")

st.divider()
    
st.markdown(
    "<h3 style='text-align: center; color: inherit;'>🤖 About The Model</h3>",
    unsafe_allow_html=True
)
st.info("""
Machine Learning Model: Random Forest Regressor

Dataset: Household Electricity Consumption Dataset
https://www.kaggle.com/datasets/suraj520/indian-household-electricity-bill

Purpose:
Estimate future electricity bills using appliance usage,
monthly hours, city, company and tariff information.
""")

st.divider()
st.markdown("""
<div class='footer'>
    <h3>⚡ Electricity Bill Prediction System</h3>
    <p>Built using Machine Learning + Streamlit</p>
    <hr style='width:40%;margin:auto;'>
    <p>Developed by</p>
    <b>Disha Thakur • Reetika Sharma • Shraddha Khare</b>
    <br><br>
    <small>© 2026 All Rights Reserved</small>
</div>
""", unsafe_allow_html=True)

