from database.conn import get_connection

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
            
            nuevo_calle = nuevo_calle or calle
            nuevo_numero = nuevo_numero or numero

            resultado_existe = self.buscar_domicilio(nuevo_calle, nuevo_numero, colonia_id)

            if resultado_existe and (resultado_existe[0] != resultado[0]):
                print("Ya existe uno con ese nombre")
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

            valores.append(valores[0])

            query = f"UPDATE domicilios SET {', '.join(campos)} WHERE id = %s"
            
            cursor.execute(query, tuple(valores))
            connection.commit()

            if cursor.rowcount > 0:
                print("Domicilio actualizado correctamente.")
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

    def obtener_habitantes(self,calle, numero, colonia_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            resultado = self.buscar_domicilio(calle, numero, colonia_id)

            if not resultado:
                print("No se encontró el domicilio.")
                return []
            
            query = "SELECT id, nombre, fecha_nac, sexo, act_eco FROM habitantes WHERE domicilio_id = %s"
            values = (resultado[0],)
            cursor.execute(query,values)
            habitantes = cursor.fetchall()
            cantidad = len(habitantes)
            
            if cantidad > 0:
                print(f"Habitantes en el domicilio: {cantidad}")
                return habitantes
            else:
                print("No hay nadie viviendo en es domicilio")
            
        except Exception as e:
            print("Error al contar habitantes: ", e)
            return []

        finally:
            cursor.close()
            connection.close()

    def contar_habitantes(self, calle, numero, colonia_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            resultado = self.buscar_domicilio(calle, numero, colonia_id)

            if not resultado:
                print("No se encontró el domicilio.")
                return 0
            
            query = "SELECT COUNT(*) FROM habitantes WHERE domicilio_id = %s"
            values = (resultado[0],)
            cursor.execute(query,values)
            cantidad = cursor.fetchone()[0]
            
            if cantidad > 0:
                print(f"Habitantes en el domicilio: {cantidad}")
                return cantidad
            else:
                print("No hay nadie viviendo en ese domicilio")
                return 0
            
        except Exception as e:
            print("Error al contar habitantes: ", e)
            return 0

        finally:
            cursor.close()
            connection.close()

    def contar_habitantes_colonia(self, colonia_id):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            cursor.execute("SELECT id FROM colonias WHERE id = %s", (colonia_id,))
            colonia = cursor.fetchone()

            if not colonia:
                print("No se encontró la colonia.")
                return 0
            
            query = """
            SELECT COUNT(h.id)
            FROM habitantes h
            JOIN domicilios d ON h.domicilio_id = d.id
            WHERE d.colonia_id = %s
            """
            cursor.execute(query,(colonia_id,))
            cantidad = cursor.fetchone()[0]
            
            if cantidad > 0:
                print(f"Habitantes en la colonia: {cantidad}")
                return cantidad
            else:
                print("No hay nadie viviendo en esa colonia")
                return 0
            
        except Exception as e:
            print("Error al contar habitantes: ", e)
            return 0

        finally:
            cursor.close()
            connection.close()

    def obtener_habitantes_colonia(self, colonia_id):
        connection = get_connection()
        cursor = connection.cursor(dictionary=True)

        try:
            cursor.execute("SELECT nombre FROM colonias WHERE id = %s", (colonia_id,))
            colonia = cursor.fetchone()

            if not colonia:
                print("No se encontró la colonia.")
                return []

            query = """
                SELECT 
                    h.id AS habitante_id,
                    h.nombre AS habitante_nombre,
                    h.fecha_nac,
                    h.sexo,
                    h.act_eco,
                    d.id AS domicilio_id,
                    d.calle,
                    d.numero,
                    c.nombre AS colonia_nombre
                FROM habitantes h
                JOIN domicilios d ON h.domicilio_id = d.id
                JOIN colonias c ON d.colonia_id = c.id
                WHERE c.id = %s
                ORDER BY d.calle, d.numero, h.nombre
            """

            cursor.execute(query, (colonia_id,))
            habitantes = cursor.fetchall()

            if habitantes:
                print(f"Se encontraron {len(habitantes)} habitantes en la colonia '{colonia['nombre']}'.")
                return habitantes
            else:
                print(f"No hay habitantes registrados en la colonia '{colonia['nombre']}'.")
                return []

        except Exception as e:
            print("Error al obtener habitantes por colonia:", e)
            return []

        finally:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    dom = domicilio()

    #dom.registrar_domicilio("Vivienda de concreto", "Ildelfonso Fuentes", 668, 50300001)
    #dom.editar_domicilio("Ildelfonso Fuentes", 668, 50300001,nuevo_calle="Ildelfonso Flores")
    #dom.eliminar_domicilio("Ildelfonso Flores", 668, 50300001)
    #conteo = dom.contar_habitantes("Ildelfonso Fuentes", 668, 50300001)
    #conteo = dom.contar_habitantes_colonia(50300001)
    #conteo = dom.obtener_habitantes_colonia(50300001)
    #for persona in conteo:
    #    print(f"{persona['habitante_nombre']} ({persona['sexo']}) - {persona['calle']} #{persona['numero']}, {persona['colonia_nombre']}")