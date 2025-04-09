# auth.py
from database import conectar

def autenticar_usuario(usuario, senha):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        SELECT * FROM usuarios 
        WHERE usuario = %s AND senha = %s
    """, (usuario, senha))
    resultado = cursor.fetchone()
    conn.close()
    return resultado is not None
