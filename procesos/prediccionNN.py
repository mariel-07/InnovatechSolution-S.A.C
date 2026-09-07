import numpy as np
import pandas as pd

from pathlib import Path

from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler

from sklearn.metrics import (
    mean_absolute_error,
    mean_squared_error,
    r2_score
)


# ==============================================================================
# 1. RUTA DEL PROYECTO
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ruta_csv = BASE_DIR / "datos" / "20k.csv"


# ==============================================================================
# 2. CARGAR DATASET
# ==============================================================================

try:

    df = pd.read_csv(ruta_csv)

except FileNotFoundError:

    raise FileNotFoundError(
        f"No se encontró el archivo 20k.csv en:\n{ruta_csv}"
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

        "Faltan las siguientes columnas en 20k.csv:\n"

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


df = df.dropna(
    subset=[columna_target]
).copy()


# ==============================================================================
# 7. INGENIERÍA DE CARACTERÍSTICAS
# ==============================================================================

# Evitar división entre cero

df["deadline_dias"] = df[
    "deadline_dias"
].replace(
    0,
    np.nan
)


# Crear presupuesto por día

df["presupuesto_por_dia"] = (

    df["presupuesto_estimado"]

    / df["deadline_dias"]

)


# Eliminar valores infinitos

df["presupuesto_por_dia"] = (

    df["presupuesto_por_dia"]

    .replace(
        [np.inf, -np.inf],
        np.nan
    )

)


# ==============================================================================
# 8. VARIABLES PREDICTORAS
# ==============================================================================

columnas_a_excluir = [

    "id_proyecto",

    "fecha_entrega",

    columna_target

]


X_temp = df.drop(
    columns=columnas_a_excluir
)


y = df[columna_target]


# ==============================================================================
# 9. CODIFICACIÓN DE VARIABLES CATEGÓRICAS
# ==============================================================================

X = pd.get_dummies(

    X_temp,

    drop_first=True

)


# Guardar columnas utilizadas por el modelo

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
# 11. IMPUTACIÓN
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
# 12. ESCALAMIENTO DE LAS VARIABLES X
# ==============================================================================

scaler_x = MinMaxScaler()


X_train_scaled = scaler_x.fit_transform(
    X_train_imputed
)


X_test_scaled = scaler_x.transform(
    X_test_imputed
)


# ==============================================================================
# 13. ESCALAMIENTO DEL TARGET
# ==============================================================================

scaler_y = MinMaxScaler()


y_train_scaled = scaler_y.fit_transform(

    y_train.values.reshape(-1, 1)

).ravel()


y_test_scaled = scaler_y.transform(

    y_test.values.reshape(-1, 1)

).ravel()


# ==============================================================================
# 14. CREACIÓN DE LA RED NEURONAL
# ==============================================================================

model_nn = MLPRegressor(

    hidden_layer_sizes=(256, 128, 64),

    activation="relu",

    solver="adam",

    learning_rate_init=0.001,

    max_iter=3000,

    tol=1e-6,

    random_state=42

)


# ==============================================================================
# 15. INFORMACIÓN DEL ENTRENAMIENTO
# ==============================================================================

print()
print("=" * 80)

print(
    "   INNOVATECH SOLUTIONS S.A.C."
)

print(
    "   RED NEURONAL PARA PREDICCIÓN DE HORAS-HOMBRE"
)

print("=" * 80)


print()
print("[1] INFORMACIÓN DEL DATASET")
print("-" * 80)


print(
    f"[+] Archivo                  : 20k.csv"
)


print(
    f"[+] Registros procesados    : {len(df):,}"
)


print(
    f"[+] Variables de entrada    : {X.shape[1]}"
)


print(
    f"[+] Variable objetivo       : {columna_target}"
)


# ==============================================================================
# 16. MOSTRAR DIVISIÓN
# ==============================================================================

print()
print("[2] DIVISIÓN TRAIN / TEST")
print("-" * 80)


print(
    f"[+] Datos totales            : {len(df):,}"
)


print(
    f"[+] Entrenamiento 80%        : {len(X_train):,}"
)


print(
    f"[+] Prueba 20%               : {len(X_test):,}"
)


# ==============================================================================
# 17. ENTRENAMIENTO
# ==============================================================================

print()
print("[3] ENTRENAMIENTO DE LA RED NEURONAL")
print("-" * 80)


print(
    "[~] Entrenando MLPRegressor..."
)


model_nn.fit(

    X_train_scaled,

    y_train_scaled

)


print(
    "[✓] Red neuronal entrenada correctamente."
)


# ==============================================================================
# 18. PREDICCIÓN SOBRE DATOS DE PRUEBA
# ==============================================================================

pred_test_scaled = model_nn.predict(

    X_test_scaled

)


# ==============================================================================
# 19. REGRESAR PREDICCIONES A ESCALA REAL
# ==============================================================================

y_pred = scaler_y.inverse_transform(

    pred_test_scaled.reshape(-1, 1)

).ravel()


# ==============================================================================
# 20. EVALUACIÓN
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
# 21. MOSTRAR MÉTRICAS
# ==============================================================================

print()
print("[4] EVALUACIÓN DE LA RED NEURONAL")
print("-" * 80)


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
# 22. INFORMACIÓN DEL TARGET
# ==============================================================================

print()
print("[5] INFORMACIÓN DE HORAS-HOMBRE")
print("-" * 80)


print(
    f"[+] Mínimo                 : "
    f"{y.min():.2f} horas"
)


print(
    f"[+] Máximo                 : "
    f"{y.max():.2f} horas"
)


print(
    f"[+] Promedio               : "
    f"{y.mean():.2f} horas"
)


# ==============================================================================
# 23. FUNCIÓN DE PREDICCIÓN
# ==============================================================================

def predecir_nn_desde_diccionario(datos_diccionario):

    """
    Recibe los requerimientos de un nuevo proyecto
    y devuelve las horas-hombre estimadas por
    la red neuronal.
    """

    # --------------------------------------------------------------------------
    # Crear DataFrame
    # --------------------------------------------------------------------------

    nuevo_df = pd.DataFrame(

        [datos_diccionario]

    )


    # --------------------------------------------------------------------------
    # Validar campos
    # --------------------------------------------------------------------------

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

            "Faltan datos requeridos: "

            + ", ".join(campos_faltantes)

        )


    # --------------------------------------------------------------------------
    # Convertir variables numéricas
    # --------------------------------------------------------------------------

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


    # --------------------------------------------------------------------------
    # Crear presupuesto por día
    # --------------------------------------------------------------------------

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


    # --------------------------------------------------------------------------
    # One-Hot Encoding
    # --------------------------------------------------------------------------

    nuevo_df = pd.get_dummies(

        nuevo_df

    )


    # --------------------------------------------------------------------------
    # Alinear columnas
    # --------------------------------------------------------------------------

    nuevo_df = nuevo_df.reindex(

        columns=columnas_modelo,

        fill_value=0

    )


    # --------------------------------------------------------------------------
    # Imputación
    # --------------------------------------------------------------------------

    nuevo_imputado = imputer.transform(

        nuevo_df

    )


    # --------------------------------------------------------------------------
    # Escalamiento
    # --------------------------------------------------------------------------

    nuevo_escalado = scaler_x.transform(

        nuevo_imputado

    )


    # --------------------------------------------------------------------------
    # Predicción
    # --------------------------------------------------------------------------

    pred_escalada = model_nn.predict(

        nuevo_escalado

    )


    # --------------------------------------------------------------------------
    # Regresar a escala original
    # --------------------------------------------------------------------------

    pred_real = scaler_y.inverse_transform(

        pred_escalada.reshape(-1, 1)

    ).ravel()


    return float(
        pred_real[0]
    )


