from fastapi import FastAPI
from fastapi.responses import JSONResponse
from fastapi import status
from fastapi import Body , HTTPException

app = FastAPI()

BOOKS = [
    {'title': 'Title One', 'author': 'Author One', 'category': 'science'},
    {'title': 'Title Two', 'author': 'Author Two', 'category': 'science'},
    {'title': 'Title Three', 'author': 'Author Three', 'category': 'history'},
    {'title': 'Title Four', 'author': 'Author Four', 'category': 'math'},
    {'title': 'Title Five', 'author': 'Author Five', 'category': 'math'},
    {'title': 'Title Six', 'author': 'Author Two', 'category': 'math'}
]


@app.get("/books")
async def read_root():
    return BOOKS

@app.get("/books/{book_title}",status_code=200)
async def read_book(book_title: str):
    for book in BOOKS:
        if book.get('title').casefold() == book_title.casefold():
            return book

    return JSONResponse(
        content={"message":"Not found"},
        status_code=404
    )


#Example of Query Parameter

@app.get("/books/",status_code=status.HTTP_200_OK)
def getbookbyCatagory(title:str,catagory:str):
    for book in BOOKS:
        if book.get("catagory").casefold==catagory.casefold and book.get("title").casefold==title.casefold:
            return book

        return JSONResponse(content={"message":"Not found"},status_code=404)

from fastapi.responses import JSONResponse

@app.get("/book/{title}")
def getBook(title: str, category: str):
    for book in BOOKS:
        book_category = book.get("category")
        book_title = book.get("title")

        if (
            book_category 
            and book_title 
            and book_category.casefold() == category.casefold()
            and book_title.casefold() == title.casefold()
        ):
            return book

    return JSONResponse(content={"message": "Not found"}, status_code=404)


#post Method
    
@app.post("/book/create")
async def create_newbook(newBook=Body()):
    BOOKS.append(newBook)
    return JSONResponse(content={"message":"created","data":newBook},
    status_code=200)
#Put method

@app.put("/books/update_book")
def update_book(updated_book=Body()):
    for i in range(len(BOOKS)):
        if BOOKS[i]["title"].casefold() == updated_book.title.casefold():
            BOOKS[i] = updated_book.dict()
            return {"message": "Book updated", "book": BOOKS[i]}

    raise HTTPException(status_code=404, detail="Book not found")


#Delete Method

@app.delete("/books/delete_book/{book_title}")
def delete_book(book_title: str):
    for i in range(len(BOOKS)):
        title = BOOKS[i].get("title")

        if title and title.casefold() == book_title.casefold():
            deleted_book = BOOKS.pop(i)
            return {
                "message": "Book deleted",
                "book": deleted_book
            }

    raise HTTPException(status_code=404, detail="Book not found")

#Gett all the book from specific authothor
@app.get("/books/author/{author}")
async def get_all_books_by_author(author: str):
    books = []

    for book in BOOKS:
        book_author = book.get("author")

        if book_author and book_author.casefold() == author.casefold():
            books.append(book)

    return JSONResponse(content=books, status_code=200)