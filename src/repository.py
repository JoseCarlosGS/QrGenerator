import sqlite3

def crear_tabla_metadatos(conexion):
    """
    Crear tabla para almacenar datos en la base de datos

        Args:
            conexion (connection): Conexion a la base de datos
    """
    cursor = conexion.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS qr_metadata (
            id TEXT PRIMARY KEY,
            url TEXT NOT NULL,
            author TEXT,
            created_at TEXT,
            description TEXT
        )
    """)
    conexion.commit()
    
def guardar_metadatos(conexion, qr_id, url, author, created_at, description):
    """
    Guardar metadatos en la tabla previamente creada

        Args:
            conexion (connection): Conexion a la base de datos
            qr_id (str): Id del QR generado
            url (str): Url almacenada en el qr
            author (str): Autor del QR
            created_at (str): Timestamp de la creacion del QR
            description (str): Descripcion adicional para el QR
    """
    try:
        cursor = conexion.cursor()
        cursor.execute("""
            INSERT INTO qr_metadata (id, url, author, created_at, description)
            VALUES (?, ?, ?, ?, ?)
        """, (qr_id, url, author, created_at, description))
        conexion.commit()
    except Exception:
        print("Error al guardar")