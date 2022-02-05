from flask import Flask, render_template, request
import sys
from urllib import request as urlreq
import json

# api_key = sys.argv[1]
# print(api_key)

app = Flask(__name__)




# print(retrieval("524901", "fa", api_key))

@app.route("/", methods = ["GET", "POST"])
def Homepage():
    api_key = "9d50450a48809637b4862bdcb125927d"
    if request.method == "POST":
        city = request.form["button"]
        
        if city == "London":
            city_id = "2643743"
            language = "en"

        elif city == "Paris":
            city_id = "2988507"
            language = "fr"

        elif city == "New York":
            city_id = "5128581"
            language = "en"

        elif city == "Delhi":
            city_id = "2650225"
            language = "hi"

        elif city == "Tokyo":
            city_id = "1850147"
            language = "ja"


        data = urlreq.urlopen(f'http://api.openweathermap.org/data/2.5/weather?id={city_id}&units=metric&lang={language}&appid={api_key}').read()
        weather_data = json.loads(data)
        display_data = {
            "current_city": str(weather_data["name"]),
            "current_temp": str(weather_data["main"]["temp"])+" degrees C",
            "humidity": str(weather_data["main"]["humidity"]),
            "description": str(weather_data["weather"][0]["description"]),
            "min_temp": str(weather_data["main"]["temp_min"])+" degrees C",
            "max_temp": str(weather_data["main"]["temp_max"])+" degrees C"
        }
    else:
        display_data = None
    return render_template("index.html", display_data = display_data)

# def retrieval(city_id, language, api_key):


# @app.route("/<city>")
# def City(city):
#     return render_template("index.html", retrieval("524901", "fa", api_key))







if __name__ == "__main__":
    app.run(host="0.0.0.0", port="3009", debug=True)