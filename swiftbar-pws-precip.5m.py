#!/usr/bin/env python3

import configparser
import urllib.request
import json
from pathlib import Path

try:
    config_path = Path(__file__).parent / "weather.conf"
    config = configparser.ConfigParser()
    config.read(config_path)

    api_key = config['weather']['api_key']
    station_id = config['weather']['station_id']

    url = f"https://api.weather.com/v2/pws/observations/current?stationId={station_id}&format=json&units=e&apiKey={api_key}"

    with urllib.request.urlopen(url) as response:
        data = json.load(response)

    obs = data['observations'][0]
    precip_rate = obs['imperial']['precipRate']
    precip_total = obs['imperial']['precipTotal']

    # SwiftBar output
    print(f"⛆ {precip_total} in")
    print("---")
    print(f"Rate: {precip_rate} in/hr")

except Exception as e:
    print("⚠️ Error")
    print("---")
    print(str(e))
