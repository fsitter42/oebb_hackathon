import sqlite3
import os

DB_PATH = "audit_log.db"

def init_db():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    # Tabelle erstellen, falls sie nicht existiert
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS uploads (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            filename TEXT,
            phash TEXT UNIQUE,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    conn.close()

def check_and_store_hash(filename, phash):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    
    # Prüfen, ob der Hash schon existiert
    cursor.execute("SELECT filename FROM uploads WHERE phash = ?", (phash,))
    result = cursor.fetchone()
    
    if result:
        conn.close()
        return False, result[0]  # Duplikat gefunden!
    
    # Wenn neu, dann speichern
    cursor.execute("INSERT INTO uploads (filename, phash) VALUES (?, ?)", (filename, phash))
    conn.commit()
    conn.close()
    return True, None  # Alles okay, neu gespeichert