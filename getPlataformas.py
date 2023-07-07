from fastapi import FastAPI, Header
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
    allow_methods=["GET"],
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


@app.get("/plataforma/getPlataformas/")
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

if __name__ == '__main__':
    uvicorn.run(app, port=8080, host='0.0.0.0')
