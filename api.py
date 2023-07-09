from fastapi import FastAPI, Header
import mysql.connector
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from fastapi import Response
from pydantic import BaseModel

app = FastAPI()

origins = [
    "*",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["GET", "POST"],
    allow_headers=["*"],
)

def get_db_connection():
    connection = mysql.connector.connect(
        host="10.1.2.32",
        port="3306",
        user="admin",
        password="Ronald@4321",
        database="BDEP4"
    )
    return connection

class Juego(BaseModel):
    tituloJuego: str
    plataformaId: int

@app.get("/plataforma/getPlataformas")
async def getPlataformas():
    connection = get_db_connection()
    cursor = connection.cursor()
    query = "SELECT id, nombre FROM plataforma"
    cursor.execute(query)
    resultados = cursor.fetchall()
    cursor.close()
    connection.close()

    plataformas = []
    for resultado in resultados:
        plataforma = {
            "id": resultado[0],
            "nombre": resultado[1]
        }
        plataformas.append(plataforma)

    return {"lista": plataformas}
	
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
	
@app.get("/plataforma/getReporteJuegos")
def get_reporte_juegos():
    try:
        db = get_db_connection()
        cursor = db.cursor()

        query = "SELECT p.id AS plataforma_id, COALESCE(COUNT(j.plataforma_id), 0) AS cantidad " \
                "FROM plataforma p " \
                "LEFT JOIN juegos j ON p.id = j.plataforma_id " \
                "GROUP BY p.id"

        cursor.execute(query)
        resultados = cursor.fetchall()

        reporte_juegos = []
        for resultado in resultados:
            plataforma_id = resultado[0]
            cantidad = resultado[1]
            reporte_juegos.append({"plataforma_id": plataforma_id, "cantidad": cantidad})

        cursor.close()
        db.close()

        return {"lista": reporte_juegos}

    except Exception as e:
        return {"error": "Error al obtener el reporte de juegos"}

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
