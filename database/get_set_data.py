from database.conn import get_connection
import mysql.connector

def fetch_domicilios():
    connection = get_connection()

    if connection is None:
        print("Error en la conexion")
        return

    try:
        cursor = connection.cursor()
        query = "SELECT * FROM domicilios"
        cursor.execute(query)
        results = cursor.fetchall()
        for row in results:
            print(row)
        
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()

def obtener_municipios():
    connection = get_connection()
    if connection is None:
        return []
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT DISTINCT localidad FROM colonias ORDER BY localidad")
            return [r[0] for r in cursor.fetchall()]
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return

def obtener_colonias(municipio):
    connection = get_connection()
    if connection is None:
        return []
    try:
        with connection.cursor() as cursor:
            query = "SELECT nombre FROM colonias where localidad = %s "
            values = (municipio,)

            cursor.execute(query, values)

            return [r[0] for r in cursor.fetchall()]
    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()
    return

if __name__ == "__main__":
    fetch_domicilios()