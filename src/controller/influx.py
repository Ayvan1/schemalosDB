from  src.connect.connectInflux import client_influx as cli, config 
from src.model.record import Record
import influxdb_client as client
from src.model.alertData import AlertData

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
    query = 'from(bucket: "' + config['influx']['bucket'] + '''") |> range(start: -20m) |> timeShift(duration: 2h) |> filter(fn: (r) => 
    r._measurement == "temp" and
    r.sensor != "nct6776_auxtin" and
    r.sensor != "nct6776_cputin" and
    r.sensor != "nct6776_pch_chip_temp" and
    r.sensor != "nct6776_pch_cpu_temp" and
    r.sensor != "nct6776_pch_mch_temp" and
    r.sensor != "nct6776_peci_agent_0" and
    r.sensor != "nct6776_systin"
  )'''
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

    org_api = cli.organizations_api()
    orgs = org_api.find_organizations()
    org_entity = None
    for org in orgs:
        if org.name == config['influx']['org']:
            org_entity = org 

    buckets_api = client.BucketsApi(cli)
    buckets =  buckets_api.find_bucket_by_name("alert")
    if(buckets is None):
        buckets_api.create_bucket(bucket_name="alert",org=config['influx']['org'],retention_rules=None)


    query = 'from (bucket:"'+ config['influx']['bucket'] +'''") |> range(start: task.start)
      |> filter(fn: (r) => r._measurement == "temp")
      |> filter(fn: (r) => 
            r.sensor != "nct6776_auxtin" and
            r.sensor != "nct6776_cputin" and
            r.sensor != "nct6776_pch_chip_temp" and
            r.sensor != "nct6776_pch_cpu_temp" and
            r.sensor != "nct6776_pch_mch_temp" and
            r.sensor != "nct6776_peci_agent_0" and
            r.sensor != "nct6776_systin"
        )''' +  f'|> filter(fn: (r) => r._value >= {limit_temperature})' +'''
      |> drop(columns: ["host"])
      |> map(fn: (r) => ({
          _time: r._time,
          _value: r._value,
          _field: "temperature_alert",
          _measurement: "alert_temp",
          sensor: r.sensor
      }))
      |> to(bucket:"alert")'''
    try:
        task_api = cli.tasks_api()
        print("test")        
        task = task_api.create_task_every(name="HighTempAlert",every="30s",flux=query,organization=org_entity)
        print(type(task))
        return {"message": "Task created","task_id":task.id}
    except Exception as e:
        return {"error": str(e)}
    

def get_alert():
    query = 'from(bucket:"alert") |> range(start:0) |> timeShift(duration: 2h)'
    tables  = cli.query_api().query(query,org=config['influx']['org'])
    result = []
    for table in tables:
        for record in table.records:
            print(record)
            result.append(AlertData(
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