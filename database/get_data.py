from conn import get_connection
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

if __name__ == "__main__":
    fetch_domicilios()