import requests
import logging
import traceback
import csv
import os
import configparser
import argparse
import time
from datetime import datetime


class WeatherApp:
	def __init__(self):
		# Initialize data dictionary
		self.data_dict = {}
		# Initialize directories
		self.makedirs()
		# Read default configuration file for api url
		self.config = configparser.ConfigParser()
		self.config.read('../config.ini')
		self.api_url = self.config['url']['api_url']

		# Create logger instance and setup argparser
		self.logger = self._setuplogger()
		parser = argparse.ArgumentParser(description='Gather weather data.')
		parser.add_argument('-ll', '--logging-level', dest='loglevel', default=2, type=int,
							help="Specify the level of logging messages \n \
								  0=DEBUG \n\
								  2=WARNING (default)")
		args = parser.parse_args()
		if args.loglevel == 0: self.logger.setLevel(logging.DEBUG)

	def makedirs(self):
		if not os.path.isdir("data/"): os.mkdir("data")
		if not os.path.isdir("logs/"): os.mkdir("logs")

	def _setuplogger(self):
		file = 'logs/' + datetime.today().strftime("%d-%m-%Y") + '.log'
		if not os.path.exists(file):
			with open(file, 'w'): pass

		logger = logging.getLogger(__name__)
		logger.setLevel(logging.WARNING)

		# Define file handler and set formatter
		fh = logging.FileHandler(file, mode='a')
		formatter = logging.Formatter('|%(asctime)s| %(levelname)s : %(message)s')
		fh.setFormatter(formatter)

		# Add file handler to logger
		logger.addHandler(fh)

		return logger

	def get_data(self):
		# Ping url for weather data and check the response status code
		trials = 3
		while trials:
			trials -= 1
			response = requests.get(self.api_url)
			if response.ok:
				response = response.json()
				self.logger.info("API response received successfully!")
				break
			else:
				self.logger.error('API returned {} status code ({} trials remaining)'.format(response.status_code, trials))
				if trials == 0:
					self.logger.critical("URL not reachable (api unresponsive).")
					return
			# Wait for a while before pinging again
			time.sleep(3) 

		now = datetime.now().strftime("%H:%M:%S")
		self.data_dict['Time'] = now

		place_dict = {}
		for attr in self.config['data']:
			place_dict[attr] = [ data['place'] for data in response[attr]['data'] ]
			for place in self.config['data'][attr].strip("][").split(', '):
				place = place.strip("'")
				col_name = place + " " + attr
				try:
					place_ind = place_dict[attr].index(place)
				except ValueError as e:
					self.logger.warning('Missing temperature data for {}.'.format(place))
					self.data_dict[col_name] = 'na'
				else:
					if attr == 'rainfall':
						self.data_dict[col_name] = response['rainfall']['data'][place_ind]['max']
					elif attr == 'temperature':
						self.data_dict[col_name] = response['temperature']['data'][place_ind]['value']
					else:
						self.data_dict[col_name] = 'field_not_found'

	def log_data(self):
		date = datetime.today().strftime("%d-%m-%Y")
		csv_file = 'data/' + str(date) + '.csv'

		if not os.path.exists(csv_file):
			self.logger.info("Creating data file!")
			with open(csv_file, 'w') as f:
				writer = csv.DictWriter(f, fieldnames=list(self.data_dict.keys()))
				writer.writeheader()
				self.logger.info("Appending to data file")
				writer.writerow(self.data_dict)
		else:
			with open(csv_file, 'a') as f:
				writer = csv.DictWriter(f, fieldnames=list(self.data_dict.keys()))
				self.logger.info("Appending to data file")
				writer.writerow(self.data_dict)

		self.logger.info("Data logging completed")

def run():
	weather_app = WeatherApp()
	weather_app.get_data()
	weather_app.log_data()

if __name__ == '__main__':
	weather_app = WeatherApp()
	weather_app.get_data()
	weather_app.log_data()

