import os


AUTH_SERVICE_HOST = os.environ["AUTH_SERVICE_HOST"]
AUTH_SERVICE_PORT = int(os.environ["AUTH_SERVICE_PORT"])

DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ["DB_PORT"])
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_TITLE = os.environ["DB_TITLE"]

BROKER_HOST = os.environ["BROKER_HOST"]
BROKER_PORT = int(os.environ["BROKER_PORT"])

SERVE_PORT = int(os.environ["SERVE_PORT"])
