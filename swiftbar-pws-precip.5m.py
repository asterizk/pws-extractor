#!/usr/bin/env python3

import configparser
import urllib.request
import json
import os
from pathlib import Path

def error_output(message):
    print("⚠️ Error")
    print("---")
    print(message)

try:
    # Resolve the symlink to find the real script directory
    script_dir = Path(__file__).resolve().parent
    config_path = Path(os.environ.get("SWIFTBAR_WEATHER_CONF", script_dir / "weather.conf"))

    config = configparser.ConfigParser()

    if not config.read(config_path):
        raise RuntimeError(f"Failed to read config file at: {config_path}")

    try:
        api_key = config['weather']['api_key']
        station_id = config['weather']['station_id']
    except KeyError as e:
        raise RuntimeError(f"Missing config key: {e}")

    url = f"https://api.weather.com/v2/pws/observations/current?stationId={station_id}&format=json&units=e&apiKey={api_key}"

    with urllib.request.urlopen(url) as response:
        data = json.load(response)

    obs = data['observations'][0]
    precip_rate = obs['imperial']['precipRate']
    precip_total = obs['imperial']['precipTotal']

    print(f"⛆ {precip_total} in")
    print("---")
    print(f"Rate: {precip_rate} in/hr")

except Exception as e:
    error_output(str(e))
