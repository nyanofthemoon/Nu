import requests
from nu.modules.config import query_config

queryConfig = query_config()


class WeatherForecastApi:

    def __init__(self, key, location):
        self.key = key
        self.setLocation(location)

    def setLocation(self, location):
        self.location = location

    def current(self):
        response = self._current()
        data = 'unknown'
        if response != None:
            data = str(int(response['main']['temp'])) + ' Celsius with ' + response['weather'][0]['description']
        return data

    def forecastToday(self):
      response = self._forecast()
      data = 'unknown'
      if response != None:
          data = response['list'][0]['weather'][0]['description'] + ' with a minimum of ' + str(int(response['list'][0]['main']['temp_min'])) + ' and a maximum of ' + str(int(response['list'][0]['main']['temp_max'])) + ' Celsius'
      return data

    def forecastTomorrow(self):
      response = self._forecast()
      data = 'unknown'
      if response != None:
          data = response['list'][1]['weather'][0]['description'] + ' with a minimum of ' + str(int(response['list'][1]['main']['temp_min'])) + ' and a maximum of ' + str(int(response['list'][1]['main']['temp_max'])) + ' Celsius'
      return data

    # http://api.openweathermap.org/data/2.5/weather?q=Montreal&units=metric&APPID=f4b293fa455d861843e2afb0acd35852
    def _current(self):
        req = requests.get('http://api.openweathermap.org/data/2.5/weather?q=' + self.location + '&units=metric&APPID=' + self.key)
        if req.status_code == requests.codes.ok:
            return req.json()
        else:
            return None

    # http://api.openweathermap.org/data/2.5/forecast?q=Montreal&units=metric&APPID=f4b293fa455d861843e2afb0acd35852
    def _forecast(self):
        req = requests.get('http://api.openweathermap.org/data/2.5/forecast?q=' + self.location + '&units=metric&APPID=' + self.key)
        if req.status_code == requests.codes.ok:
            return req.json()
        else:
            return None


WeatherForecast = WeatherForecastApi(queryConfig.get('WeatherForecast', 'apiKey'), queryConfig.get('WeatherForecast', 'location'))
