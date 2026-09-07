import numpy as np
import pandas as pd

from pathlib import Path

from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# ==============================================================================
# 1. RUTA DEL PROYECTO
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ruta_csv = BASE_DIR / "datos" / "datos.csv"


# ==============================================================================
# 2. CARGAR DATASET
# ==============================================================================

try:

    df = pd.read_csv(ruta_csv)

except FileNotFoundError:

    raise FileNotFoundError(
        f"No se encontró el archivo DATOS.csv en:\n{ruta_csv}"
    )


# ==============================================================================
# 3. CONFIGURACIÓN
# ==============================================================================

columna_target = "horas_hombre_invertidas"


# ==============================================================================
# 4. VALIDAR COLUMNAS
# ==============================================================================

columnas_requeridas = [
    "id_proyecto",
    "presupuesto_estimado",
    "deadline_dias",
    "cantidad_bugs",
    "numero_desarrolladores",
    "tipo_servicio",
    "infraestructura_nube_previa",
    "renovacion_contrato",
    "horas_hombre_invertidas",
    "fecha_entrega"
]


columnas_faltantes = [
    columna
    for columna in columnas_requeridas
    if columna not in df.columns
]


if columnas_faltantes:

    raise ValueError(
        "Faltan las siguientes columnas en DATOS.csv:\n"
        + "\n".join(columnas_faltantes)
    )


# ==============================================================================
# 5. LIMPIEZA DEL TARGET
# ==============================================================================

df = df.dropna(
    subset=[columna_target]
).copy()


# ==============================================================================
# 6. CONVERSIÓN DE VARIABLES NUMÉRICAS
# ==============================================================================

columnas_numericas = [
    "presupuesto_estimado",
    "deadline_dias",
    "cantidad_bugs",
    "numero_desarrolladores",
    "horas_hombre_invertidas"
]


for columna in columnas_numericas:

    df[columna] = pd.to_numeric(
        df[columna],
        errors="coerce"
    )


# Eliminar registros donde el target no pueda convertirse
df = df.dropna(
    subset=[columna_target]
).copy()


# ==============================================================================
# 7. INGENIERÍA DE CARACTERÍSTICAS
# ==============================================================================

# Evitar división entre cero
df["deadline_dias"] = df["deadline_dias"].replace(
    0,
    np.nan
)


# Presupuesto diario
df["presupuesto_por_dia"] = (
    df["presupuesto_estimado"]
    / df["deadline_dias"]
)


# Restaurar valores infinitos
df["presupuesto_por_dia"] = (
    df["presupuesto_por_dia"]
    .replace([np.inf, -np.inf], np.nan)
)


# ==============================================================================
# 8. VARIABLES PREDICTORAS
# ==============================================================================

# IMPORTANTE:
#
# id_proyecto NO se utiliza porque solo identifica el proyecto.
#
# fecha_entrega tampoco se utiliza porque representa información
# temporal/histórica que no debería ser necesaria para cotizar
# un proyecto nuevo.
#
# La variable objetivo tampoco entra en X.

columnas_a_excluir = [
    "id_proyecto",
    "fecha_entrega",
    columna_target
]


X = df.drop(
    columns=columnas_a_excluir
)

y = df[columna_target]


# ==============================================================================
# 9. CODIFICACIÓN DE VARIABLES CATEGÓRICAS
# ==============================================================================

X = pd.get_dummies(
    X,
    drop_first=True
)


# Guardamos los nombres de las columnas finales.
# Esto será importante para las predicciones del frontend.

columnas_modelo = X.columns.tolist()


# ==============================================================================
# 10. DIVISIÓN 80% / 20%
# ==============================================================================

X_train, X_test, y_train, y_test = train_test_split(

    X,
    y,

    test_size=0.20,

    random_state=42
)


# ==============================================================================
# 11. IMPUTACIÓN DE VALORES FALTANTES
# ==============================================================================

imputer = SimpleImputer(
    strategy="median"
)


X_train_imputed = imputer.fit_transform(
    X_train
)


X_test_imputed = imputer.transform(
    X_test
)


# ==============================================================================
# 12. ESCALADO
# ==============================================================================

scaler = StandardScaler()


X_train_scaled = scaler.fit_transform(
    X_train_imputed
)


X_test_scaled = scaler.transform(
    X_test_imputed
)


# ==============================================================================
# 13. MODELO RANDOM FOREST
# ==============================================================================

model = RandomForestRegressor(

    n_estimators=200,

    max_depth=10,

    min_samples_split=4,

    min_samples_leaf=1,

    max_features="sqrt",

    random_state=42,

    n_jobs=-1
)


# ==============================================================================
# 14. ENTRENAMIENTO
# ==============================================================================

print()
print("=" * 75)
print("   INNOVATECH SOLUTIONS S.A.C.")
print("   SISTEMA INTELIGENTE DE COTIZACIÓN AUTOMÁTICA")
print("=" * 75)

