from src.connect.connectOracle import connect
from src.model.record import Record
from src.model.alertData  import AlertData
from datetime import datetime

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
            query = """SELECT captured_time, temperature, host_name, sensor_name
                        FROM cpu_temperature
                        WHERE  captured_time >= SYSTIMESTAMP - INTERVAL '20' MINUTE"""
            cursor.execute(query)
            for row in cursor.fetchall():
                temp.append(Record(
                        host=row[2],
                        sensor_name=row[3],
                        time= row[0],
                        temperature=row[1]
                    )
                )
        print(temp)
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
    

def set_alert(alert_info):

    create_proc_sql = """

        create or replace  procedure  add_data is v_start_date TIMESTAMP;
        begin
            select start_date into v_start_date
            from job_params
            where job_name  = 'job_oracle';

            insert into alert_temperature (id,captured_time, temperature,sensor_name)
            select id,captured_time, temperature, sensor_name 
            from cpu_temperature
            where temperature >= {alert_info} and captured_time >= v_start_date and not exists (
                select 1 from alert_temperature where alert_temperature.id  =  cpu_temperature.id
            );

            commit;
        end;
    """
    
    create_job_sql = """
    Begin
         DBMS_SCHEDULER.CREATE_JOB (
        job_name        => 'job_oracle',
        job_type        => 'PLSQL_BLOCK',
        job_action      => 'BEGIN inserer_donnees; END;',
        start_date      => TO_TIMESTAMP('{start_date}', 'YYYY-MM-DD HH24:MI:SS'),
        repeat_interval => 'FREQ=SECONDLY; INTERVAL=40',
        enabled         => TRUE
            );
        EXCEPTION
            WHEN OTHERS THEN
                IF SQLCODE = -27477 THEN NULL; -- job existe déjà
                ELSE RAISE;
                END IF;
        END;
    """

    update_time = """ MERGE INTO job_params jp
                    USING (SELECT 'job_oracle' AS job_name, TO_TIMESTAMP(:start_date, 'YYYY-MM-DD HH24:MI:SS') AS start_date FROM dual) src
                    ON (jp.job_name = src.job_name)
                    WHEN MATCHED THEN UPDATE SET jp.start_date = src.start_date
                    WHEN NOT MATCHED THEN INSERT (job_name, start_date) VALUES (src.job_name, src.start_date)
                """,

    current_time = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")[:-3]

    with connect.cursor() as cursor:
        cursor.execute(create_proc_sql,alert_info=alert_info)
        cursor.execute(update_time,start_date=current_time)
        create_job_sql_ = create_job_sql.format(start_date=current_time)
        cursor.execute(create_job_sql_)

    connect.commit()
    return {"status": "Job saved"}


    # try:
    #     with connect.cursor() as cursor:
    #         query = """
    #             insert into alert_temperature(captured_time,temperature,sensor) values(:time,:temp,:name)
    #         """
    #         cursor.execute(
    #             query,{
    #                 "time":alert_info.time,
    #                 "temp":alert_info.temp,
    #                 "name":alert_info.name
    #             })
    #         connect.commit()
    # except  Exception as  e:
    #     return {"error":e}
    

def get_alert():
    temp = []
    try:
        with connect.cursor() as  cursor:
            query = """
                    select  captured_time,temperature,sensor from alert_temperature
            """
            cursor.execute(query)
            for row  in cursor.fetchall():
                temp.append (AlertData(
                    time= row[0],
                    temperature= row[1],
                    sensor_name= row[2],
                ))
        return temp
    except Exception as  e:
        print(e)
        return  temp

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