import sqlite3

def conectar():
    return sqlite3.connect('database.db')
def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS clientes (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                   nome TEXT NOT NULL,
                   telefone TEXT NOT NULL,
                   email TEXT NOT NULL)""")
    
    cursor.execute("""CREATE TABLE IF NOT EXISTS atendimentos (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                   cliente_id INTEGER NOT NULL,
                   data TEXT NOT NULL,
                   descricao TEXT NOT NULL,
                   status TEXT NOT NULL,
                   FOREIGN KEY (cliente_id) REFERENCES clientes (id))""")
    conexao.commit()
    conexao.close()