import os
from dotenv import load_dotenv

load_dotenv()


class DBConnectionString:
    DB_CONNECTION_STRING: os.getenv("DB_CONNECTION_STRING")
