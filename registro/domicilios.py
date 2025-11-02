from database import get_connection

class domicilio:
    def __init__ (self):
        pass

    def registrar_domicilio(self, tipo_casa, calle, numero, colonia_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            resultado = self.buscar_domicilio(calle, numero, colonia_id)

            if resultado:
                print("domicilio ya registrado.")
                return False
            else:
                query = """
                    INSERT INTO domicilios (tipo_casa, calle, numero, colonia_id)
                    VALUES (%s, %s, %s, %s)
                """
                values = (tipo_casa, calle, numero, colonia_id)
                cursor.execute(query, values)
                connection.commit()
                print("domicilio registrado correctamente.")
                return True

        except Exception as e:
            print("Error al registrar domicilio:", e)
            return False

        finally:
            cursor.close()
            connection.close()

    def buscar_domicilio(self, calle, numero, colonia_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            query = """
                SELECT id, tipo_casa, calle, numero, colonia_id
                FROM domicilios
                WHERE calle = %s AND numero = %s AND colonia_id = %s 
            """
            values = (calle, numero, colonia_id)
            cursor.execute(query, values)
            result = cursor.fetchone()

            if result:
                return result
            else:
                return False
        finally:
            cursor.close()
            connection.close()
    
    def editar_domicilio(self, calle, numero, colonia_id, nuevo_calle=None, nuevo_numero=None, nuevo_tipo_casa=None):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            resultado = self.buscar_domicilio(calle, numero, colonia_id)

            if not resultado:
                print("No se encontró el domicilio a editar.")
                return False

            campos = []
            valores = []

            if nuevo_calle:
                campos.append("calle = %s")
                valores.append(nuevo_calle)
            if nuevo_numero:
                campos.append("numero = %s")
                valores.append(nuevo_numero)
            if nuevo_tipo_casa:
                campos.append("tipo_casa = %s")
                valores.append(nuevo_tipo_casa)

            if not campos:
                print("No se especificaron campos a actualizar.")
                return False

            valores.append(calle)
            valores.append(numero)
            valores.append(colonia_id)

            query = f"UPDATE domicilios SET {', '.join(campos)} WHERE calle = %s AND numero = %s AND colonia_id = %s"

            cursor.execute(query, tuple(valores))
            connection.commit()

            if cursor.rowcount > 0:
                print("domicilio actualizado correctamente.")
                return True
            else:
                print("No se realizaron cambios.")
                return False

        except Exception as e:
            print("Error al editar domicilio:", e)
            return False

        finally:
            cursor.close()
            connection.close()
    
    def eliminar_domicilio(self, calle, numero, colonia_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            resultado = self.buscar_domicilio(calle, numero, colonia_id)

            if not resultado:
                print("No se encontró el domicilio a eliminar.")
                return False

            query = "DELETE FROM domicilios WHERE id = %s"
            values = (resultado[0],)
            cursor.execute(query, values)
            connection.commit()

            if cursor.rowcount > 0:
                print("Domicilio eliminado correctamente.")
                return True
            else:
                print("No se eliminó ningún registro.")
                return False

        except Exception as e:
            print("Error al eliminar domicilio:", e)
            return False

        finally:
            cursor.close()
            connection.close()