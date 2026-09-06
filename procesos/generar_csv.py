import numpy as np
import pandas as pd

# Fijar semilla para que los datos sean estables
np.random.seed(42)
n_registros = 2000

# 1. Generar datos lógicos y coherentes para las 2,000 cotizaciones
id_proyecto = [f"PRJ-{i:05d}" for i in range(1, n_registros + 1)]
presupuesto_estimado = np.random.uniform(5000, 80000, n_registros)
deadline_dias = np.random.randint(30, 365, n_registros)
cantidad_bugs = np.random.randint(0, 15, n_registros)
numero_desarrolladores = np.random.randint(1, 10, n_registros)

tipos_servicio = ["Sistema SaaS", "E-commerce", "App Móvil", "Portal Web"]
tipo_servicio = np.random.choice(tipos_servicio, n_registros)

nubes = ["Sí", "No"]
infraestructura_nube_previa = np.random.choice(nubes, n_registros)

renovaciones = ["Sí", "No"]
renovacion_contrato = np.random.choice(renovaciones, n_registros)

# 2. Variable objetivo (horas_hombre_invertidas)
horas_base = (presupuesto_estimado * 0.02) + (numero_desarrolladores * 45) + (cantidad_bugs * 12)
ruido = np.random.normal(0, 25, n_registros)
horas_hombre_invertidas = np.clip(horas_base + ruido, 100, 5000)

# 3. Construir el DataFrame y guardarlo como 2k.csv
df_nuevo = pd.DataFrame({
    "id_proyecto": id_proyecto,
    "presupuesto_estimado": presupuesto_estimado.round(2),
    "deadline_dias": deadline_dias,
    "cantidad_bugs": cantidad_bugs,
    "numero_desarrolladores": numero_desarrolladores,
    "tipo_servicio": tipo_servicio,
    "infraestructura_nube_previa": infraestructura_nube_previa,
    "renovacion_contrato": renovacion_contrato,
    "horas_hombre_invertidas": horas_hombre_invertidas.round(1),
    "fecha_entrega": pd.date_range(start="2024-01-01", periods=n_registros, freq="h").strftime("%Y-%m-%d")
})

df_nuevo.to_csv("2k.csv", index=False)
print("[+] ¡Archivo '2k.csv' regenerado con éxito con 2,000 registros!")