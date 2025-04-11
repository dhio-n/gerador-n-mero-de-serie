# 🛠️ Documentação Técnica - Sistema de Geração e Impressão de Etiquetas

## 📌 Visão Geral

Este projeto é um sistema completo para:

- Cadastro de produtos
- Geração automática de números de série
- Criação de etiquetas com código de barras em PDF
- Reimpressão de etiquetas
- Filtros de busca e paginação

Tecnologias utilizadas:

- `Python`
- `Streamlit` (interface)
- `FPDF` (geração de PDFs)
- `python-barcode` (códigos de barras)
- `PostgreSQL` via `Supabase` (banco de dados)
- `Psycopg2` (acesso ao banco)

---

## 🧩 Estrutura dos Arquivos

### `auth.py` - 🔐 Autenticação

```python
def autenticar_usuario(usuario, senha):
    # Verifica se usuário existe e senha está correta
```

- Consulta segura ao banco (evita SQL injection)
- Autenticação básica com usuário e senha

---

### `database.py` - 📦 Conexão com Banco

Funções principais:

- `conectar()` → conecta ao banco Supabase
- `cadastrar_produto()` → insere novo produto
- `buscar_produto(codigo)` → retorna dados de um produto
- `salvar_serie()` → salva número de série
- `consultar_series()` → busca séries com filtros (data, série, produto, etc.)

---

### `serial_generator.py` - 🔢 Geração de Número de Série

```python
def gerar_numero_serie(codigo_produto):
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    unique_id = uuid.uuid4().hex[:6].upper()
    return f"{codigo_produto}-{timestamp}-{unique_id}"
```

- Gera um identificador único
- Formato: `CODIGO-YYYYMMDDHHMMSS-ID`

---

### `etiqueta.py` - 🖨️ Geração de Etiquetas em PDF

Funções:

#### `gerar_etiqueta_pdf(produto, lista_series, tamanho='Pequena')`

- Cria várias etiquetas por lote
- Suporta 3 tamanhos: Pequena, Média e Grande
- Cada etiqueta inclui:
  - Logo
  - Nome do produto
  - Código do produto
  - Número de série
  - Código de barras (Code128)

#### `reimprimir_etiqueta_individual(produto, numero_serie, tamanho='Pequena')`

- Gera PDF com **uma única etiqueta** específica para reimpressão

#### `gerar_codigo_barras(numero_serie)`

- Cria uma imagem de código de barras temporária com base no número de série

---

## 🧱 Estrutura do Banco de Dados

### Tabela `usuarios`

| Campo   | Tipo |
|---------|------|
| usuario | TEXT |
| senha   | TEXT |

### Tabela `produtos`

| Campo     | Tipo |
|-----------|------|
| codigo    | TEXT |
| nome      | TEXT |
| descricao | TEXT |

### Tabela `series`

| Campo         | Tipo      |
|---------------|-----------|
| numero_serie  | TEXT      |
| codigo_produto| TEXT      |
| data_geracao  | TIMESTAMP |

---

## ✅ Funcionalidades

- ✅ Login com autenticação
- ✅ Cadastro de produtos
- ✅ Geração de número de série exclusivo
- ✅ Impressão de etiquetas em PDF (com código de barras)
- ✅ Agrupamento de etiquetas por lote
- ✅ Reimpressão de etiquetas individuais
- ✅ Filtro por data, série e produto
- ✅ Paginação (limite de 50 séries por página)

---

## 🔒 Segurança

- Variáveis de ambiente para conexão segura
- SQL seguro com parâmetros
- Arquivos temporários tratados com `os.path.exists`
- Uso do diretório `/tmp` para compatibilidade multiplataforma

---

## 💡 Melhorias Futuras

- 🔐 Hash de senha (ex: `bcrypt`)
- 📊 Painel com estatísticas
- 📤 Exportar dados para CSV
- 🔁 Suporte a QR Codes
- 🧾 Integração com sistema de estoque/ERP

---

## 🚀 Como Usar

1. Inicie com `streamlit run app.py`
2. Faça login
3. Cadastre um novo produto
4. Gere números de série
5. Imprima as etiquetas (PDF)
6. Filtre e reimprima quando necessário

---

## 🧪 Instalação

Instale os pacotes com:

```bash
pip install streamlit fpdf python-barcode psycopg2
```

---

## 👨‍💻 Autor

Desenvolvido por **Dhionatan Pereira Barbosa**, como parte do projeto de produção e identificação dos compressores na Mundial Refrigeração focado em **automação e usabilidade**, software solicitado por **Rafael Loredo**, hospedado em https://github.com/dhio-n/gerador-n-mero-de-serie. 