# ==============================================================================
# 24. FUNCIÓN COMPLETA DE COTIZACIÓN
# ==============================================================================

def generar_cotizacion_nn(

    datos_diccionario,

    tarifa_hora_usd=35.0

):

    """
    Genera una cotización utilizando
    la red neuronal.
    """

    horas_estimadas = predecir_nn_desde_diccionario(

        datos_diccionario

    )


    costo_estimado = (

        horas_estimadas

        * tarifa_hora_usd

    )


    return {

        "horas_hombre_estimadas":
            round(
                horas_estimadas,
                2
            ),

        "tarifa_hora_usd":
            round(
                tarifa_hora_usd,
                2
            ),

        "costo_estimado_usd":
            round(
                costo_estimado,
                2
            ),

        "tiempo_respuesta":
            "< 1 segundo"

    }


# ==============================================================================
# 25. PRUEBA DE PREDICCIÓN
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


    resultado = generar_cotizacion_nn(

        cliente_demo,

        tarifa_hora_usd=35.0

    )


    print()
    print("[6] PREDICCIÓN DE UN NUEVO PROYECTO")
    print("-" * 80)


    print(
        f"[+] Tipo de servicio       : "
        f"{cliente_demo['tipo_servicio']}"
    )


    print(
        f"[+] Presupuesto             : "
        f"${cliente_demo['presupuesto_estimado']:,.2f}"
    )


    print(
        f"[+] Deadline                : "
        f"{cliente_demo['deadline_dias']} días"
    )


    print(
        f"[+] Cantidad de bugs       : "
        f"{cliente_demo['cantidad_bugs']}"
    )


    print(
        f"[+] Desarrolladores        : "
        f"{cliente_demo['numero_desarrolladores']}"
    )


    print(
        f"[+] Infraestructura nube   : "
        f"{cliente_demo['infraestructura_nube_previa']}"
    )


    print(
        f"[+] Renovación contrato    : "
        f"{cliente_demo['renovacion_contrato']}"
    )


    print()
    print("[RESULTADO]")
    print("-" * 80)


    print(
        f"[+] Horas-hombre estimadas : "
        f"{resultado['horas_hombre_estimadas']:.2f} horas"
    )


    print(
        f"[+] Tarifa por hora        : "
        f"${resultado['tarifa_hora_usd']:.2f} USD"
    )


    print(
        f"[+] Costo estimado         : "
        f"${resultado['costo_estimado_usd']:,.2f} USD"
    )


    print(
        f"[+] Tiempo de respuesta    : "
        f"{resultado['tiempo_respuesta']}"
    )


    print()
    print("=" * 80)

    print(
        "   PREDICCIÓN FINALIZADA CORRECTAMENTE"
    )

    print("=" * 80)



