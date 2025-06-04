# PWS Weather Fetcher

A Python script to fetch current weather data (e.g., precipitation rate and accumulation) from a Weather Underground PWS API.

## Setup

1. Clone this repo:
   ```bash
   git clone https://github.com/yourname/pws-extractor.git
   cd pws-extractor
   ```

2. Copy the example configuration file and fill in your API key and station ID:
   ```bash
   cp weather.conf.example weather.conf
   ```

   Then edit `weather.conf`:
   ```ini
   [weather]
   api_key = your_api_key_here
   station_id = your_station_id_here
   ```

3. Set up a virtual environment and install dependencies (use the Makefile for convenience):
   ```bash
   make setup
   ```

4. Run the script:
   ```bash
   make run
   ```

5. To remove the virtual environment and Python cache files:
   ```bash
   make clean
   ```

## Requirements

- Python 3.7+
- Access to a Weather Underground API key
- `make` (available on macOS/Linux or via GNU Make on Windows)

## Notes

- `weather.conf` contains sensitive configuration like your API key and is ignored via `.gitignore`.
- `weather.conf.example` is a safe placeholder for others to copy and customize.
