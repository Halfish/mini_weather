"""
Author: Bruce
"""
import json

from flask import Flask, render_template
from werkzeug.exceptions import HTTPException

from weather_api import SevenTimerWeatherApi

app = Flask(__name__)


CITY_COOR = {
    "beijing": [116.411168, 39.912943],
    "shanghai": [121.47824, 31.236176],
    "guangzhou": [113.273082, 23.136732],
    "shenzhen": [114.072789, 22.551624],
}

@app.errorhandler(404)
def page_not_found(error):
    return 'This page does not exist', 404

@app.errorhandler(HTTPException)
def handle_exception(e):
    """Return JSON instead of HTML for HTTP errors."""
    # start with the correct headers and status code from the error
    response = e.get_response()
    # replace the body with JSON
    response.data = json.dumps({
        "code": e.code,
        "name": e.name,
        "description": e.description,
    })
    response.content_type = "application/json"
    return response


@app.route("/hello", methods=["GET"])
def hello():
    return "<p>hello</p>";


@app.route("/weather/<city>", methods=["GET"])
def weather_7timer(city: str):
    city = city.lower()
    if city not in CITY_COOR:
        return 'City not supported', 401
    lon, lat = CITY_COOR[city]
    api = SevenTimerWeatherApi()
    dataset = api.get_weather_data(lon, lat)
    return render_template('index.html', city=city, dataset=dataset)
