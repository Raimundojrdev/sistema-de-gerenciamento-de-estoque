import sqlite3

def conectar():
    return sqlite3.connect('estoque.db')


def criar_tabelas():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS produtos (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        valor REAL NOT NULL
    )
    ''')
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS movimentacoes (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        produto_id INTEGER NOT NULL,
        tipo TEXT NOT NULL,
        quantidade INTEGER NOT NULL,
        data TEXT DEFAULT CURRENT_DATE,
        FOREIGN KEY(produto_id) REFERENCES produtos(id)
        )
    ''')





    conexao.commit()
    conexao.close()

    print('Banco de dados criado com sucesso!')

