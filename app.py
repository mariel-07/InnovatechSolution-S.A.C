from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

# ============================================================
# IMPORTAR LOS MODELOS DESDE LA CARPETA procesos
# ============================================================

from procesos.prediccion import predecir_desde_diccionario
from procesos.prediccionNN import predecir_nn_desde_diccionario


# ============================================================
# CONFIGURACIÓN DE FASTAPI
# ============================================================

app = FastAPI(
    title="Innovatech Solutions API",
    version="2.5"
)


# ============================================================
# CORS
# ============================================================

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================
# MODELO DE DATOS - MACHINE LEARNING
# ============================================================

class DatosML(BaseModel):

    presupuesto_usd: float

    deadline_dias: int

    tipo_servicio: str

    infraestructura_cloud: int


# ============================================================
# ENDPOINT MACHINE LEARNING
# ============================================================

@app.post("/api/predecir-ml")
def predecir_ml(datos: DatosML):

    try:

        datos_diccionario = datos.model_dump()

        prediccion = predecir_desde_diccionario(
            datos_diccionario
        )

        costo = prediccion * 35.0


        return {
            "success": True,

            "modelo": "Random Forest Regressor",

            "horas_hombre": round(
                float(prediccion),
                1
            ),

            "costo_usd": round(
                float(costo),
                2
            )
        }


    except Exception as e:

        return {
            "success": False,

            "error": str(e)
        }


# ============================================================
# MODELO DE DATOS - RED NEURONAL
# ============================================================

class DatosNN(BaseModel):

    presupuesto_estimado: float

    deadline_dias: int

    cantidad_bugs: int

    numero_desarrolladores: int

    infraestructura_nube_previa: str

    renovacion_contrato: str

    tipo_servicio: str


# ============================================================
# ENDPOINT RED NEURONAL
# ============================================================

@app.post("/api/predecir-nn")
def predecir_nn(datos: DatosNN):

    try:

        datos_diccionario = datos.model_dump()

        prediccion = predecir_nn_desde_diccionario(
            datos_diccionario
        )

        costo = prediccion * 120.0


        return {
            "success": True,

            "modelo": "MLP Regressor - Red Neuronal",

            "horas_hombre": round(
                float(prediccion),
                1
            ),

            "costo_pen": round(
                float(costo),
                2
            )
        }


    except Exception as e:

        return {
            "success": False,

            "error": str(e)
        }


# ============================================================
# RUTA PRINCIPAL DE PRUEBA
# ============================================================

@app.get("/")
def inicio():

    return {
        "mensaje": "Innovatech Solutions API funcionando correctamente",

        "version": "2.5",

        "endpoints": {
            "machine_learning": "/api/predecir-ml",
            "red_neuronal": "/api/predecir-nn"
        }
    }