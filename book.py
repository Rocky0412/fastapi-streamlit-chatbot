from fastapi import FastAPI

class book:
    id:int
    title:str
    author:str
    description:str
    rating:str

    def __init__(self, id: int, title: str, author: str, description: str, rating: str):
        self.id = id
        self.title = title
        self.author = author
        self.description = description
        self.rating = rating


