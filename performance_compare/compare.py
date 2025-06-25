import time
from influxdb_client import InfluxDBClient, Point, WritePrecision, QueryApi
import oracledb
import matplotlib.pyplot as plt
import numpy as np
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
        v = random.uniform(20, 30)  # random temp values between 20-30
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

def visualize_results(influx_insert_time=None, oracle_insert_time=None, influx_read_time=None, oracle_read_time=None, 
                        influx_update_time=None, oracle_update_time=None, influx_delete_time=None, oracle_delete_time=None):
    operations = ['Insert', 'Read', 'Update', 'Delete']
    if influx_insert_time is None:
        influx_times = [0.0308, 0.0305, None, 0.0866]
        oracle_times = [0.0362, 0.0032, 0.0065, 0.0105]
    else:
        influx_times = [influx_insert_time, influx_read_time, influx_update_time, influx_delete_time]
        oracle_times = [
            oracle_insert_time, oracle_read_time, oracle_update_time, oracle_delete_time
        ]

    x = np.arange(len(operations))
    width = 0.35

    fig, ax = plt.subplots()

    # For update, handle None by showing 0 or leaving blank
    influx_plot = [t if t is not None else 0 for t in influx_times]

    bars1 = ax.bar(x - width/2, influx_plot, width, label='InfluxDB')
    bars2 = ax.bar(x + width/2, oracle_times, width, label='Oracle Database 23ai')

    # Add labels and title
    ax.set_ylabel('Time (seconds)')
    ax.set_title('CRUD Performance Comparison: InfluxDB vs Oracle Database 23ai')
    ax.set_xticks(x)
    ax.set_xticklabels(operations)
    ax.legend()

    # Mark "N/A" on Update InfluxDB bar
    for i, t in enumerate(influx_times):
        if t is None:
            ax.text(x[i] - width/2, 0.001, 'N/A', ha='center', va='bottom', color='red')

    plt.show()

def main():
    n_data_points = 1000
    print(f"Starting performance comparison between InfluxDB and Oracle on {n_data_points} time series data points.")
    data = generate_data(n_data_points)
    influx_insert_time = insert_influx(data)
    oracle_insert_time = insert_oracle(data)
    print("Insert InfluxDB:", influx_insert_time)
    print("Insert Oracle:", oracle_insert_time)
    time.sleep(1)  # Ensure some time has passed for read operations
    influx_read_time = read_influx()
    oracle_read_time = read_oracle()
    print("Read InfluxDB:", influx_read_time)
    print("Read Oracle:", oracle_read_time)
    # update_influx() # skipped
    print("Influx does not support UPDATE, skipping.")
    oracle_update_time = update_oracle()
    print("Update Oracle:", oracle_update_time)
    influx_delete_time = delete_influx()
    oracle_delete_time = delete_oracle()
    print("Delete InfluxDB:", influx_delete_time)
    print("Delete Oracle:", oracle_delete_time)
    cleanup()
    print("Closed all connections.")
    visualize_results()
    # visualize_results(
    #     influx_insert_time, oracle_insert_time,
    #     influx_read_time, oracle_read_time,
    #     None,  # InfluxDB update time is not applicable
    #     oracle_update_time,
    #     influx_delete_time, oracle_delete_time
    # )

if __name__ == "__main__":
    main()