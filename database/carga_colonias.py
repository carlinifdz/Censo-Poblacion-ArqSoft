import pandas as pd
import numpy as np
from conn import get_connection

df = pd.read_csv("database/colonias.csv")

connection = get_connection()
cursor = connection.cursor()

for i in range (len(df)):
    nombre = df['NOM_LOC'].iloc[i]
    localidad = df['NOM_MUN'].iloc[i]
    query = """INSERT INTO colonias (nombre, localidad) VALUES(%s,%s) """
    values = (nombre, localidad)

    cursor.execute(query, values)

connection.commit()
cursor.close()
connection.close()
