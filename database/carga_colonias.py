import pandas as pd
import numpy as np
from conn import get_connection

df = pd.read_csv("database/colonias.csv")

connection = get_connection()
cursor = connection.cursor()

for i in range (len(df)):
    id = df['CVEGEO'].iloc[i]
    nombre = df['NOM_LOC'].iloc[i]
    localidad = df['NOM_MUN'].iloc[i]
    ambito = df['AMBITO'].iloc[i]
    query = """INSERT INTO colonias (id, nombre, localidad, ambito) VALUES(%s,%s,%s,%s) """
    values = (int(np.int64(id)), nombre, localidad, ambito)

    cursor.execute(query, values)

connection.commit()
cursor.close()
connection.close()
