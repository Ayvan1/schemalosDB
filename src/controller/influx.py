from  src.connect.connectInflux import client_influx as cli, config 
from  influxdb_client import TaskCreateRequest
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
    query = f'''
        import "timezone"
        option location = timezone.location(name: "Europe/Paris")
        from(bucket: "{config['influx']['bucket']}") 
            |> range(start: -20m) 
            |> filter(fn: (r) => 
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

def create_task(limit_temperature:float):

    org_api = cli.organizations_api()
    orgs = org_api.find_organizations()
    org_entity = None
    for org in orgs:
        if org.name == config['influx']['org']:
            org_entity = org 

    buckets_api = client.BucketsApi(cli)
    buckets =  buckets_api.find_bucket_by_name("alert")
    if buckets:
        buckets_api.delete_bucket(buckets)
        buckets_api.create_bucket(bucket_name="alert",org=config['influx']['org'],retention_rules=None)

    print(limit_temperature)
    query = f'''
        option task = {{name: "HighTempAlert", every: 10s}}
    
        from (bucket:"{config['influx']['bucket']}") |> range(start: -30s)
            |> filter(fn: (r) => r._measurement == "temp")
            |> filter(fn: (r) => float(v: r._value) >= {limit_temperature})
            |> filter(fn: (r) => 
                    r.sensor != "nct6776_auxtin" and
                    r.sensor != "nct6776_cputin" and
                    r.sensor != "nct6776_pch_chip_temp" and
                    r.sensor != "nct6776_pch_cpu_temp" and
                    r.sensor != "nct6776_pch_mch_temp" and
                    r.sensor != "nct6776_peci_agent_0" and
                    r.sensor != "nct6776_systin"
                )
            
            |> drop(columns: ["host"])
            |> map(fn: (r) => ({{
                _time: r._time,
                _value: r._value,
                _field: "temperature_alert",
                _measurement: "alerts",
                sensor: r.sensor
            }}))
            |> to(bucket:"alert",tagColumns: ["sensor"])'''
    try:
        task_api = cli.tasks_api()     
        tasks = task_api.find_tasks()
        for task in tasks:
            print(f"Delete task : {task.name} ({task.id})")
            task_api.delete_task(task.id)
        task_request = TaskCreateRequest(
            org_id=org_entity.id,
            flux=query,
            status="active"
        )
        task = task_api.create_task(task_request)
        return {"message": "Task created","task_id":task.id}
    except Exception as e:
        print(e)
        return {"error": str(e)}
    

def get_alert():
    query = '''
        import "timezone"
        option location = timezone.location(name: "Europe/Berlin")
        from(bucket:"alert")
            |> range(start:-10m) 
            |> filter(fn: (r) => r._measurement == "alerts") 
        '''
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