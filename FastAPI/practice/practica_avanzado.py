from fastapi import FastAPI, Path, Query
from fastapi.responses import HTMLResponse, JSONResponse
from typing import Optional, List
from pydantic import BaseModel,Field
from jwt_manager import create_token


app = FastAPI()
app.title = "Movies.com"
app.version = "1.0"

class User(BaseModel):
    email:str
    password: str
    

class Movie(BaseModel):
    id: Optional[int] = None
    titulo : str = Field(min_length= 1, max_length=40)
    año : int = Field(le= 2024)
    categoria : str = Field(min_length= 1, max_length= 40)
    
    model_config = {
        "json_schema_extra" : {
            "example" : {
                "id" : 10,
                "titulo" : "el hombre de la mascara de hierro",
                "año" : 1993,
                "categoria" : "aventura"
            }
        }
    }

movies = [
    {
        "id": 1,
        "titulo": "bastador sin gloria",
        "año" : 2019,
        "categoria" : "accion"
    },
    {
        "id": 2,
        "titulo": "300",
        "año" : 2008,
        "categoria" : "accion"
    },
    {
        "id": 3,
        "titulo": "el señor de los anillos",
        "año" : 2005,
        "categoria" : "fantasia"
    },
    {
        "id": 4,
        "titulo": "un sueño sin fin",
        "año" : 2018,
        "categoria" : "aventura"
    },
    {
        "id": 5,
        "titulo": "get out",
        "año" : 2015,
        "categoria" : "terror"
    },
    {
        "id": 6,
        "titulo": "medias de abejita",
        "año" : 2001,
        "categoria" : "drama"
    }
]

@app.get("/")
async def home():
    return HTMLResponse("<h1>Pelis.com</h1>")

@app.post("/login", tags=["Auth"])
async def login(user:User):
    return user

@app.get("/Movies/List", response_model= List[Movie], status_code= 200) 
async def list_movie() -> List[Movie]:
    return JSONResponse(movies, status_code= 200)

@app.get("/Movie/{id}")
async def get_movie_id(id:int = Path(ge= 1, le= 200)):
    for i in movies:
        if i["id"] == id:
            return JSONResponse(i, status_code=200)

@app.get("/Movies/")
async def get_movie_category(category:str = Query(min_length=1, max_length=30)):
    for i in movies:
        if i["categoria"] == category:
            return JSONResponse(i, status_code= 200)
    
@app.post("/Movies/", response_model= dict, status_code= 201)
async def post_movie(peli: Movie):
    movies.append(peli)
    return JSONResponse("Se ha resistrado la pelicula", status_code=201)

@app.put("/Movie/{id}")
async def update_movie(id : int, peli:Movie):
    for i in movies:
        if i["id"] == id:
            i["titulo"] == peli.titulo
            i["año"] == peli.año
            i["categoria"] == peli.categoria
        return JSONResponse("se ha modificado la pelicula", status_code= 200)

@app.delete("/Movie/{id}", status_code= 200)
async def delete_movie(id:int):
    for i in movies:
        if i["id"] == id:
            movies.remove(i)
        return JSONResponse ("se ha eliminado una pelicula", status_code=200)

