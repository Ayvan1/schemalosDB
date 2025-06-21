from src.connect.connectOracle import connect
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

def read_all_temperature():
    temp = []
    try:
        with connect.cursor() as cursor:
            query = "select captured_time ,temperature,host_name,sensor_name from cpu_temperature"
            cursor.execute(query)
            for row in cursor.fetchall():
                temp.append(Record(
                        host=row[2],
                        sensor_name=row[3],
                        time= row[0],
                        temperature=row[1]
                    )
                )
        return temp
    except Exception as  e:
        print(e)
        return temp
    

def read_all_temperature_by_time(time:str):
    temp = []
    try:
        with connect.cursor() as cursor:
            query = """select captured_time ,temperature,host_name,sensor_name 
                            from cpu_temperature
                            where captured_time >= TO_TIMESTAMP(':ts', 'YYYY-MM-DD HH24:MI:SS')
                    """
            cursor.execute(query,{'ts': time})
            for row in cursor.fetchall():
               temp.append(Record(
                        host=row[2],
                        sensor_name=row[3],
                        time= row[0],
                        temperature=row[1]
                    )
                )
        return temp
    except Exception as e:
        print(e)
        return temp
    

def  read_temperature_from_a_sensor(sensor_index:int):
    temp = []
    try:
        with  connect.cursor() as cursor:
            query = """ select captured_time ,temperature,host_name,sensor_name 
                        from cpu_temperature
                        where sensor_name = ':name'
                    
                    """
            cursor.execute(query,{'name':_get_sensor_name(sensor_index)})
            for row in cursor.fetchall():
               temp.append(Record(
                        host=row[2],
                        sensor_name=row[3],
                        time= row[0],
                        temperature=row[1]
                    )
                )
        return temp
    except Exception as e:
        print(e)
        return temp
    

def read_temperature_from_a_sensor_by_time(sensor_index:int, time:str):
    
    temp = []
    try:
        with connect.cursor() as cursor:
            query = """ select captured_time ,temperature,host_name,sensor_name 
                        from cpu_temperature
                        where sensor_name = ':name' and captured_time >= TO_TIMESTAMP(':ts', 'YYYY-MM-DD HH24:MI:SS')
            """
            cursor.execute(query,{'name':_get_sensor_name(sensor_index),'ts':time})
            for row in cursor.fetchall():
                temp.append(Record(
                        host=row[2],
                        sensor_name=row[3],
                        time= row[0],
                        temperature=row[1]
                    )
                )
        return temp
    except Exception as e:
        print(e)
        return temp