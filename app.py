from flask import Flask, render_template, request
import sys
from urllib import request as urlreq
import json

app = Flask(__name__)

@app.route("/", methods = ["GET", "POST"])
def Homepage():
    reqs = {
        "London":{
            "city_id":"2643743",
            "language":"en"
        },
        "Paris":{
            "city_id":"2988507",
            "language":"fr"
        },
        "New York":{
            "city_id":"5128581",
            "language":"en"
        },
        "Delhi":{
            "city_id":"2650225",
            "language":"hi"
        },
        "Tokyo":{
            "city_id":"1850147",
            "language":"ja"
        },
    }
    api_key = "9d50450a48809637b4862bdcb125927d"
    if request.method == "POST":
        city = request.form["city_select"]
        data = urlreq.urlopen(f'http://api.openweathermap.org/data/2.5/weather?id={reqs[city]["city_id"]}&units=metric&lang={reqs[city]["language"]}&appid={api_key}').read()
        weather_data = json.loads(data)
        display_data = {
            "current_city": str(weather_data["name"]),
            "current_temp": str(weather_data["main"]["temp"])+"°C",
            "humidity": str(weather_data["main"]["humidity"])+r"%",
            "description": str(weather_data["weather"][0]["description"]),
            "min_temp": str(weather_data["main"]["temp_min"])+"°C",
            "max_temp": str(weather_data["main"]["temp_max"])+"°C"
        }
    else:
        display_data = None
    return render_template("index.html", display_data = display_data)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5001", debug=True)