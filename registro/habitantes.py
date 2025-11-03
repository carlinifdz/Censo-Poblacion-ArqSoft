from database.conn import get_connection
from datetime import date

class habitante:
    def __init__ (self):
        pass

    def registrar_habitante(self, nombre, fecha_nac, sexo, domicilio_id, act_eco):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            resultado = self.buscar_habitante(nombre, domicilio_id)

            if resultado:
                print("Habitante ya registrado.")
                return False
            else:
                query = """
                    INSERT INTO habitantes (nombre, fecha_nac, sexo, domicilio_id, act_eco)
                    VALUES (%s, %s, %s, %s, %s)
                """
                values = (nombre, fecha_nac, sexo, domicilio_id, act_eco)
                cursor.execute(query, values)
                connection.commit()
                print("Habitante registrado correctamente.")
                return True

        except Exception as e:
            print("Error al registrar habitante:", e)
            return False

        finally:
            cursor.close()
            connection.close()

    
    def buscar_habitante(self, nombre, domicilio_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            query = """
                SELECT id, nombre, fecha_nac, sexo, domicilio_id, act_eco
                FROM habitantes
                WHERE nombre = %s AND domicilio_id = %s
            """
            values = (nombre, domicilio_id)
            cursor.execute(query, values)
            result = cursor.fetchone()

            if result:
                return result
            else:
                return False
        finally:
            cursor.close()
            connection.close()
    
    def editar_habitante(self, nombre, domicilio_id, nuevo_nombre=None, nuevo_sexo=None, nuevo_act_eco=None, nuevo_fecha_nac = None):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            resultado = self.buscar_habitante(nombre, domicilio_id)

            if not resultado:
                print("No se encontró el habitante a editar.")
                return False

            nuevo_nombre = nuevo_nombre or nombre

            resultado_existe = self.buscar_habitante(nuevo_nombre, domicilio_id)

            if resultado_existe and (resultado_existe[0] != resultado[0]):
                print("Ya existe un habitante con ese nombre en el mismo domicilio.")
                return False

            campos = []
            valores = []

            if nuevo_nombre:
                campos.append("nombre = %s")
                valores.append(nuevo_nombre)
            if nuevo_sexo:
                campos.append("sexo = %s")
                valores.append(nuevo_sexo)
            if nuevo_act_eco:
                campos.append("act_eco = %s")
                valores.append(nuevo_act_eco)
            if nuevo_fecha_nac:
                campos.append("fecha_nac = %s")
                valores.append(nuevo_fecha_nac)

            if not campos:
                print("No se especificaron campos a actualizar.")
                return False

            valores.append(resultado[0])

            query = f"UPDATE habitantes SET {', '.join(campos)} WHERE id = %s"

            cursor.execute(query, tuple(valores))
            connection.commit()

            if cursor.rowcount > 0:
                print("Habitante actualizado correctamente.")
                return True
            else:
                print("No se realizaron cambios.")
                return False

        except Exception as e:
            print("Error al editar habitante:", e)
            return False

        finally:
            cursor.close()
            connection.close()
    
    def eliminar_habitante(self, nombre, domicilio_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            resultado = self.buscar_habitante(nombre, domicilio_id)

            if not resultado:
                print("No se encontró el habitante a eliminar.")
                return False

            query = "DELETE FROM habitantes WHERE id = %s"
            values = (resultado[0],)
            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount > 0:
                print("Habitante eliminado correctamente.")
                return True
            else:
                print("No se eliminó ningún registro (puede que ya no exista).")
                return False

        except Exception as e:
            print("Error al eliminar habitante:", e)
            return False

        finally:
            cursor.close()
            connection.close()

    def obtener_edad(self, nombre, domicilio_id):

        resultado = self.buscar_habitante(nombre, domicilio_id)

        if not resultado:
            print("No se encontró el habitante.")
            return None

        fecha_nac = resultado[2]
        hoy = date.today()
        
        # Calcular edad
        edad = hoy.year - fecha_nac.year
        if (hoy.month, hoy.day) < (fecha_nac.month, fecha_nac.day):
            edad -= 1

        return edad

if __name__ == "__main__":
    hab = habitante()
    
    #edad = hab.obtener_edad("Carlo Hiram Fernandez Salinas", 6)

    #print(edad)

    #YYYY-MM-DD
    fecha_nac = date(2004, 11, 11)
    hab.registrar_habitante("Carlos Hiram Fernandez Salinas", fecha_nac, 'M', 5, "Ninguna")
    #hab.editar_habitante("Carlo Hiram Fernandez Salinas", 6 ,nuevo_nombre = "Carlo Manuel Fernandez Salinas,")

    #hab.eliminar_habitante("Carlo Hiram Fernandez Salinas", 1)