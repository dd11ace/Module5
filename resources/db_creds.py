import os
from dotenv import load_dotenv

load_dotenv()


# class DBConnectionString:
#     DB_CONNECTION_STRING: os.getenv("DB_CONNECTION_STRING")


class MoviesDbCreds:
    HOST = os.getenv("DB_MOVIES_HOST")
    PORT = os.getenv("DB_MOVIES_PORT")
    DATABASE_NAME = os.getenv("DB_MOVIES_NAME")
    USERNAME = os.getenv("DB_MOVIES_USERNAME")
    PASSWORD = os.getenv("DB_MOVIES_PASSWORD")
