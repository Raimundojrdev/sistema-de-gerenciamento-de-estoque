import sqlite3

def conectar():
    return sqlite3.connect('estoque.db')



conexao = sqlite3.connect('estoque.db')
cursor = conexao.cursor()

cursor.execute('''
CREATE TABLE IF NOT EXISTS produtos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    nome TEXT NOT NULL,
    quantidade INTEGER NOT NULL,
    valor REAL NOT NULL
)
''')

conexao.commit()
conexao.close()

print('Banco de dados criado com sucesso!')