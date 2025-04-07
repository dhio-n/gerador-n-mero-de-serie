import sqlite3

def conectar():
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
            numero_serie TEXT,
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

def consultar_serie(codigo_produto):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT numero_serie, data_geracao FROM series WHERE codigo_produto = ?", (codigo_produto,))
    result = cursor.fetchone()
    conn.close()
    return result
