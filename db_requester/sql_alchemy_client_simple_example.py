from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db_models.user import UserDBModel
from constants import DATABASE_CONNECTION_STRING


# формируем URL для подключения к базе
connection_string = DATABASE_CONNECTION_STRING
# обьект для подключения к базе данных
engine = create_engine(connection_string)


def sdl_alchemy_ORM():
    Session = sessionmaker(bind=engine)
    session = Session()

    user_id = "d44f2c26-0b23-451e-9843-a2bcf35216c4"

    user = session.query(UserDBModel).filter(UserDBModel.id == user_id).first()

    if user:
        print(f"ID: {user.id}")
        print(f"Email: {user.email}")
        print(f"Full Name: {user.full_name}")
        print(f"Password: {user.password}")
        print(f"Created At: {user.created_at}")
        print(f"Updated At: {user.updated_at}")
        print(f"Verified: {user.verified}")
        print(f"Banned: {user.banned}")
        print(f"Roles: {user.roles}")
    else:
        print("Пользователь не найден.")


if __name__ == "__main__":
    sdl_alchemy_ORM()
