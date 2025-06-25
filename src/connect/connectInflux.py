import influxdb_client as client
import configparser


def load_config(path='config.ini'):
    config = configparser.ConfigParser()
    config.read(path)
    return config

def client_influx(config):
    return InfluxDBClient(
        url=config['influx']['url'],
        token=config['influx']['token'],
        org=config['influx']['org']
    )