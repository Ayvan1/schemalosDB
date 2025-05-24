import influxdb_client as client
import configparser


config = configparser.ConfigParser()
config.read('src\connect\config.ini')
  
client_influx = client.InfluxDBClient(
            url=config['database']['url'],
            token= config['database']['token'],
            org=config['database']['org'])