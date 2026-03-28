# weather_ny.py
import requests


def get_ny_weather():
    city = "New York"

    # Step 1: Get coordinates for New York City
    geo_url = "https://geocoding-api.open-meteo.com/v1/search"
    geo_params = {
        "name": city,
        "count": 1,
        "language": "en",
        "format": "json",
    }

    geo_res = requests.get(geo_url, params=geo_params, timeout=10)
    geo_res.raise_for_status()
    geo_data = geo_res.json()

    results = geo_data.get("results")
    if not results:
        print("City not found.")
        return

    place = results[0]
    lat = place["latitude"]
    lon = place["longitude"]
    name = place["name"]
    country = place.get("country", "")

    # Step 2: Get current weather
    weather_url = "https://api.open-meteo.com/v1/forecast"
    weather_params = {
        "latitude": lat,
        "longitude": lon,
        "current": "temperature_2m,relative_humidity_2m,wind_speed_10m",
        "timezone": "auto",
    }

    weather_res = requests.get(weather_url, params=weather_params, timeout=10)
    weather_res.raise_for_status()
    weather_data = weather_res.json()

    current = weather_data.get("current", {})

    print(f"Weather for {name}, {country}")
    print(f"Time: {current.get('time')}")
    print(f"Temperature: {current.get('temperature_2m')} °C")
    print(f"Humidity: {current.get('relative_humidity_2m')} %")
    print(f"Wind Speed: {current.get('wind_speed_10m')} km/h")


if __name__ == "__main__":
    get_ny_weather()