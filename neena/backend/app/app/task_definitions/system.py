from dataclasses import dataclass
from app.execution.decorators import Task
import requests
from urllib.parse import quote
import datetime


@dataclass
class Coordinates:
    lat: float
    long: float


@Task
def get_temperature(coords: Coordinates) -> float:
    """Gets current temperature in Celsius"""
    
    base_url = "https://api.open-meteo.com/v1/forecast"
    params = {
        'latitude': coords.lat,
        'longitude': coords.long,
        'hourly': 'temperature_2m'  # getting hourly temperature at 2m above the ground level
    }
    response = requests.get(base_url, params=params)
    weather_data = response.json()
    
    current_date = datetime.date.today()
    time_data = weather_data['hourly']['time']
    temperature_data = weather_data['hourly']['temperature_2m']
    time_data_current_day = [time for time in time_data if datetime.date.fromisoformat(time[:10]) == current_date][-1]
    temperature_data_current_day = temperature_data[:len(time_data_current_day)][-1]
    
    print(f"At {time_data_current_day}, the temperature is {temperature_data_current_day}°C.")
    
    return temperature_data_current_day


@Task
def get_lat_lon_for_city(city: str) -> Coordinates:
    """Gets latitude and longtitude for given city"""
    base_url = f"https://nominatim.openstreetmap.org/search?city={quote(city)}&format=json"
    response = requests.get(base_url)
    data = response.json()

    if data:  # if data is not empty
        lat = data[0]['lat']  # latitude
        lon = data[0]['lon']  # longitude
        return Coordinates(lat, lon)
    else:
        print(f"Error: Location not found")  # print error message
        return None


@Task
def addition(a: float, b: float) -> float:
    """Adds two floats together.
    """
    return a + b
