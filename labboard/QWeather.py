#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# @author: InTereSTingHE

import requests

url_api_weather = 'https://devapi.qweather.com/v7/weather/'
url_api_geo = 'https://geoapi.qweather.com/v2/city/'
url_api_rain = 'https://devapi.qweather.com/v7/minutely/5m'
url_api_air = 'https://devapi.qweather.com/v7/air/now'

class QWeather:
    def __init__(self, key):
        self._key = '&key=' + key

    def get(self, api_type, city_id):
        url = url_api_weather + api_type + '?location=' + city_id + self._key
        return requests.get(url).json()

    def rain(self, lat, lon):
        url = url_api_rain  + '?location=' + lat + ',' + lon + self._key
        return requests.get(url).json()

    def air(self, city_id):
        url = url_api_air + '?location=' + city_id + self._key
        return requests.get(url).json()

    def get_city(self, city_kw):
        url_v2 = url_api_geo + 'lookup?location=' + city_kw + self._key
        return requests.get(url_v2).json()['location']

    def now(self, city_id):
        return self.get('now', city_id)

    def daily(self, city_id):
        return self.get('3d', city_id)

    def hourly(self, city_id):
        return self.get('24h', city_id)