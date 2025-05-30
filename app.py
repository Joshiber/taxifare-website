import streamlit as st
import datetime
import requests

# ---------- Page Config ----------
st.set_page_config(page_title="Taxi Fare Estimator", layout="centered", page_icon="🛺")

# ---------- Adaptive CSS Theme ----------
st.markdown("""
<style>
    :root {
        --primary-green: #2ecc71;
        --text-color-light: #333;
        --text-color-dark: #eee;
        --bg-color-light: #ffffff;
        --bg-color-dark: #1e1e1e;
        --card-bg-light: #f9f9f9;
        --card-bg-dark: #2c2c2c;
    }

    @media (prefers-color-scheme: dark) {
        html, body, .stApp {
            background-color: var(--bg-color-dark);
            color: var(--text-color-dark);
        }
        .block-container {
            background-color: var(--card-bg-dark);
            border-radius: 10px;
            padding: 2rem;
        }
    }

    @media (prefers-color-scheme: light) {
        html, body, .stApp {
            background-color: var(--bg-color-light);
            color: var(--text-color-light);
        }
        .block-container {
            background-color: var(--card-bg-light);
            border-radius: 10px;
            padding: 2rem;
        }
    }

    h1 {
        color: var(--primary-green);
        text-align: center;
        margin-bottom: 1.5rem;
    }

    .stButton>button {
        background-color: var(--primary-green);
        color: white;
        border: none;
        padding: 0.6em 1.2em;
        border-radius: 6px;
        font-weight: bold;
        transition: background-color 0.2s ease;
    }

    .stButton>button:hover {
        background-color: #27ae60;
    }

    hr {
        border: none;
        border-top: 1px solid #ccc;
        margin: 1.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# ---------- Title ----------
st.markdown("<h1>Taxi Fare Estimator</h1>", unsafe_allow_html=True)

# ---------- Sidebar Inputs ----------
st.sidebar.header("📍 Ride Details")

pickup_date = st.sidebar.date_input("Pickup Date", datetime.date.today())
pickup_time = st.sidebar.time_input("Pickup Time", datetime.datetime.now().time())

pickup_latitude = st.sidebar.slider("Pickup Latitude", 40.60, 40.90, 40.75, step=0.0001)
pickup_longitude = st.sidebar.slider("Pickup Longitude", -74.05, -73.75, -73.98, step=0.0001)

dropoff_latitude = st.sidebar.slider("Dropoff Latitude", 40.60, 40.90, 40.76, step=0.0001)
dropoff_longitude = st.sidebar.slider("Dropoff Longitude", -74.05, -73.75, -73.99, step=0.0001)

passenger_count = st.sidebar.slider("Passenger Count", 1, 6, 1)

pickup_datetime = f"{pickup_date} {pickup_time}"

# ---------- Ride Summary ----------
st.subheader("🧾 Ride Summary")
st.markdown(f"""
- **Pickup:** ({pickup_latitude}, {pickup_longitude})  
- **Dropoff:** ({dropoff_latitude}, {dropoff_longitude})  
- **Datetime:** {pickup_datetime}  
- **Passengers:** {passenger_count}  
""")

# ---------- Prediction ----------
st.subheader("💰 Predicted Fare")

params = {
    "pickup_datetime": pickup_datetime,
    "pickup_longitude": pickup_longitude,
    "pickup_latitude": pickup_latitude,
    "dropoff_longitude": dropoff_longitude,
    "dropoff_latitude": dropoff_latitude,
    "passenger_count": passenger_count
}

url = "https://taxifare.lewagon.ai/predict"

if st.button("Predict Fare"):
    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        fare = response.json()["fare"]
        st.success(f"Estimated Fare: ${fare:.2f}")
    except Exception as e:
        st.error("Could not fetch prediction.")
        st.exception(e)

# ---------- Footer ----------
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<div style='text-align:center; color:gray;'>TaxiFare</div>",
    unsafe_allow_html=True
)
