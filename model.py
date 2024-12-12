import sqlite3

def ConectarDB():
    return sqlite3.connect("peliculas.db")
def CrearDB():

    conn = ConectarDB()

    cursor = conn.cursor()

    # Crear la tabla "Pelicula"
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS Pelicula (
        ID INTEGER PRIMARY KEY,
        title CHAR(50) NOT NULL,
        synopsis CHAR(500) NOT NULL,
        critic_score INTEGER NOT NULL,
        people_score INTEGER NOT NULL,
        concensus CHAR(500) NOT NULL,
        total_review INTEGER NOT NULL,
        total_ratings INTEGER NOT NULL,
        type CHAR(255) NOT NULL,
        rating CHAR(512) NOT NULL,
        genre CHAR(255) NOT NULL,
        original_language CHAR(255),
        director CHAR(255) NOT NULL,
        producer CHAR(255) NOT NULL,
        writer CHAR(255) NOT NULL,
        release_date_theaters DATE,
        box_office_gross_usa INTEGER,
        runtime CHAR(128),
        production_co CHAR(255),
        aspect_ratio CHAR(255),
        view_the_collection CHAR(255),
        crew CHAR(512),
        link CHAR(512)
    )
    """)

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
