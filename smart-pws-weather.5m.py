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

def direction_from_degrees(degrees):
    directions = [
        "N", "NNE", "NE", "ENE", "E", "ESE", "SE", "SSE",
        "S", "SSW", "SW", "WSW", "W", "WNW", "NW", "NNW"
    ]
    idx = int((degrees + 11.25) % 360 / 22.5)
    return directions[idx]

def dew_point_feel_emoji(dewpt):
    if dewpt < 50:
        return "🏜️ Dry"
    elif dewpt < 60:
        return "😊 Comfortable"
    elif dewpt < 66:
        return "😐 Humid"
    elif dewpt < 71:
        return "😓 Muggy"
    elif dewpt < 76:
        return "🥵 Oppressive"
    else:
        return "🔥 Miserable"

def uv_index_emoji(uv):
    if uv is None:
        return "🌑 UV: –"
    if uv <= 2:
        return f"🌑 UV: {uv} (Low)"
    elif uv <= 5:
        return f"🌤️ UV: {uv} (Moderate)"
    elif uv <= 7:
        return f"☀️ UV: {uv} (High)"
    elif uv <= 10:
        return f"🔆 UV: {uv} (Very High)"
    else:
        return f"🧴 UV: {uv} (Extreme)"

def wind_emoji(speed, gust):
    if gust and gust >= 25:
        return "🌪️ Gusty"
    elif speed >= 15:
        return "🌬️ Windy"
    elif speed >= 5:
        return "💨 Breezy"
    else:
        return "🍃 Calm"

def pressure_trend(current_pressure, storage_path):
    try:
        with open(storage_path, "r") as f:
            prev = float(f.read().strip())
        trend = "↗️ Rising" if current_pressure > prev else "↘️ Falling" if current_pressure < prev else "→ Steady"
    except Exception:
        trend = "↔️ Unknown"
    try:
        with open(storage_path, "w") as f:
            f.write(str(current_pressure))
    except Exception:
        pass
    return trend

try:
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
    imp = obs['imperial']

    precip_rate = imp['precipRate']
    precip_total = imp['precipTotal']
    wind_speed = imp['windSpeed']
    wind_gust = imp['windGust']
    wind_dir = obs['winddir']
    temp = imp['temp']
    dewpt = imp['dewpt']
    heat_index = imp.get('heatIndex')
    wind_chill = imp.get('windChill')
    uv = obs.get('uv')
    pressure = imp.get('pressure')

    output = ""
    submenu = []

    if precip_rate > 0:
        output = f"⛆ {precip_total} in"
        submenu = [f"Rate: {precip_rate} in/hr"]
    elif wind_speed >= 10 or (wind_gust and wind_gust >= 15):
        dir_txt = direction_from_degrees(wind_dir)
        emoji = wind_emoji(wind_speed, wind_gust)
        output = f"{emoji} {wind_speed} mph {dir_txt}"
        submenu = [f"Gusts: {wind_gust or '–'} mph"]
    elif heat_index and heat_index > temp + 3:
        output = f"🥵 {heat_index}°F"
        submenu = [f"Actual: {temp}°F", uv_index_emoji(uv)]
    elif wind_chill and wind_chill < temp - 3:
        output = f"🥶 {wind_chill}°F"
        submenu = [f"Actual: {temp}°F", f"Wind: {wind_speed} mph"]
    else:
        comfort = dew_point_feel_emoji(dewpt)
        output = f"🌡️ {temp}°F"
        submenu = [f"{comfort} dew point: {dewpt}°F", f"💧 Humidity: {obs['humidity']}%", uv_index_emoji(uv)]

    if pressure is not None:
        trend = pressure_trend(pressure, script_dir / ".pressure")
        if trend not in ('→ Steady', '↔️ Unknown'):
            submenu.append(f"⏱️ Pressure: {pressure:.2f} inHg {trend}")

    print(output)
    print("---")
    for line in submenu:
        print(line)

except Exception as e:
    error_output(str(e))
