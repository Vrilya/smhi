from smhi_weather import SmhiWeather
import json
import requests

# Definiera koordinaterna
latitude = 57.112354
longitude = 12.289106

forecast = SmhiWeather(latitude, longitude).get_forecast()

# Hämta platsnamnet från OpenStreetMap
response = requests.get(f"https://nominatim.openstreetmap.org/reverse?format=json&lat={latitude}&lon={longitude}")
location_data = response.json()

# Kontrollera om 'town' finns i adressdatan, om inte, använd 'village'
if 'town' in location_data["address"]:
    location_name = location_data["address"]["town"]
elif 'village' in location_data["address"]:
    location_name = location_data["address"]["village"]
elif 'municipality' in location_data["address"]:
    location_name = location_data["address"]["municipality"]
else:
    location_name = "Okänd plats"

# Hämta den nuvarande temperaturen
current_time_series = forecast['timeSeries'][0]
for parameters in current_time_series['parameters']:
    if parameters['name'] == 't':
        print(f"Det är just nu {parameters['values'][0]} grader i {location_name}.")
        break

# Hämta den nuvarande vindhastigheten
for parameters in current_time_series['parameters']:
    if parameters['name'] == 'ws':
        wind_speed = parameters['values'][0]
        break

# Definiera vindförhållanden baserat på Beauforts vindskala
if wind_speed < 4:
    wind_condition = "lugnt"
elif wind_speed < 8:
    wind_condition = "lätt bris"
elif wind_speed < 14:
    wind_condition = "måttlig vind"
elif wind_speed < 21:
    wind_condition = "frisk vind"
elif wind_speed < 29:
    wind_condition = "stark vind"
elif wind_speed < 38:
    wind_condition = "storm"
else:
    wind_condition = "orkan"

print(f"Det är {wind_condition} just nu med en vindhastighet på {wind_speed} m/s.")

# Hämta den nuvarande nederbördskategorin
for parameters in current_time_series['parameters']:
    if parameters['name'] == 'pcat':
        precipitation_category = parameters['values'][0]
        break

# Definiera nederbördskategorier
precipitation_categories = {
    0: "Ingen nederbörd",
    1: "Snö",
    2: "Snöblandat regn",
    3: "Regn",
    4: "Duggregn",
    5: "Fryst duggregn",
    6: "Fryst regn"
}

print(f"Nederbördskategori: {precipitation_categories[precipitation_category]}")
