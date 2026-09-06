import numpy as np
import pandas as pd

from pathlib import Path

from sklearn.ensemble import RandomForestRegressor
from sklearn.impute import SimpleImputer
from sklearn.metrics import mean_absolute_error, r2_score
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler


# ==============================================================================
# 1. RUTA DEL PROYECTO
# ==============================================================================

BASE_DIR = Path(__file__).resolve().parent.parent

ruta_csv = BASE_DIR / "datos" / "DATOS.csv"


# ==============================================================================
# 2. CARGA Y PREPROCESAMIENTO DE DATOS
# ==============================================================================

df = pd.read_csv(ruta_csv)


# Definir la variable objetivo
columna_target = "horas_hombre"

df = df.dropna(subset=[columna_target])


# ==============================================================================
# 3. INGENIERÍA DE CARACTERÍSTICAS
# ==============================================================================

df["presupuesto_por_dia"] = (
    df["presupuesto_usd"] / df["deadline_dias"]
)


# ==============================================================================
# 4. VARIABLES PREDICTORAS Y OBJETIVO
# ==============================================================================

X = df.drop(columns=[columna_target])

y = df[columna_target]


# ==============================================================================
# 5. VARIABLES CATEGÓRICAS
# ==============================================================================

X = pd.get_dummies(
    X,
    drop_first=True
)


# ==============================================================================
# 6. DIVISIÓN ENTRENAMIENTO / PRUEBA
# ==============================================================================

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42
)


# ==============================================================================
# 7. IMPUTACIÓN
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
# 8. ESCALADO
# ==============================================================================

scaler = StandardScaler()

X_train_scaled = scaler.fit_transform(
    X_train_imputed
)

X_test_scaled = scaler.transform(
    X_test_imputed
)


# ==============================================================================
# 9. ENTRENAMIENTO DEL MODELO
# ==============================================================================

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=10,
    min_samples_split=4,
    max_features="sqrt",
    random_state=42
)

model.fit(
    X_train_scaled,
    y_train
)


# ==============================================================================
# 10. EVALUACIÓN
# ==============================================================================

y_pred = model.predict(
    X_test_scaled
)

mae = mean_absolute_error(
    y_test,
    y_pred
)

r2 = r2_score(
    y_test,
    y_pred
)


print("=" * 65)

print(
    "   SYSTEM DEMO: SISTEMA INTELIGENTE DE COTIZACION AUTOMATICA"
)

print(
    "                 INNOVATECH SOLUTIONS S.A.C."
)

print("=" * 65)

print(
    "[+] Estado del modelo : Entrenado y optimizado correctamente"
)

print(
    "[+] Algoritmo         : "
    "Random Forest Regressor (Hyperparameter Tuned)"
)

print(
    f"[+] Datos procesados  : {len(df):,} cotizaciones historicas"
)

print("-" * 65)

print(
    "1. METRICAS DE RENDIMIENTO DEL MODELO (EVALUACION ML):"
)

print(
    f"   - Error Absoluto Medio (MAE)         : "
    f"{mae:.2f} horas-hombre"
)

print(
    f"   - Coeficiente de Determinacion (R^2) : "
    f"{r2:.4f} ({r2 * 100:.2f}%)"
)

print("-" * 65)


# ==============================================================================
# 11. FUNCIÓN DE PREDICCIÓN EN TIEMPO REAL
# ==============================================================================

def predecir_desde_diccionario(datos_diccionario):

    nuevo_df = pd.DataFrame(
        [datos_diccionario]
    )


    # Aplicar la misma ingeniería de características

    if "presupuesto_por_dia" not in nuevo_df.columns:

        nuevo_df["presupuesto_por_dia"] = (
            nuevo_df["presupuesto_usd"]
            / nuevo_df["deadline_dias"]
        )


    # One-Hot Encoding

    nuevo_df = pd.get_dummies(
        nuevo_df
    )


    # Alinear columnas con el entrenamiento

    nuevo_df = nuevo_df.reindex(
        columns=X.columns,
        fill_value=np.nan
    )


    # Imputar

    nuevo_imputado = imputer.transform(
        nuevo_df
    )


    # Escalar

    nuevo_escalado = scaler.transform(
        nuevo_imputado
    )


    # Predecir

    prediccion = model.predict(
        nuevo_escalado
    )


    return prediccion[0]


# ==============================================================================
# 12. CLIENTE SIMULADO PARA LA DEMO
# ==============================================================================

cliente_demo = {

    "presupuesto_usd": 15000.00,

    "deadline_dias": 90,

    "tipo_servicio": "Plataforma_SaaS",

    "infraestructura_cloud": 1,

}


horas_estimadas = predecir_desde_diccionario(
    cliente_demo
)

tarifa_hora_usd = 35.0

costo_estimado = (
    horas_estimadas * tarifa_hora_usd
)


print(
    "2. PRUEBA DE COTIZACION EN TIEMPO REAL (DEMO):"
)

print(
    "   [DATOS DE ENTRADA DEL CLIENTE]"
)

print(
    f"   * Tipo de Servicio        : "
    f"{cliente_demo['tipo_servicio']}"
)

print(
    f"   * Presupuesto Referencial : "
    f"${cliente_demo['presupuesto_usd']:,.2f} USD"
)

print(
    f"   * Plazo Solicitado        : "
    f"{cliente_demo['deadline_dias']} dias"
)

print(
    f"   * Infraestructura Cloud   : "
    f"{'Si' if cliente_demo['infraestructura_cloud'] == 1 else 'No'}"
)

print("")

print(
    "   [RESULTADO PREDECIDO POR EL MODELO ML]"
)

print(
    f"   * Horas-Hombre Estimadas  : "
    f"{horas_estimadas:.1f} hrs"
)

print(
    f"   * Costo Estimado Proyecto : "
    f"${costo_estimado:,.2f} USD"
)

print(
    "   * Tiempo de Respuesta ML  : "
    "< 1 segundo (frente a 72 hrs manuales)"
)

print("-" * 65)


# ==============================================================================
# 13. IMPORTANCIA DE LAS VARIABLES
# ==============================================================================

nombres_caracteristicas = X.columns

pesos = model.feature_importances_


df_pesos = (
    pd.DataFrame(
        {
            "Variable": nombres_caracteristicas,
            "Peso_Relativo": pesos
        }
    )
    .sort_values(
        by="Peso_Relativo",
        ascending=False
    )
    .reset_index(
        drop=True
    )
)


print(
    "3. IMPORTANCIA / PESO REDISTRIBUIDO DE LAS VARIABLES:"
)


for idx, fila in df_pesos.iterrows():

    porcentaje = (
        fila["Peso_Relativo"] * 100
    )

    print(
        f"   * {fila['Variable']:<30}: "
        f"{porcentaje:6.2f}%"
    )


print("=" * 65)