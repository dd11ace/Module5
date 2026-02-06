from pydantic import BaseModel, Field, field_validator, field_serializer, ConfigDict
from typing import Optional
import datetime
import re
from typing import List
from enums.roles import Roles


class UserData(BaseModel):
    email: str
    fullName: str
    password: str
    passwordRepeat: str = Field(
        ...,
        min_length=1,
        max_length=20,
        description="passwordRepeat должен вполностью совпадать с полем password",
    )
    roles: list[Roles] = [Roles.USER]
    verified: Optional[bool] = None
    banned: Optional[bool] = None

    @field_validator("passwordRepeat")
    def check_password_repeat(cls, value: str, info) -> str:
        # Проверяем, совпадение паролей
        if "password" in info.data and value != info.data["password"]:
            raise ValueError("Пароли не совпадают")
        return value

    # Добавляем кастомный JSON-сериализатор для Enum

    @field_serializer("roles")
    def serialize_roles(self, roles: list[Roles | str]) -> list[str]:
        """Сериализует роли в строки, принимает как Enum, так и строки."""
        if not roles:
            return []

        result = []
        for role in roles:
            if isinstance(role, Roles):
                result.append(role.value)
            elif isinstance(role, str):
                result.append(role)
            else:
                result.append(str(role))
        return result

    # Метод для удобного получения ролей как строк
    def get_roles_as_strings(self) -> list[str]:
        """Возвращает роли в виде списка строк."""
        return self.serialize_roles(self.roles)

    @property
    def roles_strings(self) -> list[str]:
        """Property для получения ролей в виде строк."""
        return self.get_roles_as_strings()


class RegisterUserResponse(BaseModel):
    id: str
    email: str = Field(
        pattern=r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$",
        description="Email пользователя",
    )
    fullName: str = Field(
        min_length=1, max_length=100, description="Полное имя пользователя"
    )
    verified: bool
    banned: bool = False
    roles: List[Roles]
    createdAt: str = Field(
        description="Дата и время создания пользователя в формате ISO 8601"
    )

    @field_validator("createdAt")
    def validate_created_at(cls, value: str) -> str:
        # Валидатор для проверки формата даты и времени (ISO 8601).
        try:
            datetime.datetime.fromisoformat(value)
        except ValueError:
            raise ValueError(
                "Некорректный формат даты и времени. Ожидается формат ISO 8601."
            )
        return value

    @field_serializer("roles")
    def serialize_roles(self, roles: List[Roles | str]) -> List[str]:
        """Сериализует роли в строки."""
        if not roles:
            return []
        return [role.value if isinstance(role, Roles) else str(role) for role in roles]

    def get_roles_as_strings(self) -> list[str]:
        """Возвращает роли в виде списка строк."""
        return self.serialize_roles(self.roles)

    @property
    def roles_strings(self) -> list[str]:
        """Property для получения ролей в виде строк."""
        return self.get_roles_as_strings()

    model_config = ConfigDict()
