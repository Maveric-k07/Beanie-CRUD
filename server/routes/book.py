from beanie import PydanticObjectId
from fastapi import APIRouter, HTTPException, status
from typing import List
from beanie import PydanticObjectId
from server.utils import pydantic_encoder
from server.models.book import Book, UpdateBook

router = APIRouter()


@router.get("/", response_model=List[Book])
async def get_books():
    books = await Book.find_all().to_list()
    return books


@router.get("/{id}", response_model=Book)
async def get_book(id: PydanticObjectId):
    book = await Book.get(id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found"
        )

    return book


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=Book)
async def create_book(book: Book):
    await book.insert()
    return book


@router.put("/{id}", response_model=Book)
async def update_book(id: PydanticObjectId, book_data: UpdateBook):
    book = await Book.get(id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found"
        )
    book_data = pydantic_encoder.encode_input(book_data)
    _ = await book.update({"$set": book_data})
    updated_book = await Book.get(id)
    return updated_book


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_book(id: PydanticObjectId):
    book = await Book.get(id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found"
        )
    await book.delete()
    return {"message": "Book deleted successfully"}


@router.post("/{id}/reviews", response_model=Book)
async def add_review(id: PydanticObjectId, review: str):
    book = await Book.get(id)
    if not book:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail=f"Book with id {id} not found"
        )
    _ = await book.update({"$push": {"reviews": review}})
    updated_book = await book.get(id)
    return updated_book
