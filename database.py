import psycopg2
from psycopg2.extras import RealDictCursor
from datetime import datetime
import os

# Pega a URL do banco via variável de ambiente (deve estar no formato PostgreSQL)
SUPABASE_URL = os.environ["SUPABASE_URL"]

# Função de conexão com cursor que retorna dicionários
def conectar():
    return psycopg2.connect(SUPABASE_URL, cursor_factory=RealDictCursor)

# Busca produto pelo código
def buscar_produto(codigo):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM produtos WHERE codigo = %s", (codigo,))
    produto = cursor.fetchone()
    conn.close()
    return produto

# Cadastra um novo produto
def cadastrar_produto(codigo, nome, descricao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO produtos (codigo, nome, descricao)
        VALUES (%s, %s, %s)
        ON CONFLICT (codigo) DO NOTHING
    """, (codigo, nome, descricao))  # Evita erro caso o produto já exista
    conn.commit()
    conn.close()

# Salva uma nova série vinculada ao produto
def salvar_serie(codigo_produto, numero_serie, data_geracao):
    conn = conectar()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO series (codigo_produto, numero_serie, data_geracao)
        VALUES (%s, %s, %s)
        ON CONFLICT (numero_serie) DO NOTHING
    """, (codigo_produto, numero_serie, data_geracao))  # Evita erro duplicado
    conn.commit()
    conn.close()

# Consulta séries com filtros opcionais
def consultar_series(codigo_produto, data_inicio=None, data_fim=None, numero_serie=None):
    conn = conectar()
    cursor = conn.cursor()

    query = "SELECT numero_serie, data_geracao FROM series WHERE codigo_produto = %s"
    params = [codigo_produto]

    if data_inicio:
        query += " AND data_geracao >= %s"
        params.append(data_inicio)

    if data_fim:
        query += " AND data_geracao <= %s"
        params.append(data_fim)

    if numero_serie:
        query += " AND numero_serie ILIKE %s"
        params.append(f"%{numero_serie}%")

    query += " ORDER BY data_geracao DESC"

    cursor.execute(query, tuple(params))
    resultados = cursor.fetchall()
    conn.close()
    return resultados
