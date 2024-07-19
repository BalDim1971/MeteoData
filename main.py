from flask import Flask, render_template, request
import requests
from geopy.geocoders import Nominatim


def get_geo_data(city):
    geolocator = Nominatim(user_agent="MeteoData")
    location = geolocator.geocode(city)
    return location


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def weather():
    if request.method == 'POST':
        city_name = request.form['city']
    else:
        city_name = 'Москва'
    
    geo = get_geo_data(city=city_name)
    params = {
        "latitude": geo.latitude,
        "longitude": geo.longitude,
        "daily": "temperature_2m_min,temperature_2m_max,precipitation_sum",
        "timezone": "Europe/Moscow"
    }
    response = requests.get("https://api.open-meteo.com/v1/forecast",
                            params=params)
    
    if response.status_code == 200:
        response_json = response.json()
        data = {
            "cityname": city_name,
            "temp_min": str(response_json['daily']['temperature_2m_min'][0]),
            "temp_max": str(response_json['daily']['temperature_2m_max'][0]),
        }
        # Поскольку индекс 0 представляет собой данные на текущий день,
        # индекс 1 будет представлять данные на завтра
        tomorrow_temp_min = response_json['daily']['temperature_2m_min'][1]
        tomorrow_temp_max = response_json['daily']['temperature_2m_max'][1]
        tomorrow_precipitation = response_json['daily']['precipitation_sum'][1]
        
        print(f"Прогноз погоды в {city_name} на завтра:")
        print(f"Минимальная температура: {tomorrow_temp_min}°C")
        print(f"Максимальная температура: {tomorrow_temp_max}°C")
        print(f"Ожидаемое количество осадков: {tomorrow_precipitation} мм")
        return render_template('index.html', data=data)
    else:
        print(f"Ошибка {response.status_code}: {response.text}")
        return render_template('/')


if __name__ == '__main__':
    app.run(debug=True)
