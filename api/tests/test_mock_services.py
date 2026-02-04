import requests
from custom_requester.custom_requester 
from constants import WORLDCLOCKNOW

from pydantic import BaseModel, Field, ConfigDict


class WorldClockResponse(BaseModel):
    id: str = Field(alias="$id")
    currentDateTime: str
    utcOffset: str
    isDayLightSavingTime: bool
    dayOfTheWeek: str
    timeZoneName: str
    currentFileTime: int
    ordinalDate: str
    serviceRespones: None

    model_config = ConfigDict(validate_by_name=True)


class DateTimeRequest(BaseModel):
    currentDateTime: str


class WhatIsTodayResponse(BaseModel):
    message: str


def get_worldclockapi_time() -> WorldClockResponse:
    response = requests.get(WORLDCLOCKNOW)
    assert response.status_code == 200, "Удаленный сервис недоступен"
    return WorldClockResponse(**response.json())
