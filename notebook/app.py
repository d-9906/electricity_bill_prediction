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
            
[data-testid="stAppViewContainer"] {
    background: linear-gradient(135deg, #f8fbff 0%, #e7f0ff 100%) !important;
    color: #102a43 !important;
}


[data-testid="stHeader"],
[data-testid="stToolbar"],
[data-testid="stSidebar"] {
    background: transparent !important;
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
    color: #27187d !important;
}


.subtitle {
    text-align: center;
    font-size: 20px;
    margin-bottom: 25px;
    color: #334155 !important;
}



.bill-card {
    background: rgba(255,255,255,0.90) !important;
    padding: 30px;
    border-radius: 20px;
    box-shadow: 0px 0px 18px rgba(0,0,0,0.10);
    border-left: 10px solid #38BDF8;
    backdrop-filter: blur(8px);
    color: #102a43 !important;
}



.footer {
    text-align: center;
    padding: 10px;
    color: inherit !important;
}

.decor-row {
    text-align: center;
    font-size: 34px;
    letter-spacing: 10px;
    margin: 10px 0 18px 0;
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

st.markdown("<div style='text-align:center;font-size:60px'>💡 ⚡ 🌀 🔌 🏠</div>", unsafe_allow_html=True)
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

