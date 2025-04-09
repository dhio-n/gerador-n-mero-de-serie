import sqlite3
from datetime import datetime

def conectar():
    os.makedirs("data", exist_ok=True)  # Garante que a pasta existe
    return sqlite3.connect("data/produtos.db")

def criar_tabelas():
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS produtos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo TEXT UNIQUE,
            nome TEXT,
            descricao TEXT
        )
    """)
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS series (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            codigo_produto TEXT,
            numero_serie TEXT UNIQUE,
            data_geracao TEXT,
            FOREIGN KEY (codigo_produto) REFERENCES produtos(codigo)
        )
    """)
    conn.commit()
    conn.close()

def buscar_produto(codigo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE codigo = ?", (codigo,))
    produto = cursor.fetchone()
    conn.close()
    return produto

def cadastrar_produto(codigo, nome, descricao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO produtos (codigo, nome, descricao) VALUES (?, ?, ?)", (codigo, nome, descricao))
    conn.commit()
    conn.close()

def salvar_serie(codigo_produto, numero_serie, data_geracao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO series (codigo_produto, numero_serie, data_geracao) VALUES (?, ?, ?)", 
                   (codigo_produto, numero_serie, data_geracao))
    conn.commit()
    conn.close()

def consultar_series(codigo_produto, data_inicio=None, data_fim=None, numero_serie=None):
    conn = conectar()
    cursor = conn.cursor()

    query = "SELECT numero_serie, data_geracao FROM series WHERE codigo_produto = ?"
    params = [codigo_produto]

    if data_inicio:
        query += " AND data_geracao >= ?"
        params.append(data_inicio)

    if data_fim:
        query += " AND data_geracao <= ?"
        params.append(data_fim)

    if numero_serie:
        query += " AND numero_serie LIKE ?"
        params.append(f"%{numero_serie}%")

    query += " ORDER BY data_geracao DESC"

    cursor.execute(query, tuple(params))
    resultados = cursor.fetchall()
    conn.close()
    return resultados
