from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import os
import math
import pandas as pd

# ============================================================
# IMPORTAR LOS MODELOS
# ============================================================

from procesos.prediccion import predecir_desde_diccionario
from procesos.prediccionNN import predecir_nn_desde_diccionario


# ============================================================
# CONFIGURACIÓN DE FASTAPI
# ============================================================

app = FastAPI(
    title="Innovatech Solutions API",
    description="Sistema inteligente de cotización automática",
    version="4.1"
)


# ============================================================
# RUTAS DEL PROYECTO
# ============================================================

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

STYLE_DIR = os.path.join(
    BASE_DIR,
    "style"
)

DATOS_DIR = os.path.join(
    BASE_DIR,
    "datos"
)


# ============================================================
# ARCHIVOS DE DATOS PERMITIDOS
# IMPORTANTE:
# El archivo correcto es datos.csv
# ============================================================

ARCHIVOS_DATOS = {
    "datos.csv": os.path.join(DATOS_DIR, "datos.csv"),
    "20k.csv": os.path.join(DATOS_DIR, "20k.csv")
}


# ============================================================
# CARPETA ESTÁTICA
# ============================================================

if os.path.exists(STYLE_DIR):
    app.mount(
        "/style",
        StaticFiles(directory=STYLE_DIR),
        name="style"
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
# MODELO DE DATOS - RANDOM FOREST
# ============================================================

class DatosML(BaseModel):

    presupuesto_estimado: float

    deadline_dias: int

    cantidad_bugs: int

    numero_desarrolladores: int

    tipo_servicio: str

    infraestructura_nube_previa: str

    renovacion_contrato: str


# ============================================================
# ENDPOINT - RANDOM FOREST
# ============================================================

@app.post("/api/predecir-ml")
def predecir_ml(datos: DatosML):

    try:

        datos_diccionario = datos.model_dump()

        print()
        print("=" * 70)
        print("DATOS RECIBIDOS - RANDOM FOREST")
        print("=" * 70)
        print(datos_diccionario)

        # ----------------------------------------------------
        # VALIDACIONES
        # ----------------------------------------------------

        if datos.presupuesto_estimado <= 0:
            raise ValueError(
                "El presupuesto debe ser mayor que 0."
            )

        if datos.deadline_dias <= 0:
            raise ValueError(
                "El deadline debe ser mayor que 0."
            )

        if datos.cantidad_bugs < 0:
            raise ValueError(
                "La cantidad de bugs no puede ser negativa."
            )

        if datos.numero_desarrolladores <= 0:
            raise ValueError(
                "Debe existir al menos un desarrollador."
            )

        # ----------------------------------------------------
        # EJECUTAR MODELO
        # ----------------------------------------------------

        prediccion = predecir_desde_diccionario(
            datos_diccionario
        )

        prediccion = float(prediccion)

        if not math.isfinite(prediccion):
            raise ValueError(
                "El modelo devolvió una predicción inválida."
            )

        # ----------------------------------------------------
        # COTIZACIÓN EN SOLES
        # ----------------------------------------------------

        tarifa_hora = 35.0

        costo_pen = prediccion * tarifa_hora

        costo_pen = float(costo_pen)

        # ----------------------------------------------------
        # RESPUESTA
        # ----------------------------------------------------

        respuesta = {

            "success": True,

            "modelo":
                "Random Forest Regressor",

            "horas_hombre":
                round(prediccion, 2),

            "tarifa_hora":
                tarifa_hora,

            "moneda":
                "PEN",

            "costo_pen":
                round(costo_pen, 2),

            "mensaje":
                "Predicción realizada correctamente"
        }

        print()
        print("RESULTADO RANDOM FOREST")
        print("=" * 70)
        print(respuesta)

        return respuesta

    except Exception as e:

        print()
        print("ERROR RANDOM FOREST")
        print("=" * 70)
        print(str(e))

        return {

            "success": False,

            "modelo":
                "Random Forest Regressor",

            "error":
                str(e)
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
# ENDPOINT - RED NEURONAL
# ============================================================

@app.post("/api/predecir-nn")
def predecir_nn(datos: DatosNN):

    try:

        datos_diccionario = datos.model_dump()

        print()
        print("=" * 70)
        print("DATOS RECIBIDOS - RED NEURONAL")
        print("=" * 70)
        print(datos_diccionario)

        # ----------------------------------------------------
        # VALIDACIONES
        # ----------------------------------------------------

        if datos.presupuesto_estimado <= 0:
            raise ValueError(
                "El presupuesto debe ser mayor que 0."
            )

        if datos.deadline_dias <= 0:
            raise ValueError(
                "El deadline debe ser mayor que 0."
            )

        if datos.cantidad_bugs < 0:
            raise ValueError(
                "La cantidad de bugs no puede ser negativa."
            )

        if datos.numero_desarrolladores <= 0:
            raise ValueError(
                "Debe existir al menos un desarrollador."
            )

        # ----------------------------------------------------
        # EJECUTAR MODELO
        # ----------------------------------------------------

        prediccion = predecir_nn_desde_diccionario(
            datos_diccionario
        )

        prediccion = float(prediccion)

        if not math.isfinite(prediccion):
            raise ValueError(
                "La red neuronal devolvió una predicción inválida."
            )

        # ----------------------------------------------------
        # COTIZACIÓN EN SOLES
        # ----------------------------------------------------

        tarifa_hora = 35.0

        costo_pen = prediccion * tarifa_hora

        costo_pen = float(costo_pen)

        # ----------------------------------------------------
        # RESPUESTA
        # ----------------------------------------------------

        respuesta = {

            "success": True,

            "modelo":
                "MLP Regressor - Red Neuronal",

            "horas_hombre":
                round(prediccion, 2),

            "tarifa_hora":
                tarifa_hora,

            "moneda":
                "PEN",

            "costo_pen":
                round(costo_pen, 2),

            "mensaje":
                "Predicción realizada correctamente"
        }

        print()
        print("RESULTADO RED NEURONAL")
        print("=" * 70)
        print(respuesta)

        return respuesta

    except Exception as e:

        print()
        print("ERROR RED NEURONAL")
        print("=" * 70)
        print(str(e))

        return {

            "success": False,

            "modelo":
                "MLP Regressor - Red Neuronal",

            "error":
                str(e)
        }


# ============================================================
# ENDPOINT - VISUALIZAR DATASETS
# ============================================================

@app.get("/api/datos")
def obtener_datos(
    archivo: str = "datos.csv",
    page: int = 1,
    limit: int = 10,
    search: str = ""
):

    try:

        # ----------------------------------------------------
        # VALIDAR ARCHIVO
        # ----------------------------------------------------

        if archivo not in ARCHIVOS_DATOS:

            return {
                "success": False,
                "error": "Dataset no permitido."
            }

        ruta_csv = ARCHIVOS_DATOS[archivo]

        # ----------------------------------------------------
        # VERIFICAR EXISTENCIA
        # ----------------------------------------------------

        if not os.path.exists(ruta_csv):

            return {
                "success": False,
                "error":
                    f"No se encontró el archivo: {ruta_csv}"
            }

        # ----------------------------------------------------
        # LEER CSV
        # ----------------------------------------------------

        df = pd.read_csv(ruta_csv)

        # ----------------------------------------------------
        # BÚSQUEDA
        # ----------------------------------------------------

        search = search.strip()

        if search:

            search_lower = search.lower()

            mask = df.astype(str).apply(
                lambda columna:
                    columna.str.lower().str.contains(
                        search_lower,
                        na=False,
                        regex=False
                    )
            ).any(axis=1)

            df = df[mask]

        # ----------------------------------------------------
        # INFORMACIÓN
        # ----------------------------------------------------

        total = len(df)

        columnas = df.columns.tolist()

        # ----------------------------------------------------
        # PAGINACIÓN
        # ----------------------------------------------------

        try:
            page = int(page)
        except:
            page = 1

        try:
            limit = int(limit)
        except:
            limit = 10

        page = max(1, page)

        limit = max(
            1,
            min(limit, 100)
        )

        total_paginas = (
            math.ceil(total / limit)
            if total > 0
            else 1
        )

        if page > total_paginas:
            page = total_paginas

        # ----------------------------------------------------
        # ÍNDICES
        # ----------------------------------------------------

        start = (page - 1) * limit

        end = start + limit

        df_page = df.iloc[
            start:end
        ].copy()

        # ----------------------------------------------------
        # NaN -> None
        # ----------------------------------------------------

        registros = []

        for registro in df_page.to_dict(
            orient="records"
        ):

            nuevo_registro = {}

            for clave, valor in registro.items():

                if pd.isna(valor):

                    nuevo_registro[clave] = None

                else:

                    nuevo_registro[clave] = valor

            registros.append(
                nuevo_registro
            )

        # ----------------------------------------------------
        # RESPUESTA
        # ----------------------------------------------------

        return {

            "success": True,

            "archivo":
                archivo,

            "total":
                total,

            "page":
                page,

            "limit":
                limit,

            "total_paginas":
                total_paginas,

            "columnas":
                columnas,

            "datos":
                registros
        }

    except Exception as e:

        print("ERROR DATASET:")
        print(str(e))

        return {

            "success": False,

            "error":
                str(e)
        }


# ============================================================
# ENDPOINT - INFORMACIÓN DE DATASETS
# ============================================================

@app.get("/api/datasets")
def informacion_datasets():

    try:

        resultado = []

        for archivo, ruta in ARCHIVOS_DATOS.items():

            existe = os.path.exists(ruta)

            cantidad = 0

            columnas = []

            if existe:

                df = pd.read_csv(ruta)

                cantidad = len(df)

                columnas = df.columns.tolist()

            resultado.append({

                "archivo":
                    archivo,

                "existe":
                    existe,

                "registros":
                    cantidad,

                "columnas":
                    columnas
            })

        return {

            "success": True,

            "datasets":
                resultado
        }

    except Exception as e:

        return {

            "success": False,

            "error":
                str(e)
        }


# ============================================================
# ENDPOINT - ESTADO DEL SISTEMA
# ============================================================

@app.get("/api/estado")
def estado():

    return {

        "success": True,

        "mensaje":
            "API de Innovatech Solutions funcionando correctamente",

        "version":
            "4.1",

        "moneda":
            "PEN",

        "tarifa_hora":
            35.0,

        "modelos": [

            "Random Forest Regressor",

            "MLP Regressor - Red Neuronal"
        ],

        "datasets": {

            "datos.csv":
                os.path.exists(
                    ARCHIVOS_DATOS["datos.csv"]
                ),

            "20k.csv":
                os.path.exists(
                    ARCHIVOS_DATOS["20k.csv"]
                )
        }
    }


# ============================================================
# RUTA PRINCIPAL
# ============================================================

@app.get(
    "/",
    response_class=HTMLResponse
)
def inicio():

    index_path = os.path.join(
        BASE_DIR,
        "index.html"
    )

    if os.path.exists(index_path):

        with open(
            index_path,
            "r",
            encoding="utf-8"
        ) as f:

            return f.read()

    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Innovatech Solutions</title>
    </head>

    <body>

        <h1>
            Innovatech Solutions API
        </h1>

        <p>
            API funcionando correctamente.
        </p>

        <p>
            index.html no encontrado.
        </p>

    </body>
    </html>
    """