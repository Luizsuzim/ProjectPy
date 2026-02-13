import sqlite3

def conectar():
    return sqlite3.connect('database.db')
def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS clientes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   telefone TEXT NOT NULL
                   )""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS atendimentos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                   cliente_id INTEGER NOT NULL,
                   descricao TEXT NOT NULL,
                   status TEXT NOT NULL,
                   FOREIGN KEY (cliente_id) REFERENCES clientes (id))""")
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