import configparser

config = configparser.ConfigParser()
config['url'] = {
	'API_URL' : 'https://data.weather.gov.hk/weatherAPI/opendata/weather.php?dataType=rhrread&lang=en',
}
config['data'] = {
		'rainfall' : ['Wan Chai'],
		'temperature' : ['Happy Valley']
}

with open('config.ini', 'w') as configfile:
	config.write(configfile)