import streamlit as st
import requests
import datetime
from streamlit_js_eval import get_geolocation

api_key = "6040c6c74f7d471d8ffb884ffa6d621b"  # ✅ New working key for OneCall 3.0

st.set_page_config(page_title="📍 Real-Time Weather", layout="centered")
st.title("📍 Real-Time Location-Based Weather Predictor")

unit = st.radio("Choose temperature unit:", ("Celsius (°C)", "Fahrenheit (°F)"))
units_param = "metric" if unit.startswith("Celsius") else "imperial"
temp_symbol = "°C" if units_param == "metric" else "°F"

def get_wind_direction(degree):
    dirs = ['N', 'NE', 'E', 'SE', 'S', 'SW', 'W', 'NW', 'N']
    ix = int((degree + 22.5) / 45)
    return dirs[ix % 8]

def convert_utc_to_local(utc_timestamp, offset_seconds):
    tz = datetime.timezone(datetime.timedelta(seconds=offset_seconds))
    utc_dt = datetime.datetime.utcfromtimestamp(utc_timestamp).replace(tzinfo=datetime.timezone.utc)
    local_dt = utc_dt.astimezone(tz)
    return local_dt.strftime('%H:%M:%S')

def get_local_datetime(offset_seconds):
    tz = datetime.timezone(datetime.timedelta(seconds=offset_seconds))
    utc_now = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc)
    local_now = utc_now.astimezone(tz)
    return local_now.strftime('%A, %d %B %Y %H:%M')

def set_background_color(weather_main):
    weather_main = weather_main.lower()
    if 'rain' in weather_main:
        return '#A3BFD9'
    elif 'cloud' in weather_main:
        return '#C0C0C0'
    elif 'clear' in weather_main:
        return '#FFD966'
    elif 'snow' in weather_main:
        return '#FFFFFF'
    else:
        return '#F0F0F0'

def fetch_weather_by_coords(lat, lon):
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&units={units_param}&appid={api_key}"
    res = requests.get(url)
    return res.json()

def fetch_weather_by_city(city):
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&units={units_param}&appid={api_key}"
    res = requests.get(url)
    return res.json()

# def fetch_7_day_forecast(lat, lon):
#     url = f"https://api.openweathermap.org/data/2.5/onecall"
#     params = {
#         "lat": lat,
#         "lon": lon,
#         "exclude": "minutely,hourly,alerts,current",
#         "units": units_param,
#         "appid": api_key
#     }
#     res = requests.get(url, params=params)
#     data = res.json()

#     # Optional: Check and handle if "daily" is missing
#     if "daily" not in data:
#         st.error("⚠️ 7-day forecast data not available. Please check your API plan or try again later.")
#         return {"daily": []}  # Return empty structure to avoid crash
#     return data



# def display_forecast(data):
#     st.markdown("## 📅 7-Day Forecast")
#     daily = data.get("daily", [])[:7]

#     for i in range(0, len(daily), 3):
#         cols = st.columns(3)
#         for j in range(3):
#             if i + j < len(daily):
#                 day = daily[i + j]
#                 date = datetime.datetime.fromtimestamp(day["dt"]).strftime("%A, %d %b")
#                 icon = day["weather"][0]["icon"]
#                 description = day["weather"][0]["description"].title()
#                 temp_day = day["temp"]["day"]
#                 temp_night = day["temp"]["night"]
#                 humidity = day["humidity"]

#                 with cols[j]:
#                     st.markdown(f"### {date}")
#                     st.image(f"http://openweathermap.org/img/wn/{icon}@2x.png", width=70)
#                     st.markdown(f"**🌤 {description}**")
#                     st.markdown(f"🌡 Day: `{temp_day} {temp_symbol}`")
#                     st.markdown(f"🌙 Night: `{temp_night} {temp_symbol}`")
#                     st.markdown(f"💧 Humidity: `{humidity}%`")

def display_weather(data):
    if data.get("cod") != 200:
        st.error("⚠️ Could not fetch weather data.")
        return

    city_name = data['name']
    temp = data['main']['temp']
    feels_like = data['main']['feels_like']
    condition = data['weather'][0]['description'].title()
    humidity = data['main']['humidity']
    pressure = data['main']['pressure']
    visibility = data.get('visibility', 0) / 1000
    wind_speed = data['wind']['speed']
    wind_deg = data['wind'].get('deg', 0)
    wind_dir = get_wind_direction(wind_deg)
    timezone_sec = data.get('timezone', 0)
    sunrise = convert_utc_to_local(data['sys']['sunrise'], timezone_sec)
    sunset = convert_utc_to_local(data['sys']['sunset'], timezone_sec)
    local_time = get_local_datetime(timezone_sec)

    bg_color = set_background_color(data['weather'][0]['main'])
    st.markdown(
        f"<div style='background-color:{bg_color}; padding:20px; border-radius:15px; box-shadow: 3px 3px 10px rgba(0,0,0,0.2);'>",
        unsafe_allow_html=True
    )

    icon_code = data['weather'][0]['icon']
    icon_url = f"http://openweathermap.org/img/wn/{icon_code}@4x.png"
    st.image(icon_url, width=150)

    st.markdown(f"### 🌆 {city_name}")
    st.markdown(f"**🕒 Local time:** {local_time}")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f"🌡 Temperature ({temp_symbol})", value=f"{temp} {temp_symbol}")
        st.metric(label=f"🤗 Feels Like ({temp_symbol})", value=f"{feels_like} {temp_symbol}")
        st.write(f"🌥 Condition: {condition}")
    with col2:
        st.write(f"💧 Humidity: {humidity}%")
        st.write(f"👁️ Visibility: {visibility} km")
        st.write(f"📈 Pressure: {pressure} hPa")
        st.write(f"🌬 Wind: {wind_speed} m/s, {wind_dir}")
        st.write(f"🌅 Sunrise: {sunrise}")
        st.write(f"🌇 Sunset: {sunset}")
    st.markdown("</div>", unsafe_allow_html=True)

# 🌍 Main Logic
location = get_geolocation()

if location and location.get("coords"):
    lat = location["coords"]["latitude"]
    lon = location["coords"]["longitude"]
    st.success(f"📍 Detected Location: {lat:.2f}, {lon:.2f}")
    weather_data = fetch_weather_by_coords(lat, lon)
    #forecast_data = fetch_7_day_forecast(lat, lon)
    display_weather(weather_data)
    #display_forecast(forecast_data)

else:
    st.warning("📍 Could not detect your location automatically. Please enter your city name below.")
    city = st.text_input("🔍 Enter City Name")

    if st.button("Get Weather"):
        if city.strip():
            weather_data = fetch_weather_by_city(city.strip())
            if weather_data.get("cod") == 200:
                lat = weather_data["coord"]["lat"]
                lon = weather_data["coord"]["lon"]
                #forecast_data = fetch_7_day_forecast(lat, lon)
                display_weather(weather_data)
                #display_forecast(forecast_data)
            else:
                st.error("⚠️ City not found. Please check spelling or try another city.")
        else:
            st.warning("⚠️ Please enter a city name.")
