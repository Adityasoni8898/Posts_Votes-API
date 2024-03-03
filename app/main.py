from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from . import models
from .database import engine
from .routers import post, user, auth

models.Base.metadata.create_all(bind=engine)

app = FastAPI()


try:
    conn = psycopg2.connect(host="localhost", database="fastapi",
                            user='postgres', password='soni8898', cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Connected to the database")
except Exception as error:
    print(f"Error connecting to the database: {str(error)}")


app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)