from fastapi import FastAPI
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
    return mysql.connector.connect(
        host="10.1.2.201",
        port="3306",
        user="admin",
        password="Ronald@4321",
        database="BDEP4"
    )

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

if __name__ == "__main__":
    uvicorn.run(app, port=8082, host="0.0.0.0")
