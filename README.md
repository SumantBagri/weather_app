# WeatherApp

WeatherApp is a python application to log weather data using open data APIs

## Installation

Use the ansible installation [pipeline](https://github.com/SumantBagri/weather_app/blob/main/ansible/weather_app_pipeline.yml) to install the required dependancies as well as the package itself on a remote host. The remote hosts can be specified [here](https://github.com/SumantBagri/weather_app/blob/main/ansible/inventory/hosts). (Requires [ansible](https://docs.ansible.com/ansible/latest/installation_guide/intro_installation.html) to be installed). In order to install run:

```bash
$ansible-playbook weather_app_pipeline.yml -v
```

The required package files will be installed in the user's HOME directory

## Usage

```bash
$cd ~/weather_app/weatherapp
$wapp --help
```

By default, the logging level of the script is set to WARNING. However DEBUG level logging can be set as follows:

```bash
$wapp -ll 0
```

The above command creates two folders `data/` and `logs/` in the **weatherapp** folder. `data/` contains the logged weather data files for each day. `logs/` contains files with information regarding failed API requests and missing data (based on logging level).

By default, the installation will add jobs to crontab, to handle automatic script execution (Mon-Fri, every hour between 6am-6pm). Another job is added to cleanup older files which runs the [`cleanup.sh`](https://github.com/SumantBagri/weather_app/blob/main/weatherapp/cleanup.sh) script.


## Contributing

Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

## License

[MIT](https://choosealicense.com/licenses/mit/)
