import streamlit as st
import requests
import datetime
from streamlit_js_eval import get_geolocation
from streamlit_extras.metric_cards import style_metric_cards


api_key = "6040c6c74f7d471d8ffb884ffa6d621b"  
st.set_page_config(page_title="Real Time Weather", layout="centered")
st.markdown("<h1 style='text-align: center;'>Real-Time Location-Based Weather Predictor</h1>", unsafe_allow_html=True)

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

# def set_background_color(weather_main):
#     weather_main = weather_main.lower()
#     if 'rain' in weather_main:
#         return '#A3BFD9'
#     elif 'cloud' in weather_main:
#         return '#C0C0C0'
#     elif 'clear' in weather_main:
#         return '#FFD966'
#     elif 'snow' in weather_main:
#         return '#FFFFFF'
#     else:
#         return '#F0F0F0'
def get_weather_suggestion(temp, humidity, condition, wind_speed, visibility):
    suggestion = ""

    condition_lower = condition.lower()

    # 🔥 Extreme heat and humidity
    if temp >= 38 and humidity >= 60:
        suggestion += "🥵 Extreme heat and humidity! Avoid sunlight. Stay indoors, wear loose cotton clothes, use fans/AC, and keep ORS or lemonade handy."

    # 🌡️ Hot and sticky
    elif 30 <= temp < 38 and humidity >= 70:
        suggestion += "🌡️ It's hot and sticky — habas wala mosam. Cotton clothes, lots of water, and shade are a must."

    # ☀️ Hot but manageable
    elif 30 <= temp < 38 and humidity < 70:
        suggestion += "☀️ It's warm but manageable. Stay hydrated, wear sunglasses, and avoid heavy meals."

    # 😊 Pleasant weather
    elif 20 <= temp < 30:
        if humidity > 75:
            suggestion += "🌤️ Comfortable temperature but sticky due to humidity. Light dressing recommended, and ventilation is important."
        else:
            suggestion += "🙂 Perfect weather! Great time for a walk or light outdoor activity. Light clothes will be just fine."

    # 🧊 Chilly
    elif 10 <= temp < 20:
        suggestion += "🧥 A bit chilly. Wear a sweater or jacket, and consider warm drinks like chai or coffee."

    # ❄️ Cold
    elif temp < 10:
        suggestion += "❄️ Very cold! Wear layers, use socks and gloves if going out, and try dry fruits or soup to stay warm."

    # ☔ Rain conditions
    if "rain" in condition_lower:
        suggestion += " ☔ Rain expected — carry an umbrella, avoid slippery roads, and wear waterproof shoes."

    # ❄️ Snow
    if "snow" in condition_lower:
        suggestion += " ❄️ Snowfall ahead — bundle up! Drive or walk carefully."

    # 🌫️ Fog or mist
    if "fog" in condition_lower or "mist" in condition_lower:
        suggestion += " 🌫️ Foggy weather — drive slowly, use fog lights, and avoid early morning outings if possible."

    # 🌪️ Dust storm / haze
    if "dust" in condition_lower or "haze" in condition_lower or "sand" in condition_lower:
        suggestion += " 🌪️ Dusty atmosphere — wear a mask outside, keep windows closed, and avoid exposure if you have breathing issues."

    # 🌥️ Cloudy
    if "cloud" in condition_lower and temp > 30:
        suggestion += " ⛅ Cloudy sky but still warm — humidity may increase. Stay cool."

    # 🌞 Clear & dry
    if "clear" in condition_lower and humidity < 30:
        suggestion += " 🔆 Clear and dry day — use moisturizer, drink water, and protect your skin from sunburn."

    # 🌬️ Wind
    if wind_speed >= 10:
        suggestion += f" 💨 Strong winds blowing ({wind_speed} m/s). Secure loose objects and avoid unnecessary exposure."

    # 👁️ Visibility
    if visibility < 2:
        suggestion += f" 👁️ Low visibility ({visibility} km) — be cautious while driving."

    return suggestion.strip()

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
    current_local_ts = datetime.datetime.utcfromtimestamp(data['dt'] + timezone_sec).timestamp()

    # Time-based icon selection
    sunrise_ts = data['sys']['sunrise'] + timezone_sec
    sunset_ts = data['sys']['sunset'] + timezone_sec
    sunrise_start = sunrise_ts - 1800
    sunrise_end = sunrise_ts + 1800
    sunset_start = sunset_ts - 1800
    sunset_end = sunset_ts + 1800

    if sunrise_start <= current_local_ts <= sunrise_end:
        time_icon = "🌅"
    elif sunset_start <= current_local_ts <= sunset_end:
        time_icon = "🌇"
    elif sunrise_ts < current_local_ts < sunset_ts:
        time_icon = "☀️"
    else:
        time_icon = "🌙"

    st.markdown(f"<h1 style='text-align: center; font-size: 60px;'>{time_icon}</h1>", unsafe_allow_html=True)

    # Fetch Air Quality
    try:
        lat = data['coord']['lat']
        lon = data['coord']['lon']
        air_quality_url = f"https://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={api_key}"
        air_quality_response = requests.get(air_quality_url)
        air_quality_data = air_quality_response.json()

        pm2_5 = air_quality_data['list'][0]['components']['pm2_5']
        pm10 = air_quality_data['list'][0]['components']['pm10']
        aqi = air_quality_data['list'][0]['main']['aqi']
    except:
        pm2_5 = pm10 = aqi = None

    # Units and suggestion
    temp_celsius = temp if units_param == "metric" else (temp - 32) * 5 / 9
    suggestion = get_weather_suggestion(temp_celsius, humidity, condition, wind_speed, visibility)

    st.info(suggestion)
    st.markdown(f"### 🌆 {city_name}")
    st.markdown(f"**🕒 Local time:** {local_time}")

    col1, col2 = st.columns(2)
    with col1:
        st.metric(label=f"🌡 Temperature ({temp_symbol})", value=f"{temp} {temp_symbol}")
        st.metric(label=f"🤗 Feels Like ({temp_symbol})", value=f"{feels_like} {temp_symbol}")
        st.write(f"🌥 Condition: {condition}")
        st.write(f"💧 Humidity: {humidity}%")
        st.write(f"👁️ Visibility: {visibility} km")
    with col2:
        st.write(f"📈 Pressure: {pressure} hPa")
        st.write(f"🌬 Wind: {wind_speed} m/s, {wind_dir}")
        st.write(f"🌅 Sunrise: {sunrise}")
        st.write(f"🌇 Sunset: {sunset}")
        if pm2_5 is not None and pm10 is not None:
            st.write(f"🧪 PM2.5: {pm2_5} µg/m³")
            st.write(f"🧪 PM10: {pm10} µg/m³")
        else:
            st.write("⚠️ Air quality data not available.")
        if aqi is not None:
            aqi_levels = {
                1: "🟢 Good",
                2: "🟡 Fair",
                3: "🟠 Moderate",
                4: "🔴 Poor",
                5: "⚫ Very Poor"
            }
            st.write(f"🌫️ AQI: {aqi} {aqi_levels.get(aqi, '')}")



location = get_geolocation()

if location and location.get("coords"):
    lat = location["coords"]["latitude"]
    lon = location["coords"]["longitude"]
    st.success(f"📍 Detected Location: {lat:.2f}, {lon:.2f}")
    weather_data = fetch_weather_by_coords(lat, lon)
    display_weather(weather_data)

else:
    st.warning("📍 Could not detect your location automatically. Please enter your city name below.")
    city = st.text_input("🔍 Enter City Name")

    if st.button("Get Weather"):
        if city.strip():
            weather_data = fetch_weather_by_city(city.strip())
            if weather_data.get("cod") == 200:
                display_weather(weather_data)
            else:
                st.error("⚠️ City not found. Please check spelling or try another city.")
        else:
            st.warning("⚠️ Please enter a city name.")
