import requests
import configparser
import os

# Load API key from config file
config = configparser.ConfigParser()
config.read('weather.conf')

try:
    api_key = config['weather']['api_key']
    station_id = config['weather'].get('station_id', 'KFLSARAS2216')
except KeyError:
    raise RuntimeError("Missing required configuration in weather.conf")

# Build the API URL
url = (
    "https://api.weather.com/v2/pws/observations/current"
    f"?stationId={station_id}&format=json&units=e&apiKey={api_key}"
)

# Send the request
response = requests.get(url)
data = response.json()

# Parse the relevant data
try:
    observation = data["observations"][0]
    precip_rate = observation["imperial"]["precipRate"]
    precip_total = observation["imperial"]["precipTotal"]
    print(f"Precipitation Rate: {precip_rate} in/hr")
    print(f"Precipitation Accumulation (today): {precip_total} in")
except (KeyError, IndexError):
    print("Failed to retrieve precipitation data. Observation may be expired.")
