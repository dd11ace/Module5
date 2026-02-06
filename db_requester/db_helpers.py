from sqlalchemy.orm import Session
from db_models.user import UserDBModel
from db_models.movie import MovieDBSchema


class DBHelper:
    """Класс с методами для работы с БД в тестах"""

    def __init__(self, db_session: Session):
        self.db_session = db_session

    def create_test_user(self, user_data: dict) -> UserDBModel:
        """Создает тестового пользователя"""
        user = UserDBModel(**user_data)
        self.db_session.add(user)
        self.db_session.commit()
        self.db_session.refresh(user)
        return user

    def get_user_by_id(self, user_id: str):
        """Получет пользователя по ID"""
        return (
            self.db_session.query(UserDBModel).filter(UserDBModel.id == user_id).first()
        )

    def get_user_by_email(self, email: str):
        """Получет пользователя по email"""
        return (
            self.db_session.query(UserDBModel)
            .filter(UserDBModel.email == email)
            .first()
        )

    def get_user_by_name(self, name: str):
        """Получет пользователя по названию"""
        return (
            self.db_session.query(UserDBModel).filter(UserDBModel.name == name).first()
        )

    def user_exists_by_email(self, email: str) -> bool:
        """Проверяет существование пользователя по email"""
        return (
            self.db_session.query(UserDBModel)
            .filter(UserDBModel.email == email)
            .count()
            > 0
        )

    def delete_user(self, user: UserDBModel):
        """Удаляет пользователя"""
        self.db_session.delete(user)
        self.db_session.commit()

    def create_test_movie(self, movie_data: dict) -> MovieDBSchema:
        """Создает тестовый фильм"""
        movie = MovieDBSchema(**movie_data)
        self.db_session.add(movie)
        self.db_session.commit()
        self.db_session.refresh(movie)
        return movie

    def get_movie_by_id(self, movie_id: str):
        """Получает фильм по ID"""
        return (
            self.db_session.query(MovieDBSchema)
            .filter(MovieDBSchema.id == movie_id)
            .first()
        )

    def delete_movie(self, movie: MovieDBSchema):
        """Удаление фильма"""
        self.db_session.delete(movie)
        self.db_session.commit()

    def cleanup_test_data(self, objects_to_delete: list):
        """Очищает тестовые данные"""
        for obj in objects_to_delete:
            if obj:
                self.db_session.delete(obj)
        self.db_session.commit()
