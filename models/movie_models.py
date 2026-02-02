from pydantic import BaseModel, Field
from typing import Literal, Annotated, Optional


class MovieBase(BaseModel):
    id: Optional[int] = None
    name: str
    imageUrl: Optional[str]
    price: int | float
    description: str
    location: Literal["SPB", "MSK"]
    published: bool
    genreId: Annotated[int, Field(ge=1, le=10)]
    rating: Optional[int | float] = None
    createdAt: Optional[str] = Field(
        None, pattern=r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}(\.\d+)?Z$"
    )


class MoviesPaginatedResponse(BaseModel):
    movies: list[MovieBase]
    count: int
    page: int
    pageSize: int
    pageCount: int


class MovieDeleteResponse(BaseModel):
    message: str
    error: str
    statusCode: int
