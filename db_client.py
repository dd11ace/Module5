import psycopg2
from resources.db_creds import DBConnectionString


def connect_to_postgres():
    connection = None
    cursor = None

    try:
        connection = psycopg2.connect(DBConnectionString.DB_CONNECTION_STRING)

        cursor = connection.cursor()

        # Вывод информации о PostgreSQL сервере
        print("Информация о сервере PostgreSQL:")
        print(connection.get_dsn_parameters(), "\n")

        # Выполнение SQL-запроса
        cursor.execute("SELECT version();")

        # Получение результата
        record = cursor.fetchone()
        print("Вы подключены к - ", record, "\n")
    except psycopg2.Error as error:
        print("Ошибка при работе с PostgreSQL: ", error)

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
            print("Соединение с PostgreSQL закрыто")
