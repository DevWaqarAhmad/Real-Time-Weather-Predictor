import streamlit as st
import geocoder
import requests
from dotenv import load_dotenv
import os

# Load your API key
load_dotenv()
#api_key = os.getenv("OPENWEATHER_API_KEY")
api_key = "b2850cf621f9cc7fa55f449849c287e7"
# Streamlit page config
st.set_page_config(page_title="📍 Real-Time Weather", layout="centered")
st.title("📍 Real-Time Location-Based Weather Predictor")

# Get user location
g = geocoder.ip('me')
if g.ok:
    lat, lon = g.latlng
    st.write(f"Your Coordinates: 🌐 {lat}, {lon}")

    # API Request to OpenWeather
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    
    res = requests.get(url)
    #st.code(res.text)  # Debug: print full API response
    
    response = res.json()

    if response.get("cod") == 200:
        st.subheader(f"📍 City: {response['name']}")
        st.metric(label="🌡️ Temperature", value=f"{response['main']['temp']}°C")
        st.write(f"🌥️ Condition: {response['weather'][0]['description'].title()}")
        st.write(f"💧 Humidity: {response['main']['humidity']}%")
    else:
        st.error("Failed to fetch weather data.")
else:
    st.error("Could not detect your location.")