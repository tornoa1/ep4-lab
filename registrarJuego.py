from fastapi import FastAPI, Header
from fastapi import Response
from pydantic import BaseModel
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
import uvicorn

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["POST"],
    allow_headers=["*"],
)

def get_db_connection():
    connection = mysql.connector.connect(
        host="10.1.2.201",
        port="3306",
        user="admin",
        password="Ronald@4321",
        database="BDEP4"
    )
    return connection

class Juego(BaseModel):
    tituloJuego: str
    plataformaId: int

@app.options("/plataforma/registrarJuego")
async def options_registrar_juego():
    return {}

@app.post("/plataforma/registrarJuego")
async def registrar_juego(juego: Juego):
    connection = get_db_connection()
    cursor = connection.cursor()

    insert_query = "INSERT INTO juegos (nombre, plataforma_id) VALUES (%s, %s)"
    juego_data = (juego.tituloJuego, juego.plataformaId)
    cursor.execute(insert_query, juego_data)
    connection.commit()

    cursor.close()
    connection.close()

    return {"message": "Juego registrado correctamente"}

if __name__ == '__main__':
    uvicorn.run(app, port=8081, host='0.0.0.0')
