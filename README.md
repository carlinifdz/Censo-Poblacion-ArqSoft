#  Censo de Población – Arquitectura de Software

Proyecto desarrollado en **Python** con enfoque **MVC (Modelo–Vista–Controlador)** y base de datos **MySQL**, que permite **registrar, consultar y administrar habitantes y domicilios**.  
Incluye una interfaz gráfica construida con **Tkinter** y un script SQL de ejemplo (`inegi_prueba.sql`) para generar la base de datos.

---

##  Estructura del proyecto
Censo-Poblacion-ArqSoft/
├── database/ # Contiene scripts SQL y configuraciones de la base de datos
├── registro/ # Clases y controladores (modelo y lógica del CRUD)
├── interfaz.py # Interfaz gráfica principal (vista y navegación)
├── instrucciones.txt # Notas o pasos complementarios
└── README.md
---
##  Funcionalidades principales

- Registro de **habitantes** y sus **domicilios**.  
- Búsqueda y filtrado por **ciudad**.  
- Validación de domicilios existentes antes de crear nuevos registros.  
- Interfaz gráfica de usuario (GUI) intuitiva.  
- Operaciones CRUD (crear, leer, actualizar y eliminar).  

---

##  Requisitos del sistema

- **Python 3.10+**
- **MySQL** o **MariaDB**
- Librerías recomendadas:
  ```bash
  pip install mysql-connector-python

  Instalación y ejecución

Clonar el repositorio:

git clone https://github.com/carlinifdz/Censo-Poblacion-ArqSoft.git
cd Censo-Poblacion-ArqSoft


Crear la base de datos:

Abre MySQL y ejecuta:

CREATE DATABASE censo_db CHARACTER SET utf8mb4;


Luego importa el archivo SQL:

mysql -u tu_usuario -p censo_db < database/inegi_prueba.sql


Configurar la conexión a la base de datos:
Si existe un archivo config.py o sección de conexión en el código, ajusta los datos:

DB = {
    "host": "localhost",
    "user": "root",
    "password": "tu_contraseña",
    "database": "censo_db"
}


Ejecutar la aplicación:

python interfaz.py

 Uso básico

Inicia la aplicación.

En el menú principal selecciona:

Registrar habitante: ingresa datos personales y dirección.

Buscar por ciudad: muestra habitantes de una localidad específica.

Editar o eliminar: modifica o borra registros existentes.

Guarda los cambios y verifica los datos en la base de datos.


