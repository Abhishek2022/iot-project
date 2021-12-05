from flask import Flask, render_template, request
import json
import urllib.request

from jinja2.utils import urlize

app = Flask(__name__)

@app.route('/')
def index():
	city = "kolkata"
	api_key = "aa68e9cc745c091e290b5b054a659d88"

	coord = urllib.request.urlopen('https://api.openweathermap.org/geo/1.0/direct?q=' + city + '&limit=5&appid=' + api_key).read()
	lat_lon = json.loads(coord)
	lat=str(lat_lon[0]['lat'])
	lon=str(lat_lon[0]['lon'])


	source = urllib.request.urlopen('https://api.openweathermap.org/data/2.5/onecall?lat=' + lat + '&lon=' + lon + '&exclude=current,minutely,daily&appid='+api_key).read()
	list_of_data = json.loads(source)
	pop = list_of_data['hourly'][0]["pop"]

	print(pop)
	return render_template("index.html")

# @app.route('/weather', methods=['POST', 'GET'])
# def query():
# 	if(request.method == 'POST'):
# 		city = request.form['city']
# 		render_template('weather.html', {data})
# 	else:
# 		city = request.args.get('city')
# 		return render_template('weather.html',)


app.run(host='127.0.0.1', port=8000)