import pandas as pd
from conn import get_connection

df = pd.read_csv("database/colonias.csv")

connection = get_connection()
cursor = connection.cursor()

for i in range (len(df)):
    nombre = df['NOM_LOC'].iloc[i]
    localidad = df['NOM_MUN'].iloc[i]
    ambito = df['AMBITO'].iloc[i]
    latitud = df['LAT_DECIMAL'].iloc[i]
    longitud = df['LON_DECIMAL'].iloc[i]
    query = """INSERT INTO colonias (nombre, localidad, ambito, latitud, longitud) VALUES(%s,%s,%s,%s,%s) """
    values = (nombre, localidad, ambito, latitud, longitud)

    cursor.execute(query, values)

connection.commit()
cursor.close()
connection.close()
