from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from resources.db_creds import MoviesDbCreds

# Движок для подключения к базе данных
engine = create_engine(
    f"postgresql+psycopg2://{MoviesDbCreds.USERNAME}:{MoviesDbCreds.PASSWORD}@{MoviesDbCreds.HOST}:{MoviesDbCreds.PORT}/{MoviesDbCreds.DATABASE_NAME}",
    echo=False,  # True для отладки SQL запросов
)

# Создаем фабрику сессий
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


def get_db_session():
    """Создает новую сессию БД"""
    return SessionLocal()
