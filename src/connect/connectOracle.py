import oracledb as odb
from src.connect.read_config import  config

dsn = odb.makedsn(config["oracle"]["url"],config["oracle"]["port"],service_name=config["oracle"]["service"])

connect = odb.connect(user=config["oracle"]["user"],password=config["oracle"]["password"],dsn=dsn)