import streamlit as st
import requests
from dotenv import load_dotenv
import os
from streamlit_js_eval import get_geolocation

# Load your API key
load_dotenv()
# api_key = os.getenv("OPENWEATHER_API_KEY")
api_key = "b2850cf621f9cc7fa55f449849c287e7"

# Page settings
st.set_page_config(page_title="📍 Real-Time Weather", layout="centered")
st.title("📍 Real-Time Location-Based Weather Predictor")

# Try to get user location via browser
location = get_geolocation()

if location and location.get("coords"):
    lat = location["coords"]["latitude"]
    lon = location["coords"]["longitude"]
    st.success(f"📍 Detected Location: {lat:.2f}, {lon:.2f}")

    # Get weather using coordinates
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units=metric&appid={api_key}"
    res = requests.get(url)
    response = res.json()

    if response.get("cod") == 200:
        st.subheader(f"🌆 City: {response['name']}")
        st.metric(label="🌡️ Temperature", value=f"{response['main']['temp']}°C")
        st.write(f"🌥️ Condition: {response['weather'][0]['description'].title()}")
        st.write(f"💧 Humidity: {response['main']['humidity']}%")
    else:
        st.error("⚠️ Weather data could not be fetched from OpenWeather.")
else:
    st.warning("📍 Auto-location not detected. You can enter your city manually.")

    # Manual input fallback
    city = st.text_input("🔍 Enter City Name")

    if st.button("Get Weather"):
        if city.strip():
            city_url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units=metric&appid={api_key}"
            city_res = requests.get(city_url)
            city_data = city_res.json()

            if city_data.get("cod") == 200:
                st.subheader(f"🌆 City: {city_data['name']}")
                st.metric(label="🌡️ Temperature", value=f"{city_data['main']['temp']}°C")
                st.write(f"🌥️ Condition: {city_data['weather'][0]['description'].title()}")
                st.write(f"💧 Humidity: {city_data['main']['humidity']}%")
            else:
                st.error("⚠️ Could not find weather for this city. Please check the spelling.")
        else:
            st.warning("⚠️ Please enter a city name.")
