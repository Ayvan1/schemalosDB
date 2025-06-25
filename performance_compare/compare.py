import time
from influxdb_client import InfluxDBClient, Point, WritePrecision, QueryApi
import oracledb
import configparser


config = configparser.ConfigParser()
config.read("src/connect/config.ini")

# Setup InfluxDB 
influx_url = "http://localhost:8086"
influx_token = config['influx']['token']
influx_org = config['influx']['org']
influx_bucket = "performance_test"
influx_client = InfluxDBClient(url=influx_url, token=influx_token, org=influx_org)
print("InfluxDB client initialized.")
write_api = influx_client.write_api()
query_api = influx_client.query_api()

# Setup Oracle connection
oracle_conn = oracledb.connect(
    user= config['oracle']['user'],
    password= config['oracle']['password'],
    dsn= f"{config['oracle']['url']}:{config['oracle']['port']}/{config['oracle']['service']}"
)
print("Oracle connection established.")
oracle_cursor = oracle_conn.cursor()

# Sample data generator
def generate_data(n=100):
    import datetime, random
    basetime = datetime.datetime.utcnow()
    data = []
    for i in range(n):
        t = basetime + datetime.timedelta(seconds=i)
        v = random.uniform(20, 30)  # temp values between 20-30
        data.append((t, v))
    return data

# INSERT operation
def insert_influx(data):
    points = []
    for t, v in data:
        point = Point("temperature").field("value", v).time(t, WritePrecision.NS)
        points.append(point)
    start = time.time()
    write_api.write(bucket=influx_bucket, org=influx_org, record=points)
    return time.time() - start

def insert_oracle(data):
    # Create table if it doesn't exist
    oracle_cursor.execute("""
    BEGIN
        EXECUTE IMMEDIATE '
            CREATE TABLE PERFORMANCE_TEST (
                time TIMESTAMP,
                value FLOAT
            )
        ';
    EXCEPTION
        WHEN OTHERS THEN
            IF SQLCODE != -955 THEN -- -955 = ORA-00955: name is already used by an existing object
                RAISE;
            END IF;
    END;
    """)
    start = time.time()
    sql = "INSERT INTO performance_test (time, value) VALUES (:1, :2)"
    oracle_cursor.executemany(sql, data)
    oracle_conn.commit()
    return time.time() - start

# READ operation
def read_influx():
    query = f'from(bucket:"{influx_bucket}") |> range(start: -1h)'
    start = time.time()
    result = query_api.query(org=influx_org, query=query)
    return time.time() - start

def read_oracle():
    sql = "SELECT time, value FROM performance_test WHERE time > SYSDATE - 1/24"  # last 1 hour
    start = time.time()
    oracle_cursor.execute(sql)
    rows = oracle_cursor.fetchall()
    return time.time() - start

# UPDATE operation (example: increase all values by 1)
def update_influx():
    # InfluxDB doesn't support UPDATE like SQL, so you'd have to write new points or delete & reinsert.
    # For simplicity, let's skip or simulate.
    pass

def update_oracle():
    start = time.time()
    sql = "UPDATE performance_test SET value = value + 1 WHERE time > SYSDATE - 1/24"
    oracle_cursor.execute(sql)
    oracle_conn.commit()
    return time.time() - start

# DELETE operation
def delete_influx():
    # InfluxDB deletion by predicate is possible
    start = time.time()
    influx_client.delete_api().delete(
        start="1970-01-01T00:00:00Z",
        stop="2100-01-01T00:00:00Z",
        predicate='_measurement="temperature"',
        bucket=influx_bucket,
        org=influx_org
    )
    return time.time() - start

def delete_oracle():
    start = time.time()
    sql = "DELETE FROM performance_test WHERE time > SYSDATE - 1"
    oracle_cursor.execute(sql)
    oracle_conn.commit()
    return time.time() - start

def cleanup():
    try:
        oracle_cursor.close()
        oracle_conn.close()
    except Exception as e:
        print("Error closing Oracle connection:", e)
    
    try:
        influx_client.close()
    except Exception as e:
        print("Error closing InfluxDB client:", e)

def main():
    n_data_points = 1000
    print(f"Starting performance comparison between InfluxDB and Oracle on {n_data_points} time series data points.")
    data = generate_data(n_data_points)
    print("Insert InfluxDB:", insert_influx(data))
    print("Insert Oracle:", insert_oracle(data))
    print("Read InfluxDB:", read_influx())
    print("Read Oracle:", read_oracle())
    # update_influx() # skipped
    print("Influx does not support UPDATE, skipping.")
    print("Update Oracle:", update_oracle())
    print("Delete InfluxDB:", delete_influx())
    print("Delete Oracle:", delete_oracle())
    cleanup()
    print("Closed all connections.")

if __name__ == "__main__":
    main()