import sqlite3
import hashlib
import random
import math

# usuarios = [
#     ("Alejandro García", "alejandro.garcia@example.com", "12345"),
#     ("María López", "maria.lopez@example.com", "12345"),
#     ("Carlos Fernández", "carlos.fernandez@example.com", "12345"),
#     ("Laura González", "laura.gonzalez@example.com", "12345"),
#     ("Pablo Sánchez", "pablo.sanchez@example.com", "12345"),
#     ("Carmen Rodríguez", "carmen.rodriguez@example.com", "12345"),
#     ("Javier Martínez", "javier.martinez@example.com", "12345"),
#     ("Ana Gómez", "ana.gomez@example.com", "12345"),
#     ("David Ruiz", "david.ruiz@example.com", "12345"),
#     ("Lucía Díaz", "lucia.diaz@example.com", "12345"),
#     ("Sergio Hernández", "sergio.hernandez@example.com", "12345"),
#     ("Marta Morales", "marta.morales@example.com", "12345"),
#     ("Andrés Ortiz", "andres.ortiz@example.com", "12345"),
#     ("Clara Jiménez", "clara.jimenez@example.com", "12345"),
#     ("Raúl Navarro", "raul.navarro@example.com", "12345"),
#     ("Irene Muñoz", "irene.munoz@example.com", "12345"),
#     ("Daniel Romero", "daniel.romero@example.com", "12345"),
#     ("Sofía Torres", "sofia.torres@example.com", "12345"),
#     ("Juan Ramírez", "juan.ramirez@example.com", "12345"),
#     ("Beatriz Serrano", "beatriz.serrano@example.com", "12345")
# ]
#valoraciones = generar_valoraciones(1000, (1, 20), (20, 1610))    
# Insertar las valoraciones en la base de datos

def ConectarDB():
    return sqlite3.connect("peliculas.db")
def CrearDB():
    conn = ConectarDB()
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Usuario (
        ID INTEGER PRIMARY KEY,
        nombre CHAR(255),
        email CHAR(255),
        hash_pass CHAR(512)
    )
    """)

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Valoraciones (
        ID INTEGER PRIMARY KEY,
        Pelicula_ID INTEGER,
        Usuario_ID INTEGER,
        Valoracion INTEGER NOT NULL,
        FOREIGN KEY (Pelicula_ID) REFERENCES Pelicula(ID),
        FOREIGN KEY (Usuario_ID) REFERENCES Usuario(ID)
    )
    """)

    # Confirmar los cambios y cerrar la conexión
    conn.commit()
    conn.close()

    print("Base de datos creada con éxito.")
def leer_peliculas():
    conn = ConectarDB()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM peliculas;")
    datos = cursor.fetchall()
    [print(dato) for dato in datos]
    return datos
def generar_valoraciones(cantidad, usuarios_rango, peliculas_rango):
    valoraciones = []
    for _ in range(cantidad):
        usuario_id = random.randint(*usuarios_rango)
        pelicula_id = random.randint(*peliculas_rango)
        valoracion = random.randint(1, 10)
        valoraciones.append((usuario_id, pelicula_id, valoracion))
    return valoraciones
def insertar_usuarios_en_db(usuarios):
    conn = ConectarDB()
    cursor = conn.cursor()
    
    for nombre, email, contraseña in usuarios:
        # Calcular el hash de la contraseña
        hash_pass = hashlib.sha256(contraseña.encode('utf-8')).hexdigest()
        
        # Insertar en la base de datos
        cursor.execute("""
        INSERT INTO Usuario (nombre, email, hash_pass) VALUES (?, ?, ?)
        """, (nombre, email, hash_pass))
    
    conn.commit()
    conn.close()
    print(f"{len(usuarios)} usuarios insertados con éxito.")
def insertar_valoraciones_en_db(valoraciones):
    conn = ConectarDB()  # Cambia a tu archivo de base de datos
    cursor = conn.cursor()
        
    # Insertar valoraciones
    for usuario_id, pelicula_id, valoracion in valoraciones:
        cursor.execute("""
        INSERT INTO Valoraciones (Usuario_ID, Pelicula_ID, Valoracion)
        VALUES (?, ?, ?)
        """, (usuario_id, pelicula_id, valoracion))
    
    conn.commit()
    conn.close()
    print(f"{len(valoraciones)} valoraciones insertadas exitosamente.")
def insertar_valoracion(usuario,pelicula,valoracion):

    conn = ConectarDB()  # Cambia a tu archivo de base de datos
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Valoraciones (Usuario_ID, Pelicula_ID, Valoracion)
        VALUES (?, ?, ?)
        """, (usuario_id, pelicula_id, valoracion))
    conn.commit()
    conn.close()
def devolver_num_peliculas():
    conn = ConectarDB()
    cursor = conn.cursor()
    cursor.execute("SELECT ID FROM peliculas;")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    return len(datos)
def devolver_num_usrs():
    conn = ConectarDB()
    cursor = conn.cursor()
    cursor.execute("SELECT ID FROM Usuario;")
    datos = cursor.fetchall()
    cursor.close()
    conn.close()
    return len(datos)
def devolver_valoraciones_matriz():
    conn = ConectarDB()
    cursor = conn.cursor()
    cursor.execute("SELECT Usuario_ID, Pelicula_ID, Valoracion FROM Valoraciones;")
    datos = cursor.fetchall()
    matriz = [[0] * devolver_num_peliculas() for _ in range(devolver_num_usrs())]
    for dato in datos:
        usuario_id, pelicula_id, valoracion = dato
        matriz[usuario_id-1][pelicula_id-1] = valoracion
    for fila in matriz:
        print(fila)
    return matriz

print(devolver_num_usrs())
print(devolver_num_peliculas())
devolver_valoraciones_matriz()