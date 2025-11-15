from database.conn import get_connection
from datetime import date

class colonia:
    def __init__ (self):
        pass

    def registrar_colonia(self, nombre, localidad):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            resultado = self.buscar_colonia(nombre, localidad)

            if resultado:
                print("colonia ya registrada.")
                return False
            else:
                query = """
                    INSERT INTO colonias (nombre, localidad)
                    VALUES (%s, %s)
                """
                values = (nombre, localidad)
                cursor.execute(query, values)
                connection.commit()
                print("colonia registrada correctamente.")
                return True

        except Exception as e:
            print("Error al registrar colonia:", e)
            return False

        finally:
            cursor.close()
            connection.close()

    def buscar_colonia(self, nombre, localidad):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            query = """
                SELECT id, nombre, localidad
                FROM colonias
                WHERE nombre = %s AND localidad = %s
            """
            values = (nombre, localidad)
            cursor.execute(query, values)
            result = cursor.fetchone()

            if result:
                return result
            else:
                return False
        finally:
            cursor.close()
            connection.close()
    
    def editar_colonia(self, nombre, localidad, nuevo_nombre=None):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            resultado = self.buscar_colonia(nombre, localidad)

            if not resultado:
                print("No se encontró el colonia a editar.")
                return False
            
            resultado_existe = self.buscar_colonia(nuevo_nombre, localidad)

            if resultado_existe and (resultado_existe[0] != resultado[0]):
                print("Ya existe uno con ese nombre")
                return False

            campos = []
            valores = []

            if nuevo_nombre:
                campos.append("nombre = %s")
                valores.append(nuevo_nombre)


            if not campos:
                print("No se especificaron campos a actualizar.")
                return False

            valores.append(resultado[0])

            query = f"UPDATE colonias SET {', '.join(campos)} WHERE id = %s"

            cursor.execute(query, tuple(valores))
            connection.commit()

            if cursor.rowcount > 0:
                print("Colonia actualizada correctamente.")
                return True
            else:
                print("No se realizaron cambios.")
                return False

        except Exception as e:
            print("Error al editar colonia:", e)
            return False

        finally:
            cursor.close()
            connection.close()
    
    def eliminar_colonia(self, nombre, localidad):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            resultado = self.buscar_colonia(nombre, localidad)

            if not resultado:
                print("No se encontró la colonia a eliminar.")
                return False

            query = "DELETE FROM colonias WHERE id = %s"
            values = (resultado[0],)
            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount > 0:
                print("Colonia eliminada correctamente.")
                return True
            else:
                print("No se eliminó ningún registro (puede que ya no exista).")
                return False

        except Exception as e:
            print("Error al eliminar colonia:", e)
            return False

        finally:
            cursor.close()
            connection.close()


