from database.conn import get_connection

class usuario:
    def __init__ (self):
        pass

    def registrar_usuario(self, user, password):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            resultado = self.buscar_usuario(user)

            if resultado:
                print("usuario ya registrado.")
                return False
            else:
                query = """
                    INSERT INTO usuarios (user, password)   
                    VALUES (%s, %s)
                """
                values = (user, password)
                cursor.execute(query, values)
                connection.commit()
                print("usuario registrada correctamente.")
                return True

        except Exception as e:
            print("Error al registrar usuario:", e)
            return False

        finally:
            cursor.close()
            connection.close()
    
    def buscar_usuario(self, user):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            query = """
                SELECT id, user
                FROM usuarios
                WHERE user = %s 
            """
            values = (user,)
            cursor.execute(query, values)
            result = cursor.fetchone()

            if result:
                return result
            else:
                return False
        
        finally:
            cursor.close()
            connection.close()

    def iniciar_sesion(self, user, password):
        connection = get_connection()
        cursor = connection.cursor()

        try:
            query = "SELECT id FROM usuarios WHERE LOWER (user) = LOWER(%s) AND password = %s"
            values = (user, password)
            cursor.execute(query, values)
            result = cursor.fetchone()

            if result:
                print("Inicio de sesión exitoso.")
                return True
            else:
                print("Usuario o contraseña incorrectos.")
                return False

        except Exception as e:
            print("Error al iniciar sesión:", e)
            return False

        finally:
            cursor.close()
            connection.close()

if __name__ == "__main__":
    usr = usuario()
    usr.registrar_usuario("Carlo","password")
