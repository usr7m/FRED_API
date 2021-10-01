import os
import glob
import pandas as pd 
import requests
import ast

class API():
	def __init__(self):
		print('FRED API')
		self.load_key()
		#
	def load_key(self):
		f=open('FRED_API_key')
		lines=f.readlines()
		key = lines[2]
		key = key[:-1]
		f.close()
		print(key)
		self.key = key
		return self.key
		#
	def observations(self, series):
		resp = requests.get('https://api.stlouisfed.org/fred/series/observations?series_id=' +\
							series +\
							'&realtime_start=1980-01-01' +\
							'&realtime_end=9999-12-31' +\
							'&api_key=' + self.key +\
							'&file_type=json')
		pd.DataFrame.from_dict(resp.json())
		data = pd.DataFrame(resp.json())
		data = data['observations'].apply(pd.Series)
		# data.index = pd.to_datetime(data['date'])
		data['value'] = pd.to_numeric(data['value'], errors = 'coerce')
		return data
	def search(self, search):
		resp = requests.get('https://api.stlouisfed.org/fred/series/search?search_text=' +\
							search +\
							'&api_key=' + self.key +\
							'&file_type=json')
		resp = resp.text
		resp = ast.literal_eval(resp)
		data = pd.DataFrame(resp)['seriess'].apply(pd.Series)
		return data
	
	
# usage:

# fred = API()

# fred.search('ICE AA YIELD')
# fred.observations('BAMLC0A1CAAAEY')
