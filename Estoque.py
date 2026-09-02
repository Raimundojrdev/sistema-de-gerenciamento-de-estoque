from time import sleep
import sqlite3
from database import conectar

def cadastrar_produto():
    while True:
        while True:
            nome = input('Digite o nome do produto: ').strip()
            
            if nome:
                break
            print('O nome não pode ficar em branco! .')
            
        while True:   
            try:
                quantidade = int(input('Digite a quantidade do produto: '))
                if quantidade > 0:
                    break

                print('A quantidade deve ser maior que zero! ')
                
            except ValueError:
                print('Digite uma quantidade válida! .')
        while True:        
            try:
                valor = float(input('Digite o valor do produto: '))
                if valor > 0:
                    break
                print('O valor deve ser maior que zero! ')
            except ValueError:
                print('Digite um valor válido')

        conexao = conectar()
        cursor = conexao.cursor()


        cursor.execute('''
            INSERT INTO produtos (nome, quantidade, valor)
            VALUES (?, ?, ?)
        ''', ( nome, quantidade, valor))

        conexao.commit()
        conexao.close()

        print('Produto cadastrado com sucesso!')
        if input('Ainda tem produtos para cadastrar? [S/N] ').strip().lower() != 's':
            return


def listar_produtos():
    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('SELECT * FROM produtos')

    produtos = cursor.fetchall()

    conexao.close()

    if not produtos:
        print('Nenhum produto cadastrado.')
        return

    print('\n' + '=-' * 40)
    print('                 PRODUTOS')
    print('=-' * 40)

    for produto in produtos:
        print(f'ID: {produto[0]}')
        print(f'Nome: {produto[1]}')
        print(f'Quantidade: {produto[2]}')
        print(f'Valor: R$ {produto[3]:.2f}')
        print('-' * 50)
        

def buscar_produto():
    try:
        buscar = int(input('Digite o ID do produto: '))
    except ValueError:
        print('Digite um ID válido. ')
        return

    conexao = conectar()
    cursor = conexao.cursor()

    cursor.execute('''
        SELECT id, nome, quantidade, valor
        FROM produtos
        WHERE id = ?
    ''',(buscar,))

    produto = cursor.fetchone()

    conexao.close()

    if produto:
        print(f"produto encontrado! ")
        print('-=' * 40)
        print(f"ID: {produto[0]}")
        print(f"Nome: {produto[1]}")
        print(f"Quantidade: {produto[2]}")
        print(f"Valor: {produto[3]:.2f}")
    else:
        print('produto não encontrado! ')


def editar_produto():
    try:
        id_produto = int(input('Digite o ID do produto que deseja editar: '))
    except ValueError:
        print('Digite um ID válido.')
        return


    conexao = conectar()
    cursor = conexao.cursor()

    #Procura o produto
    cursor.execute('''
        SELECT id, nome, quantidade, valor
        FROM produtos
        WHERE id = ?
    ''', (id_produto,))

    produto = cursor.fetchone()

    if not produto:
        print('Produto não encontrado!')
        conexao.close()
        return

    print('\nProduto encontrado:')
    print(f'ID: {produto[0]}')
    print(f'Nome: {produto[1]}')
    print(f'Quantidade {produto[2]}')
    print(f'Valor: R$ {produto[3]}')

    print('\nDigite os novos dados:')


    novo_nome = input('Novo nome: ').strip()

    try:
        nova_quantidade = int(input('Novo quantidade: '))
        novo_valor = float(input('Novo valor: '))
    except ValueError:
        print('Digite valores válidos.')
        conexao.close()
        return

    cursor.execute('''
    UPDATE produtos
    SET nome = ?, quantidade = ?, valor = ?
    WHERE id = ?
    ''', (novo_nome, nova_quantidade, novo_valor, id_produto))

    conexao.commit()
    conexao.close()

    print('produto atualizado com sucesso!')
    

def remover_produto():
    busca = int(input('Digite o ID do produto que deseja remover: '))

    conexao = conectar()
    cursor = conexao.cursor()


    cursor.execute(
        'SELECT id, nome, quantidade, valor FROM produtos WHERE id = ?',
        (busca,)
    )

    
    produto = cursor.fetchone()

    if produto:
        print('Produto encontrado!')
        print(f'ID: {produto[0]}')
        print(f'Nome: {produto[1]}')
        print(f'Quantidade: {produto[2]}')
        print(f'Valor: {produto[3]}')


    while True:
        confirma = input('Deseja realmente remover? [S/N] ').strip().lower()

        if confirma == 's':
            cursor.execute(
                'DELETE FROM produtos WHERE id = ?',
                (busca,)
            )


            conexao.commit()

            print('Produto removido com sucesso.')
            break

        elif confirma == 'n':
            print('Remoção cancelada.')
            break

        else:
            print('Digite apenas S ou N.')

    else:
        print('Produto não encontrado.')


def menu():
    while True:
        print('=-' * 40)
        print('\n== Sistema de estoque ==')
        print('[1] Cadastrar produto')
        print('[2] Listar produtos')
        print('[3] Buscar produto')
        print('[4] Editar produto')
        print('[5] Remover produto')
        print('[6] Sair')

        try:
            opcao = int(input('Escolha uma opção: '))
            print('-='*40)
        except ValueError:
            print('Digite uma opção numérica válida.')
            continue

        if opcao == 1:
            cadastrar_produto()
        elif opcao == 2:
            listar_produtos()
        elif opcao == 3:
            buscar_produto()
        elif opcao == 4:
            editar_produto()
        elif opcao == 5:
            remover_produto()
        elif opcao == 6:
            print('Saindo! ')
            break
        else:
            print('Opção inválida. Tente novamente.')


if __name__ == '__main__':
    menu()


