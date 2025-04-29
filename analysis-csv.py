import requests
import pandas as pd

API_KEY = "9bc7010b32de8e705ec8bef3a513be8e"
#Example New Delhi
lat = 25.6139
lon = 70.2090
    
url = f"http://api.openweathermap.org/data/2.5/air_pollution?lat={lat}&lon={lon}&appid={API_KEY}"

response = requests.get(url)

if response.status_code == 200:
    try:
        data = response.json()
        if 'list' in data and len(data['list']) > 0:
            aq_data = data['list'][0]['components']
            aqi_value = data['list'][0]['main']['aqi']
            aq_data['AQI'] = aqi_value

            # AQI interpretation
            aqi_scale = {
                1: "Good 🟢 - Air quality is satisfactory.",
                2: "Fair 🟡 - Acceptable; minor concern for sensitive individuals.",
                3: "Moderate 🟠 - May affect sensitive groups.",
                4: "Poor 🔴 - May cause discomfort for people with respiratory issues.",
                5: "Very Poor 🟣 - Serious health effects possible."
            }

            aqi_description = aqi_scale.get(aqi_value, "Unknown AQI level")

            # Create DataFrame
            df = pd.DataFrame([aq_data])
            print("🧪 Air Quality Components:")
            print(df.drop(columns='AQI'))  # Show pollutants only

            print("\n📊 AQI Summary:")
            print(f"AQI Level: {aqi_value}")
            print(f"Description: {aqi_description}")

        else:
            print("No air quality data found in the response.")
    except ValueError as e:
        print("Error parsing JSON:", e)
else:
    print(f"Failed to fetch data: {response.status_code} - {response.reason}")
