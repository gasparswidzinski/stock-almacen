import sqlite3
from datetime import datetime

DB_NAME = "almacen.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    # Tabla productos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS productos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nombre TEXT NOT NULL,
        cantidad INTEGER NOT NULL,
        precio REAL NOT NULL
    )
    """)

    # Tabla movimientos
    cur.execute("""
    CREATE TABLE IF NOT EXISTS movimientos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        producto TEXT NOT NULL,
        cambio INTEGER NOT NULL,
        precio REAL NOT NULL,
        fecha TEXT NOT NULL
    )
    """)
    conn.commit()
    conn.close()

def agregar_producto(nombre, cantidad, precio):
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()

    cur.execute("INSERT INTO productos (nombre, cantidad, precio) VALUES (?, ?, ?)",
                (nombre, cantidad, precio))

    cur.execute("INSERT INTO movimientos (producto, cambio, precio, fecha) VALUES (?, ?, ?, ?)",
                (nombre, cantidad, precio, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))

    conn.commit()
    conn.close()

def obtener_productos():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT * FROM productos")
    data = cur.fetchall()
    conn.close()
    return data

def obtener_movimientos():
    conn = sqlite3.connect(DB_NAME)
    cur = conn.cursor()
    cur.execute("SELECT producto, cambio, precio, fecha FROM movimientos ORDER BY id DESC LIMIT 10")
    data = cur.fetchall()
    conn.close()
    return data
