import influxdb_client as client
import configparser


config = configparser.ConfigParser()
config.read('src\connect\config.ini')
  
client_influx = client.InfluxDBClient(
            url=config['influx']['url'],
            token= config['influx']['token'],
            org=config['influx']['org'])