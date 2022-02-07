from flask import Flask, render_template, request
import sys
from urllib import request as urlreq
import json

#initialising web-app
app = Flask(__name__)

#specifying the url for the below code and assigning http methods
@app.route("/", methods = ["GET", "POST"])
def Homepage():
    #Request details written as a dictionary so they can be selected depending on the queried city
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
    api_key = sys.argv[1]
    if request.method == "POST":
        city = request.form["city_select"]
        #below requests data from the weather api, converts it into a JSON object, relevant parts of which can then be displayed on the html
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
        #if no post request (opening the page for the 1st time), no data is returned
        display_data = None
    return render_template("index.html", display_data = display_data)

if __name__ == "__main__":
    #if the app is run directly, changes to the code can be made without killing the session
    app.run(debug=True)