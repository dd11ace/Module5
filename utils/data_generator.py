import random
import string
import datetime
from faker import Faker

faker = Faker()


class DataGenerator:
    @staticmethod
    def generate_random_email() -> str:
        random_string = "".join(
            random.choices(string.ascii_letters + string.digits, k=8)
        )

        return f"kek{random_string}@gmail.com"

    @staticmethod
    def generate_random_name() -> str:
        return f"{faker.first_name()} {faker.last_name()}"

    @staticmethod
    def generate_random_password() -> str:
        """
        Генерация пароля, соответствующего требованиям:
        - Минимум 1 буква.
        - Минимум 1 цифра.
        - Допустимые символы.
        - Длина от 8 до 20 символов
        """
        # Гарантия хотя бы одной буквы и цифры
        letters = random.choice(string.ascii_letters)
        digits = random.choice(string.digits)

        # Дополнение пароля случайными символами из допустимых
        special_chars = "?@#$%^&*|:"

        all_chars = string.ascii_letters + string.digits + special_chars

        remaining_length = random.randint(6, 18)
        remaining_chars = "".join(random.choices(all_chars, k=remaining_length))

        # Перемешиваем пароль для рандомизации
        password = list(letters + digits + remaining_chars)
        random.shuffle(password)

        return "".join(password)

    @staticmethod
    def generate_random_movie_data() -> dict:
        """
        Генерация данных для создания фильма

        returns:
            dict: Данные фильма
        """

        movie_data = {
            "name": faker.sentence(nb_words=3),
            "imageUrl": faker.image_url(),
            "price": random.randint(100, 1000),
            "description": faker.text(max_nb_chars=200),
            "location": random.choice(["SPB", "MSK"]),
            "published": random.choice([True, False]),
            "genreId": random.randint(1, 10),
        }

        return movie_data

    @staticmethod
    def generate_user_data() -> dict:
        """Генерирует данные для тестового пользователя"""
        from uuid import uuid4

        return {
            "id": f"{uuid4()}",  # генерируем UUID как строку
            "email": DataGenerator.generate_random_email(),
            "full_name": DataGenerator.generate_random_name(),
            "password": DataGenerator.generate_random_password(),
            "created_at": datetime.datetime.now(),
            "updated_at": datetime.datetime.now(),
            "verified": False,
            "banned": False,
            "roles": "{USER}",
        }
