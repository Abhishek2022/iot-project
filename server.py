from flask import Flask, render_template, request, Response
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
from datetime import datetime
import time
import random
import json
import urllib.request

from jinja2.utils import urlize

app = Flask(__name__)

temp_val = 0
moisture_val = 0

def iot_handler(self, params, packet):
	print(packet.topic)
	print((packet.payload))
	json_data = json.loads(packet.payload)
	global temp_val, moisture_val
	temp_val = float(json_data["temperature"])
	moisture_val = float(json_data["moisture"])
	print(temp_val)
 
myMQTTClient = AWSIoTMQTTClient("random-client") #random key, if another connection using the same key is opened the previous one is auto closed by AWS IOT
myMQTTClient.configureEndpoint("a1r149u415pa4r-ats.iot.us-east-2.amazonaws.com", 8883)
myMQTTClient.configureCredentials("root-ca.pem", "private.pem.key", "certificate.pem.crt")

myMQTTClient.configureOfflinePublishQueueing(-1) # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2) # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10) # 10 sec
# myMQTTClient.configureMQTTOperationTimeout(5) # 5 sec
print ('Connecting to AWS IoT Core....')

myMQTTClient.connect()
myMQTTClient.subscribe("test", 1, iot_handler)


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
	return render_template("chart-handler.html")

@app.route('/temp_handler')
def temp_handler():
	def generate_data(): 
		while True:
			json_data = json.dumps(
					{'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': temp_val})
			yield f"data:{json_data}\n\n"
			time.sleep(1)
	return Response(generate_data(), mimetype='text/event-stream')


@app.route('/moisture_handler')
def moisture_handler():
	def generate_data(): 
		while True:
			json_data = json.dumps(
					{'time': datetime.now().strftime('%Y-%m-%d %H:%M:%S'), 'value': moisture_val})
			yield f"data:{json_data}\n\n"
			time.sleep(1)
	return Response(generate_data(), mimetype='text/event-stream')

# @app.route('/weather', methods=['POST', 'GET'])
# def query():
# 	if(request.method == 'POST'):
# 		city = request.form['city']
# 		render_template('weather.html', {data})
# 	else:
# 		city = request.args.get('city')
# 		return render_template('weather.html',)


app.run(host='127.0.0.1', port=8000, debug=True, threaded=True)