# 🌦️ Real-Time Weather Predictor

A real-time weather prediction web app built with **Streamlit**, integrated with **OpenWeatherMap API**, and enriched with **geolocation** and **air quality metrics** for an interactive and user-friendly experience.

🚀 **Live Demo**  
[🌐 View Deployed App on Render](https://real-time-weather-predictor.onrender.com/)

---

## 📌 Features

- 📍 **Auto Detect User Location**
- 🌡️ Real-time **Temperature**, **Humidity**, **Pressure**, and **Wind Speed**
- 📆 Current **Day, Date & Time**
- 🌥️ **Weather Forecast** by Day
- 🌞 **Sunrise & Sunset Timings**
- 🧪 **Air Quality Metrics**:
  - PM2.5 (`µg/m³`)
  - PM10 (`µg/m³`)
  - AQI Score + Health Description
- 🌗 **Day/Night Based Theming** with Sun & Moon icons
- 📱 **Responsive & Clean UI** using `streamlit_extras`

---

## 🛠️ Tech Stack & Libraries

- **Python 3.10+**
- **Streamlit**
- **OpenWeatherMap API**
- `requests`
- `datetime`
- `streamlit_js_eval` – for geolocation detection
- `streamlit_extras.metric_cards` – for modern styled metric cards

---

## 📦 Installation

1. **Clone the Repository**
   ```bash
   git clone https:https://github.com/DevWaqarAhmad/Real-Time-Weather-Predictor
   cd Real-Time-Weather-Predictor
Create a Virtual Environment

bash
Copy
Edit
python -m venv venv
source venv/bin/activate

Install Dependencies

bash
Copy
Edit
pip install -r requirements.txt

Create a .env file in the root directory:

env
Copy
Edit
OPENWEATHER_API_KEY=your_api_key_here

Run the App

bash
Copy
Edit
streamlit run app.py

🧠 How it Works
Uses streamlit_js_eval to detect user’s geolocation.

Sends location to OpenWeatherMap API to fetch:

Current weather


Air pollution metrics

Applies sunrise/sunset logic to toggle Sun/Moon visuals.

Displays AQI health messages based on score ranges.

streamlit weather-app openweathermap api-integration air-quality geolocation python real-time dashboard climate
Contributing
Pull requests are welcome! If you find bugs or want to improve the UI/features, feel free to contribute.


License
This project is licensed under the MIT License.


---

