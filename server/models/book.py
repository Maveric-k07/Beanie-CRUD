from beanie import Document
from pydantic import BaseModel
from typing import List, Optional


class Book(Document):
    title: str
    author: str
    published_year: int
    reviews: List[str] = []

    class Settings:
        name = "books"

    class Config:
        schema_extra = {
            "example": {
                "title": "The Great Gatsby",
                "author": "F. Scott Fitzgerald",
                "published_year": 1925,
                "review": "Excellent course!",
            }
        }


class UpdateBook(BaseModel):
    title: Optional[str]
    author: Optional[str]
    published_year: Optional[int]
