#!/usr/bin/python
# Get current forecast from forecast.io using lat/long
# Kevin Hinds http://www.kevinhinds.com
# License: GPL 2.0
import time, json, string, cgi, subprocess
import includes.data as data
import includes.settings as settings
import info.WeatherDetails as WeatherDetails
import includes.settings as settings

# remove old file and start logging weather
data.removeJSONFile('weather.data')
while True:
    try:

        # get current forecast from location
        weatherInfo = json.loads(subprocess.check_output(['curl', 'https://api.forecast.io/forecast/' + settings.weatherAPIKey + '/' + str(settings.latitude) + ',' + str(settings.longitude) + '?lang=en']))
        hourlyConditions = weatherInfo['minutely']
        currentConditions = weatherInfo['currently']
        
        # gather info in serializable object to store as JSON file
        weatherDetails = WeatherDetails.WeatherDetails()
        weatherDetails.time = int(currentConditions['time'])
        weatherDetails.summary = str(currentConditions['summary'])
        weatherDetails.nextHour = str(hourlyConditions['summary'])
        weatherDetails.icon = str(currentConditions['icon'])
        weatherDetails.apparentTemperature = float(currentConditions['apparentTemperature'])
        weatherDetails.humidity = float(currentConditions['humidity'])
        weatherDetails.precipIntensity = float(currentConditions['precipIntensity'])
        weatherDetails.precipProbability = float(currentConditions['precipProbability'])
        weatherDetails.windSpeed = float(currentConditions['windSpeed'])

        # create or rewrite data to weather data file as JSON, then wait 5 minutes
        data.saveJSONObjToFile('weather.data', weatherDetails)
        time.sleep(300)
        
    except (Exception):
        time.sleep(30)
