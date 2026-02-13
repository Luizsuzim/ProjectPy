import sqlite3

def conectar():
    conn = sqlite3.connect("database.db")
    conn.execute("PRAGMA foreign_keys = ON")
    return conn

def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS clientes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nome TEXT NOT NULL,
            telefone TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS atendimentos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente_id INTEGER NOT NULL,
            descricao TEXT NOT NULL,
            status TEXT NOT NULL,
            FOREIGN KEY (cliente_id) REFERENCES clientes (id)
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            email TEXT UNIQUE NOT NULL,
            senha TEXT NOT NULL
        )
    """)

    conexao.commit()
    conexao.close()


def inserir_cliente(nome, telefone):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO clientes (nome, telefone) VALUES (?, ?)",
        (nome, telefone)
    )

    conexao.commit()
    conexao.close()


def listar_clientes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT id, nome, telefone FROM clientes")
    clientes = cursor.fetchall()

    conexao.close()
    return clientes


def inserir_atendimento(cliente_id, descricao):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO atendimentos (cliente_id, descricao, status) VALUES (?, ?, ?)",
        (cliente_id, descricao, "Aberto")
    )

    conexao.commit()
    conexao.close()


def listar_atendimentos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("""
        SELECT atendimentos.id, clientes.nome, atendimentos.descricao, atendimentos.status
        FROM atendimentos
        JOIN clientes ON clientes.id = atendimentos.cliente_id
    """)

    dados = cursor.fetchall()
    conexao.close()
    return dados


def finalizar_atendimento(atendimento_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE atendimentos SET status = 'Finalizado' WHERE id = ?",
        (atendimento_id,)
    )

    conexao.commit()
    conexao.close()


def criar_usuario(email, senha_hash):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "INSERT INTO usuarios (email, senha) VALUES (?, ?)",
        (email, senha_hash)
    )

    conexao.commit()
    conexao.close()


def buscar_usuario(email):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "SELECT id, email, senha FROM usuarios WHERE email = ?",
        (email,)
    )

    usuario = cursor.fetchone()
    conexao.close()
    return usuario

def existe_usuario():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute("SELECT COUNT(*) FROM usuarios")
    total = cursor.fetchone()[0]

    conexao.close()
    return total > 0
def atualizar_cliente(cliente_id, nome, telefone):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "UPDATE clientes SET nome = ?, telefone = ? WHERE id = ?",
        (nome, telefone, cliente_id)
    )

    conexao.commit()
    conexao.close()


def excluir_cliente(cliente_id):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        "DELETE FROM clientes WHERE id = ?",
        (cliente_id,)
    )

    conexao.commit()
    conexao.close()
