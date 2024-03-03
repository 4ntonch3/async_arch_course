import os


DB_HOST = os.environ["DB_HOST"]
DB_PORT = int(os.environ["DB_PORT"])
DB_USER = os.environ["DB_USER"]
DB_PASSWORD = os.environ["DB_PASSWORD"]
DB_TITLE = os.environ["DB_TITLE"]

BROKER_HOST = os.environ["BROKER_HOST"]
BROKER_PORT = int(os.environ["BROKER_PORT"])

JWT_TOKEN_LIFETIME_SECONDS = int(os.environ["JWT_TOKEN_LIFETIME_SECONDS"])
JWT_SECRET = os.environ["JWT_SECRET"]

SERVE_PORT = int(os.environ["SERVE_PORT"])
