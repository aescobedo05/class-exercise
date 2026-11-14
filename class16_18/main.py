import logging

from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

from check_storage import BookStorage

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)-8s %(name)s — %(message)s",
    datefmt="%H:%M:%S"
)
logger = logging.getLogger(__name__)


class BookInput(BaseModel):
    title: str
    price: float = Field(ge=0)


class BookResponse(BookInput):
    id: int


app = FastAPI(title="Books Database API")
storage = BookStorage()


@app.get("/books/{book_id}", response_model=BookResponse)
def get_book(book_id: int):
    book = storage.get_book(book_id)
    if book is None:
        logger.warning(f"Book not found: {book_id}")
        raise HTTPException(status_code=404, detail="Book not found")
    logger.info(f"Retrieved book: id={book_id}")
    return book

@app.post("/books", response_model=BookResponse)
def add_book(book: BookInput):
    book_id = storage.add_book(book.title, book.price)
    logger.info(f"Added book: id={book_id}")
    stored_book = storage.get_book(book_id)
    return stored_book


@app.get("/books", response_model=list[BookResponse])
def list_books(
    min_price: float = Query(default=0, ge=0),
    limit: int = Query(default=100, ge=1)
):
    book_list = storage.list_books(min_price, limit)
    logger.info("rows=%s", len(book_list))

    return book_list

@app.get("/search/books", response_model=list[BookResponse])
def search_books(
    min_price: float = Query(ge=0),
    max_price: float = Query(ge=0)
):
    if min_price > max_price:
        logger.warning("min_price must not exceed max_price")
        raise HTTPException(status_code=400, detail="min_price must not exceed max_price")

    if min_price < 0:
        logger.warning("min_price can't be negative")
        raise HTTPException(status_code=422, detail="min_price can't be negative")

    if max_price < 0:
        logger.warning("max_price can't be negative")
        raise HTTPException(status_code=422, detail="miax_price can't be negative")

    results = storage.search_books(min_price, max_price)
    logger.info("rows=%s", len(results))

    return results