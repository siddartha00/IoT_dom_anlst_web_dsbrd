#Simple Linear Regression with the Small Temperature dataset
from flask import Flask, render_template,request,abort
from geopy.geocoders import Nominatim
import urllib.request
import json


app = Flask(__name__)
@app.route('/')
def hello():
    return render_template('html.html')
@app.route('/weather')
def weather():
    api_key = 'd52d9455f88f7b7aa01126e1759d893f'
    if request.method == 'POST':
        city = request.form['city']
    else:
        #for default name mathura
        city = 'Vellore'
    geocode = Nominatim(user_agent="Weather")
    location =geocode.geocode(city)
    lat = location.latitude
    lon = location.longitude
    print(str(lat)+" "+str(lon))
    # source contain json data from api
    try:
        source = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/weather?q=' + city + '&appid='+api_key).read()
        print("hello! failure ovbeserved")
        prediction = urllib.request.urlopen('http://api.openweathermap.org/data/2.5/forecast?lat='+str(lat)+'&lon='+str(lon)+'&appid='+api_key).read()
    except:
        return abort(404)
    # converting json data to dictionary

    list_of_data = json.loads(source)
    prediction_data = json.loads(prediction)
    # data for variable list_of_data
    def te_cel(temp):
        return str(int(temp-273.15))
    data = {
        "country_code": str(list_of_data['sys']['country']),
        "coordinate": str(list_of_data['coord']['lon']) + ' ' + str(list_of_data['coord']['lat']),
        "temp_feel": te_cel(list_of_data['main']['feels_like']) + 'C',
        "temp": te_cel(list_of_data['main']['temp']) + 'C',
        "temp_min": te_cel(list_of_data['main']['temp_min']) + 'C',
        "temp_max": te_cel(list_of_data['main']['temp_max']) + 'C',
        "pressure": str(list_of_data['main']['pressure']),
        "humid": str(list_of_data['main']['humidity']),
        "predicted_weather": [
            str(prediction_data['list'][0]['weather'][0]['description']),
            str(prediction_data['list'][1]['weather'][0]['description']),
            str(prediction_data['list'][2]['weather'][0]['description']),
            str(prediction_data['list'][3]['weather'][0]['description']),
            str(prediction_data['list'][4]['weather'][0]['description']),
        ],
        "max_temp": [
            te_cel(prediction_data['list'][0]['main']['temp_max']),
            te_cel(prediction_data['list'][1]['main']['temp_max']),
            te_cel(prediction_data['list'][2]['main']['temp_max']),
            te_cel(prediction_data['list'][3]['main']['temp_max']),
            te_cel(prediction_data['list'][4]['main']['temp_max']),
        ],
        "min_temp": [
            te_cel(prediction_data['list'][0]['main']['temp_min']),
            te_cel(prediction_data['list'][1]['main']['temp_min']),
            te_cel(prediction_data['list'][2]['main']['temp_min']),
            te_cel(prediction_data['list'][3]['main']['temp_min']),
            te_cel(prediction_data['list'][4]['main']['temp_min']),
        ],
        "humidity": [
            str(prediction_data['list'][0]['main']['humidity']),
            str(prediction_data['list'][1]['main']['humidity']),
            str(prediction_data['list'][2]['main']['humidity']),
            str(prediction_data['list'][3]['main']['humidity']),
            str(prediction_data['list'][4]['main']['humidity']),
        ],
        "pre":[
            str(prediction_data['list'][0]['pop']),
            str(prediction_data['list'][1]['pop']),
            str(prediction_data['list'][2]['pop']),
            str(prediction_data['list'][3]['pop']),
            str(prediction_data['list'][4]['pop']),
        ],
        "time":[
            str(prediction_data['list'][0]['dt_txt']),
            str(prediction_data['list'][1]['dt_txt']),
            str(prediction_data['list'][2]['dt_txt']),
            str(prediction_data['list'][3]['dt_txt']),
            str(prediction_data['list'][4]['dt_txt']),
        ],
        "cityname":str(city),
    }
    print(data)
    return render_template('weather.html',data=data)
@app.route('/door')
def dashboard():
    return render_template('door.html')
@app.route('/lobby')
def lobby():
    return render_template('lobby.html')
@app.route('/room')
def room():
    return render_template('room.html')
@app.route('/home')
def home():
    return render_template('html.html')
if __name__ == '__main__':
    app.run(debug= True, host="0.0.0.0", port=5000)