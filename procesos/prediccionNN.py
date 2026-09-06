import numpy as np
import pandas as pd

from pathlib import Path

from sklearn.impute import SimpleImputer
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPRegressor
from sklearn.preprocessing import MinMaxScaler


# ==============================================================================
# 1. RUTAS DEL PROYECTO
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ruta_csv = BASE_DIR / "datos" / "20k.csv"


# ==============================================================================
# 2. CARGA Y ENTRENAMIENTO GLOBAL
# ==============================================================================

df = pd.read_csv(ruta_csv)

columna_target = "horas_hombre_invertidas"

df = df.dropna(subset=[columna_target])


columnas_a_excluir = [
    "id_proyecto",
    "fecha_entrega",
    columna_target
]


X_temp = df.drop(
    columns=[
        col
        for col in columnas_a_excluir
        if col in df.columns
    ]
)


# ==============================================================================
# 3. CREACIÓN DE VARIABLE
# ==============================================================================

X_temp["presupuesto_por_dia"] = (
    X_temp["presupuesto_estimado"]
    / X_temp["deadline_dias"]
)


# ==============================================================================
# 4. CODIFICACIÓN
# ==============================================================================

X = pd.get_dummies(
    X_temp,
    drop_first=True
)

y = df[columna_target]


# ==============================================================================
# 5. DIVISIÓN TRAIN / TEST
# ==============================================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ==============================================================================
# 6. IMPUTACIÓN
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
# 7. ESCALADO DE VARIABLES
# ==============================================================================

scaler_x = MinMaxScaler()

X_train_scaled = scaler_x.fit_transform(
    X_train_imputed
)

X_test_scaled = scaler_x.transform(
    X_test_imputed
)


# ==============================================================================
# 8. ESCALADO DEL TARGET
# ==============================================================================

scaler_y = MinMaxScaler()

y_train_scaled = scaler_y.fit_transform(
    y_train.values.reshape(-1, 1)
).ravel()

y_test_scaled = scaler_y.transform(
    y_test.values.reshape(-1, 1)
).ravel()


# ==============================================================================
# 9. ENTRENAMIENTO DE LA RED NEURONAL
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


print(
    "[~] Entrenando red neuronal para "
    "Innovatech Solutions S.A.C..."
)


model_nn.fit(
    X_train_scaled,
    y_train_scaled
)


print("[✓] Red neuronal entrenada correctamente.")


# ==============================================================================
# 10. FUNCIÓN DE PREDICCIÓN
# ==============================================================================

def predecir_nn_desde_diccionario(datos_diccionario):

    nuevo_df = pd.DataFrame(
        [datos_diccionario]
    )


    # --------------------------------------------------
    # Crear presupuesto_por_dia
    # --------------------------------------------------

    if "presupuesto_por_dia" not in nuevo_df.columns:

        nuevo_df["presupuesto_por_dia"] = (
            nuevo_df["presupuesto_estimado"]
            / nuevo_df["deadline_dias"]
        )


    # --------------------------------------------------
    # Convertir variables categóricas
    # --------------------------------------------------

    nuevo_df = pd.get_dummies(
        nuevo_df
    )


    # --------------------------------------------------
    # Alinear columnas con el entrenamiento
    # --------------------------------------------------

    nuevo_df = nuevo_df.reindex(
        columns=X.columns,
        fill_value=0
    )


    # --------------------------------------------------
    # Imputar
    # --------------------------------------------------

    nuevo_imputado = imputer.transform(
        nuevo_df
    )


    # --------------------------------------------------
    # Escalar
    # --------------------------------------------------

    nuevo_escalado = scaler_x.transform(
        nuevo_imputado
    )


    # --------------------------------------------------
    # Predicción
    # --------------------------------------------------

    pred_escalada = model_nn.predict(
        nuevo_escalado
    )


    # --------------------------------------------------
    # Regresar a escala original
    # --------------------------------------------------

    pred_real = scaler_y.inverse_transform(
        pred_escalada.reshape(-1, 1)
    ).ravel()


    return pred_real[0]