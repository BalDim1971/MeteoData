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

        data = {"daily": []}
        daily = []
        for day in range(len(response_json['daily']['time'])):
            one_day = {
                "date": str(response_json['daily']['time'][day]),
                "temp_min": str(
                    response_json['daily']['temperature_2m_min'][day]),
                "temp_max": str(
                    response_json['daily']['temperature_2m_max'][day]),
                "precipitation": str(
                    response_json['daily']['precipitation_sum'][day])
            }
            daily.append(one_day)
        data["daily"] = daily

        return render_template('index.html', city=city_name,
                               data=data["daily"])
    else:
        print(f"Ошибка {response.status_code}: {response.text}")
        return render_template('/')


if __name__ == '__main__':
    app.run(debug=True)
