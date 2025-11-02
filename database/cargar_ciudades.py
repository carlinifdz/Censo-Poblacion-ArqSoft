import pandas as pd

# Cargar el CSV
df = pd.read_csv("database/colonias.csv")

# Calcular promedio de coordenadas por ciudad
centros = df.groupby("NOM_MUN")[["LAT_DECIMAL", "LON_DECIMAL"]].mean().reset_index()

# Guardar resultado
centros.to_csv("centros_por_ciudad.csv", index=False)

print(centros)