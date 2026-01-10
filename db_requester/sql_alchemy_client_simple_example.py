from sqlalchemy import create_engine, Column, String, Boolean, DateTime, text
from sqlalchemy.orm import declarative_base, sessionmaker

# Подключение к базе данных
host = "80.90.191.123"
port = 31200
database_name = "db_movies"
username = "postgres"
password = "AmwFrtnR2"

# формируем URL для подключения к базе
connection_string = (
    f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}"
)
# обьект для подключения к базе данных
engine = create_engine(connection_string)


def sql_alchemy_SQL():
    query = """
    SELECT id, email, full_name, "password", created_at, updated_at, verified, banned, roles
    FROM public.users
    WHERE id = :user_id;
    """

    # Параметры запроса для подстановки в наш SQL запрос
    user_id = "3a172562-e05d-4768-82dd-a098d8e7bbb3"

    # Выполняем запрос
    with (
        engine.connect() as connection
    ):  # Выполняем соединение с базой данных и автоматически закрываем его по завершении выполнения
        result = connection.execute(text(query), {"user_id": user_id})
        for row in result:
            print(row)


if __name__ == "__main__":
    sql_alchemy_SQL()