print()
print("[1] CARGA Y PREPROCESAMIENTO")
print("-" * 75)

print(f"[+] Archivo utilizado       : DATOS.csv")
print(f"[+] Registros procesados    : {len(df):,}")
print(f"[+] Variables predictoras   : {X.shape[1]}")
print(f"[+] Variable objetivo       : {columna_target}")

print()
print("[2] DIVISIÓN DE LOS DATOS")
print("-" * 75)

print(
    f"[+] Datos totales           : {len(df):,}"
)

print(
    f"[+] Entrenamiento 80%       : {len(X_train):,}"
)

print(
    f"[+] Prueba 20%              : {len(X_test):,}"
)

print()
print("[3] ENTRENAMIENTO DEL MODELO")
print("-" * 75)

print(
    "[~] Entrenando Random Forest Regressor..."
)


model.fit(
    X_train_scaled,
    y_train
)


print(
    "[✓] Modelo entrenado correctamente."
)


# ==============================================================================
# 15. PREDICCIÓN SOBRE LOS DATOS DE PRUEBA
# ==============================================================================

y_pred = model.predict(
    X_test_scaled
)


# ==============================================================================
# 16. MÉTRICAS
# ==============================================================================

mae = mean_absolute_error(
    y_test,
    y_pred
)


rmse = np.sqrt(
    mean_squared_error(
        y_test,
        y_pred
    )
)


r2 = r2_score(
    y_test,
    y_pred
)


# ==============================================================================
# 17. RESULTADOS
# ==============================================================================

print()
print("[4] EVALUACIÓN DEL MODELO")
print("-" * 75)

print(
    f"[+] MAE  : {mae:.2f} horas-hombre"
)

print(
    f"[+] RMSE : {rmse:.2f} horas-hombre"
)

print(
    f"[+] R²   : {r2:.4f}"
)

print(
    f"[+] R²   : {r2 * 100:.2f}%"
)


# ==============================================================================
# 18. INFORMACIÓN DEL DATASET
# ==============================================================================

print()
print("[5] DISTRIBUCIÓN DE LOS DATOS")
print("-" * 75)

print(
    f"[+] Mínimo de horas-hombre : "
    f"{y.min():.2f}"
)

print(
    f"[+] Máximo de horas-hombre : "
    f"{y.max():.2f}"
)

print(
    f"[+] Promedio de horas      : "
    f"{y.mean():.2f}"
)


# ==============================================================================
# 19. FUNCIÓN PARA PREDICCIÓN EN TIEMPO REAL
# ==============================================================================

def predecir_desde_diccionario(datos_diccionario):

    """
    Recibe los datos de un nuevo proyecto y devuelve
    las horas-hombre estimadas por el modelo.
    """

    # --------------------------------------------------
    # Crear DataFrame
    # --------------------------------------------------

    nuevo_df = pd.DataFrame(
        [datos_diccionario]
    )


    # --------------------------------------------------
    # Validar variables principales
    # --------------------------------------------------

    campos_requeridos = [
        "presupuesto_estimado",
        "deadline_dias",
        "cantidad_bugs",
        "numero_desarrolladores",
        "tipo_servicio",
        "infraestructura_nube_previa",
        "renovacion_contrato"
    ]


    campos_faltantes = [
        campo
        for campo in campos_requeridos
        if campo not in nuevo_df.columns
    ]


    if campos_faltantes:

        raise ValueError(
            "Faltan datos requeridos para la predicción: "
            + ", ".join(campos_faltantes)
        )


    # --------------------------------------------------
    # Conversión numérica
    # --------------------------------------------------

    nuevo_df["presupuesto_estimado"] = pd.to_numeric(
        nuevo_df["presupuesto_estimado"],
        errors="coerce"
    )


    nuevo_df["deadline_dias"] = pd.to_numeric(
        nuevo_df["deadline_dias"],
        errors="coerce"
    )


    nuevo_df["cantidad_bugs"] = pd.to_numeric(
        nuevo_df["cantidad_bugs"],
        errors="coerce"
    )


    nuevo_df["numero_desarrolladores"] = pd.to_numeric(
        nuevo_df["numero_desarrolladores"],
        errors="coerce"
    )


    # --------------------------------------------------
    # Ingeniería de características
    # --------------------------------------------------

    nuevo_df["deadline_dias"] = nuevo_df[
        "deadline_dias"
    ].replace(
        0,
        np.nan
    )


    nuevo_df["presupuesto_por_dia"] = (
        nuevo_df["presupuesto_estimado"]
        / nuevo_df["deadline_dias"]
    )


    nuevo_df["presupuesto_por_dia"] = (
        nuevo_df["presupuesto_por_dia"]
        .replace(
            [np.inf, -np.inf],
            np.nan
        )
    )


    # --------------------------------------------------
    # One-Hot Encoding
    # --------------------------------------------------

    nuevo_df = pd.get_dummies(
        nuevo_df,
        drop_first=True
    )


    # --------------------------------------------------
    # Alinear columnas
    # --------------------------------------------------

    nuevo_df = nuevo_df.reindex(
        columns=columnas_modelo,
        fill_value=0
    )


    # --------------------------------------------------
    # Imputación
    # --------------------------------------------------

    nuevo_imputado = imputer.transform(
        nuevo_df
    )


    # --------------------------------------------------
    # Escalado
    # --------------------------------------------------

    nuevo_escalado = scaler.transform(
        nuevo_imputado
    )


    # --------------------------------------------------
    # Predicción
    # --------------------------------------------------

    prediccion = model.predict(
        nuevo_escalado
    )


    # --------------------------------------------------
    # Resultado
    # --------------------------------------------------

    horas_estimadas = float(
        prediccion[0]
    )


    return horas_estimadas


