from database import conectar

def entrada_estoque(id_produto, quantidade):
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute(
        'SELECT quantidade FROM produtos WHERE id = ?',
        (id_produto,)
    )
    produto = cursor.fetchone()

    nova_quantidade = produto[0] + quantidade

    cursor.execute(
        'UPDATE produtos SET quantidade = ? WHERE id = ?',
        (nova_quantidade, id_produto)
    )

    cursor.execute(
        '''
        INSERT INTO movimentacoes (produto_id, tipo, quantidade)
        VALUES (?, ?, ?)
        ''',
        (id_produto, 'entrada', quantidade)   
    )

    conexao.commit()
    conexao.close()


def saida_estoque(id_produto, quantidade):
    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute(
        'SELECT quantidade FROM produtos WHERE id = ?',
        (id_produto,)
    )

    produto = cursor.fetchone()

    if quantidade > produto[0]:
        print('Estoque insuficiente!')
        conexao.close()
        return
    
    nova_quantidade = produto[0] - quantidade

    cursor.execute(
        'UPDATE produtos SET quantidade = ? WHERE id = ?',
        (nova_quantidade, id_produto)
    )

    cursor.execute('''
    INSERT INTO movimentacoes (produto_id, tipo, quantidade)
    VALUES (?, ?, ?)
    ''', (id_produto, 'saida', quantidade)
    )
    conexao.commit()
    conexao.close()


def listar_movimentacoes():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM movimentacoes')

    movimentacoes = cursor.fetchall()

    movimentacoes_formatadas = []

    for movimentacao in movimentacoes:
        movimentacoes_formatadas.append({
            'id': movimentacao[0],
            'produto_id':movimentacao[1],
            'tipo': movimentacao[2],
            'quantidade': movimentacao[3],
            'data': movimentacao[4]
        })

    conexao.close()

    return movimentacoes_formatadas


    