from database import conectar


def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()
    
    cursor.execute('SELECT * FROM produtos')
    
    produtos = cursor.fetchall()

    
    conexao.close()

    produtos_formatados = []
    
    
    
    for produto in produtos:
        produtos_formatados.append({
            'id': produto[0],
            'nome': produto[1],
            'quantidade': produto[2],
            'valor': produto[3]
        })

    return produtos_formatados


def cadastrar_produto(nome, quantidade, valor):
    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute(
    'INSERT INTO produtos (nome, quantidade, valor) VALUES (?, ?, ?)',
    (nome, quantidade, valor)
)

    id_produto = cursor.lastrowid    

    conexao.commit()
    conexao.close()

    return id_produto


def buscar_produto(id_produto):
    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute(
        'SELECT * FROM produtos WHERE id = ?',
        (id_produto,)
    )

    produto = cursor.fetchone()

    conexao.close()

    return produto


def atualizar_produto(id_produto, nome, quantidade, valor):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('''
        UPDATE produtos
        SET nome = ?, quantidade = ?, valor = ?
        WHERE id = ?
        ''',
        (nome, quantidade, valor, id_produto)
    )


    conexao.commit()
    conexao.close()


def remover_produto(id_produto):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        'DELETE FROM produtos WHERE id = ?',
        (id_produto,)
    )

    conexao.commit()
    conexao.close()