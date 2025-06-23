from  src.connect.connectInflux import client_influx as cli, config 
from src.model.record import Record
import influxdb_client as client
import random

def _get_sensor_name(index:int):
    match(index):
        case 1:
            return "coretemp_core_0"
        case 2:
            return "coretemp_core_1"
        case 3:
            return "coretemp_core_2"
        case 4: 
            return "coretemp_core_3"
        case 5:
            return "coretemp_package_id_0"
        case _:
            return None

def  read_all_temperature():
    query = 'from(bucket: "' + config['influx']['bucket'] + '") |> range(start: -11d)'
    tables = cli.query_api().query(query, org=config['influx']['org'])
    result = []
    
    for table in tables:
        for record in table.records:
            result.append(Record(
                host=record.values.get("host"),
                sensor_name= record.values.get("sensor"),
                temperature= record.get_value(),
                time= record.get_time().isoformat()
            ))
    return result

def create_task(limit_temperature:int):

    buckets_api = client.BucketsApi(cli)
    buckets =  buckets_api.find_bucket_by_name("alert")
    if(buckets is None):
        buckets_api.create_bucket(bucket_name="alert",org=config['influx']['org'],retention_rules=None)

    query = '''

        option task = {{
            name: "high_temp_alert",
            every: 10s
        }}

    ''' + 'from (bucket:"'+ config['influx']['bucket'] +'''") |> range(start: -1m)
      |> filter(fn: (r) => r._measurement == "temp")
      |> filter(fn: (r) => r._field == "temp")''' + f'|> filter(fn: (r) => r._value > {limit_temperature})' +'''
      |> map(fn: (r) => ({{
          _time: r._time,
          _value: r._value,
          _field: "temperature_alert",
          _measurement: "alerts",
          sensor_name: r.sensor_name,
          host: r.host
      }}))''' + '''
      |> to(bucket:"alert")'''
    try:
        task_api = cli.tasks_api()
        task = task_api.create_task_every(name="HighTempAlert",every="10s",flux=query)
        print({"message": "Task created", "task_id": task.id})
    except Exception as e:
        return {"error": str(e)}
    

def get_alert():
    query = 'from(bucket:"alert' + f'") |> range(start:-10s)'
    tables  = cli.query_api().query(query,org=config['influx']['org'])
    result = []
    for table in tables:
        for record in table.records:
            result.append(Record(
                host=record.values.get("host"),
                sensor_name= record.values.get("sensor"),
                temperature= record.get_value(),
                time= record.get_time().isoformat()
            ))
    return result

def read_all_temperature_by_time(time:str):
    query = 'from(bucket:"' + config['influx']['bucket'] + f'") |> range(start:{time})'
    tables  = cli.query_api().query(query,org=config['influx']['org'])
    result = []
    for table in tables:
        for record in table.records:
            result.append(Record(
                host=record.values.get("host"),
                sensor_name= record.values.get("sensor"),
                temperature= record.get_value(),
                time= record.get_time().isoformat()
            ))
    return result

def read_temperature_from_a_sensor(sensor_index:int):
    query = f'from(bucket:"{str(config["influx"]["bucket"])}") |> range(start:-1h) |> filter(fn: (r) => r.sensor == "{_get_sensor_name(sensor_index)}")'
    tables  = cli.query_api().query(query,org=config['influx']['org'])
    result = []
    for table in tables:
        for record in table.records:
            result.append(Record(
                host=record.values.get("host"),
                sensor_name= record.values.get("sensor"),
                temperature= record.get_value(),
                time= record.get_time().isoformat()
            ))
    return result

def read_temperature_from_a_sensor_by_time(sensor_index:int,time:str):
    query = f'from(bucket:"{str(config["influx"]["bucket"])}") |> range(start:{time}) |> filter(fn: (r) => r.sensor == "{_get_sensor_name(sensor_index)}")'
    tables  = cli.query_api().query(query,org=config['influx']['org'])
    result = []
    for table in tables:
        for record in table.records:
            result.append(Record(
                host=record.values.get("host"),
                sensor_name= record.values.get("sensor"),
                temperature= record.get_value(),
                time= record.get_time().isoformat()
            ))
    return result