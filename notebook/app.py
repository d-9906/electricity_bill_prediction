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

/* KEEP YOUR BACKGROUND */
.stApp {
    background-image: url("https://thumbs.dreamstime.com/z/home-appliances-background-home-appliances-background-vector-seamless-pattern-home-kitchen-machines-graphic-design-165534348.jpg");
    background-size: cover;
    background-position: center;
    background-repeat: no-repeat;
    background-attachment: fixed;
}

/* LIGHTER OVERLAY (important for visibility) */
.stApp::before {
    content: "";
    position: fixed;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: rgba(10, 25, 60, 0.55);  /* reduced darkness */
    z-index: 0;
    pointer-events: none;
}

/* =========================
   STRONGER BUBBLES
========================= */
.bubbles {
    position: fixed;
    width: 100vw;
    height: 100vh;
    overflow: hidden;
    z-index: 0;
    pointer-events: none;
}

/* BIGGER + BRIGHTER + GLOW */
.bubbles span {
    position: absolute;
    bottom: -150px;

    width: 25px;
    height: 25px;

    /* 🔥 much more transparent */
    background: radial-gradient(
        circle,
        rgba(255,255,255,0.28),
        rgba(255,255,255,0.05)
    );

    /* 🔥 remove strong outline look */
    border: 2px solid rgba(255, 255, 255, 0.15);

    outline: none;
    border-radius: 50%;

    /* 🔥 softer glow */
    box-shadow: 0 0 8px rgba(255, 255, 255, 0.10);

    animation: rise 18s linear infinite;
}
/* VARIATIONS */
.bubbles span:nth-child(1) { left: 10%; width: 35px; height: 35px; animation-duration: 16s; }
.bubbles span:nth-child(2) { left: 20%; width: 20px; height: 20px; animation-duration: 22s; }
.bubbles span:nth-child(3) { left: 35%; width: 28px; height: 28px; animation-duration: 14s; }
.bubbles span:nth-child(4) { left: 50%; width: 40px; height: 40px; animation-duration: 20s; }
.bubbles span:nth-child(5) { left: 65%; width: 22px; height: 22px; animation-duration: 17s; }
.bubbles span:nth-child(6) { left: 80%; width: 30px; height: 30px; animation-duration: 19s; }
.bubbles span:nth-child(7) { left: 90%; width: 18px; height: 18px; animation-duration: 15s; }

/* SMOOTHER MOVEMENT */
@keyframes rise {
    0% {
        transform: translateY(0) scale(0.8);
        opacity: 0;
    }
    10% {
        opacity: 0.6;
    }
    50% {
        opacity: 0.9;
    }
    100% {
        transform: translateY(-110vh) scale(1.3);
        opacity: 0;
    }
}

/* KEEP CONTENT ABOVE */
.block-container {
    position: relative;
    z-index: 2;
}

</style>

<div class="bubbles">
    <span></span><span></span><span></span><span></span>
    <span></span><span></span><span></span>
</div>

""", unsafe_allow_html=True)
st.markdown("""<style>.block-container{padding-top:0rem;}</style>""", unsafe_allow_html=True)
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
   background: rgba(16,45,82,0.75);
    z-index: 0;
    pointer-events: none;
        backdrop-filter: blur(2px)
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
    color: #ffffff !important;
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
    color:#ffffff !important;
}


.subtitle {
    text-align: center;
    font-size: 20px;
    margin-bottom: 25px;
    color: #ffffff!important;
}



.bill-card {
    background: rgba(17, 24, 39, 0.50);
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
    color: #153a66 !important;
    font-weight:bold;
    background: rgba(255,255,255,0.08) !important;
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2) !important;
}
            [data-baseweb="select"] * {
    color: #153a66  !important;
    fill: #153a66 !important;
}

/* Selected value (main fix) */
div[data-baseweb="select"] span {
    color: #153a66  !important;
}

/* Input container */
div[data-baseweb="select"] > div {
    background: #ffffff) !important;
    border: 1px solid rgba(255,255,255,0.25) !important;
    border-radius: 10px !important;
}

/* Arrow icon fix */
div[data-baseweb="select"] svg {
    fill: #153a66  !important;
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
    background: linear-gradient(135deg, #bfd7ff, #7fb3ff) !important; !important;
    color: color: #102d52 !important;   !important;
    border: none !important;
    padding: 10px 20px !important;
    border-radius: 12px !important;
    font-weight: 600 !important;
    font-size: 16px !important;
    transition: 0.3s ease !important;
}
.stButton > button {
    background: linear-gradient(135deg, #bfd7ff, #8fb8ff) !important;
    color: #102d52 !important;
    border: none !important;
}

.stButton > button * {
    color: #102d52 !important;
}
.stButton > button:hover {
    transform: scale(1.03);
    box-shadow: 0 0 15px rgba(56,189,248,0.5);
}

div[data-testid="stAlert"] {
    background: rgba(191, 215, 255, 0.18) !important;
    border: 1px solid rgba(191, 215, 255, 0.35) !important;
    backdrop-filter: blur(10px);
    border-radius: 12px !important;
}

div[data-testid="stAlert"] * {
    color: #ffffff !important;
}

/* ABOUT MODEL SECTION CARD */
.stInfo {
    background: rgba(17, 24, 39, 0.75) !important;
    color: #e5e7eb !important;
}

/* 
HEADERS INSIDE INFO BOXES */
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
    text-align:center;
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

st.markdown("<div style='text-align:center;font-size:20px,color:#f1efd8'>◉ Electricity Bill Prediction System ◉</div>", unsafe_allow_html=True)
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
    estimated_units = prediction / tariff_rate if tariff_rate > 0 else 0

    if prediction < 2000:
         confidence = "High Confidence"
    elif prediction < 5000:
        confidence = "Very Good Confidence"
    else:
        confidence = "Moderate Confidence"

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
    st.markdown(
    f"""
    <div class='bill-card'>
    <h2>📄 ELECTRICITY BILL</h2>
    <hr>

    <h3>Predicted Amount</h3>
    <h1 style='color:#bfd7ff'>₹ {prediction:,.2f}</h1>

    <h3>Consumption Category</h3>
    <p style='font-size:22px'>{category}</p>

    <h3>Estimated Units Consumed</h3>
    <p style='font-size:22px'>{estimated_units:.0f} kWh</p>

    <h3>Prediction Confidence</h3>
    <p style='font-size:20px'>{confidence}</p>
    </div>
    """, 
    unsafe_allow_html=True)

    bill_percent = min(int((prediction / 8000) * 100), 100)

    st.markdown("### ⚡ Consumption Meter")
    st.progress(bill_percent)
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
    "<h3 style='text-align: center; color: inherit;'> About The Model</h3>",
    unsafe_allow_html=True
)
st.info("""
🤖 Model: Random Forest Regressor

📊 Dataset:
Indian Household Electricity Bill Dataset - https://www.kaggle.com/datasets/suraj520/indian-household-electricity-bill

⚡ Features Used:
• Appliance Usage
• Monthly Hours
• City
• Electricity Company
• Tariff Rate

🎯 Purpose:
Predict future electricity bills using Machine Learning.
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






