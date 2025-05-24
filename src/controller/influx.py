from  src.connect.connectInflux import client_influx as cli, config 
from src.model.record import Record

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
    query = 'from(bucket: "' + config['database']['bucket'] + '") |> range(start: -20s)'
    tables = cli.query_api().query(query, org=config['database']['org'])
    result = []
    for  table in tables:
        for record in table.records:
            result.append(Record(
                host=record.values.get("host"),
                sensor_name= record.values.get("sensor"),
                temperature= record.get_value(),
                time= record.get_time().isoformat()
            ))
    return result

def read_all_temperature_by_time(time:str):
    query = 'from(bucket:"' + config['database']['bucket'] + f'") |> range(start:{time})'
    tables  = cli.query_api().query(query,org=config['database']['org'])
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
    query = f'from(bucket:"{str(config["database"]["bucket"])}") |> range(start:-1h) |> filter(fn: (r) => r.sensor == "{_get_sensor_name(sensor_index)}")'
    tables  = cli.query_api().query(query,org=config['database']['org'])
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
    query = f'from(bucket:"{str(config["database"]["bucket"])}") |> range(start:{time}) |> filter(fn: (r) => r.sensor == "{_get_sensor_name(sensor_index)}")'
    tables  = cli.query_api().query(query,org=config['database']['org'])
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