# ==============================================================================
# 20. FUNCIÓN COMPLETA DE COTIZACIÓN
# ==============================================================================

def generar_cotizacion(datos_diccionario, tarifa_hora_usd=35.0):

    """
    Genera una cotización automática a partir
    de los requerimientos del proyecto.
    """

    horas_estimadas = predecir_desde_diccionario(
        datos_diccionario
    )


    costo_estimado = (
        horas_estimadas
        * tarifa_hora_usd
    )


    return {

        "horas_hombre_estimadas": round(
            horas_estimadas,
            2
        ),

        "tarifa_hora_usd": round(
            tarifa_hora_usd,
            2
        ),

        "costo_estimado_usd": round(
            costo_estimado,
            2
        ),

        "tiempo_respuesta": "< 1 segundo"

    }


# ==============================================================================
# 21. PRUEBA DE COTIZACIÓN
# ==============================================================================

if __name__ == "__main__":

    cliente_demo = {

        "presupuesto_estimado": 15000.00,

        "deadline_dias": 90,

        "cantidad_bugs": 5,

        "numero_desarrolladores": 5,

        "tipo_servicio": "Sistema SaaS",

        "infraestructura_nube_previa": "Sí",

        "renovacion_contrato": "No"

    }


    resultado = generar_cotizacion(
        cliente_demo,
        tarifa_hora_usd=35.0
    )


    print()
    print("[6] PRUEBA DE COTIZACIÓN EN TIEMPO REAL")
    print("-" * 75)

    print("[DATOS DEL PROYECTO]")

    print(
        f"Tipo de servicio          : "
        f"{cliente_demo['tipo_servicio']}"
    )

    print(
        f"Presupuesto estimado      : "
        f"${cliente_demo['presupuesto_estimado']:,.2f}"
    )

    print(
        f"Deadline                  : "
        f"{cliente_demo['deadline_dias']} días"
    )

    print(
        f"Cantidad de bugs         : "
        f"{cliente_demo['cantidad_bugs']}"
    )

    print(
        f"Número de desarrolladores: "
        f"{cliente_demo['numero_desarrolladores']}"
    )

    print(
        f"Infraestructura nube     : "
        f"{cliente_demo['infraestructura_nube_previa']}"
    )

    print(
        f"Renovación de contrato   : "
        f"{cliente_demo['renovacion_contrato']}"
    )


    print()
    print("[RESULTADO DEL MODELO]")
    print("-" * 75)

    print(
        f"Horas-hombre estimadas   : "
        f"{resultado['horas_hombre_estimadas']:.2f} horas"
    )

    print(
        f"Tarifa por hora          : "
        f"${resultado['tarifa_hora_usd']:.2f} USD"
    )

    print(
        f"Costo estimado           : "
        f"${resultado['costo_estimado_usd']:,.2f} USD"
    )

    print(
        f"Tiempo de respuesta      : "
        f"{resultado['tiempo_respuesta']}"
    )


    # ==========================================================================
    # IMPORTANCIA DE VARIABLES
    # ==========================================================================

    print()
    print("[7] IMPORTANCIA DE LAS VARIABLES")
    print("-" * 75)


    df_importancia = pd.DataFrame({

        "Variable": columnas_modelo,

        "Importancia": model.feature_importances_

    })


    df_importancia["Porcentaje"] = (
        df_importancia["Importancia"]
        * 100
    )


    df_importancia = (
        df_importancia
        .sort_values(
            by="Importancia",
            ascending=False
        )
        .reset_index(
            drop=True
        )
    )


    for _, fila in df_importancia.iterrows():

        print(
            f"{fila['Variable']:<40} "
            f"{fila['Porcentaje']:>6.2f}%"
        )


    print()
    print("=" * 75)
    print("   PROCESO FINALIZADO CORRECTAMENTE")
    print("=" * 75)
