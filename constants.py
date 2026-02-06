BASE_URL = "https://api.dev-cinescope.coconutqa.ru/"

AUTH_URL = "https://auth.dev-cinescope.coconutqa.ru"

HEADERS = {"Content-Type": "application/json", "Accept": "application/json"}

# Endpoints
LOGIN_ENDPOINT = "/login"
REGISTER_ENDPOINT = "/register"

MOVIES_ENDPOINT = "/movies"

USER_ENDPOINT = "/user"

# URLS
WORLDCLOCKNOW = "http://worldclockapi.com/api/json/utc/now"

# Colors for logs
GREEN = "\033[32m"
RED = "\033[31m"
RESET = "\033[0m"

# Database
DATABASE_HOST = "80.90.191.123"
DATABASE_PORT = 31200
DATABASE_NAME = "db_movies"
DATABASE_USERNAME = "postgres"
DATABASE_PASSWORD = "AmwFrtnR2"

DATABASE_CONNECTION_STRING = f"postgresql+psycopg2://{DATABASE_USERNAME}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"
