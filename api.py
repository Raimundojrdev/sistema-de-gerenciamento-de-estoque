from fastapi import FastAPI
from pydantic import BaseModel, Field, field_validator
from produtos import (
    listar_produtos as listar_produtos_db,
    cadastrar_produto as cadastrar_produto_db,
    buscar_produto as buscar_produto_db,
    atualizar_produto as atualizar_produto_db,
    remover_produto as remover_produto_db
)
from movimentacoes import (
    listar_movimentacoes as listar_movimentacoes_db,
    saida_estoque as saida_estoque_db,
    entrada_estoque as entrada_estoque_db
)
    




class Produto(BaseModel):
    id:int
    nome:str
    quantidade:int
    valor:float

class ProdutoCriar(BaseModel):
    nome:str
    quantidade:int = Field(gt=0)
    valor:float = Field(gt=0)


    @field_validator('nome')
    @classmethod
    def validar_nome(cls, nome):
        nome = nome.strip()

        if not nome:
            raise ValueError('O nome do produto não pode ser vazio.')
        return nome

class MovimentacaoCriar(BaseModel):
    id_produto: int
    quantidade: int = Field(g=0)


app = FastAPI()

@app.get('/')
def inicio():
    return{'mensagem': 'API do Sistema de Estoque funcionando!'}


@app.get('/produtos', response_model=list[Produto])
def listar_produtos():
    produtos = listar_produtos_db()
    return produtos


@app.post('/produtos')
def cadastrar_produto(produto: ProdutoCriar):
    id_produto = cadastrar_produto_db(
        produto.nome,
        produto.quantidade,
        produto.valor
    )

    return{'mensagem': 'Produto cadastrado com sucesso!',
           'id': id_produto} 


@app.get('/produtos/{id_produto}', response_model=Produto)
def buscar_produto(id_produto: int):
    produto = buscar_produto_db(id_produto)


    return{
        'id': produto[0],
        'nome': produto[1],
        'quantidade': produto[2],
        'valor': produto[3]
    }


@app.put('/produtos/{id_produto}')
def atualizar_produto(id_produto: int, produto: ProdutoCriar):
    atualizar_produto_db(
        id_produto,
        produto.nome,
        produto.quantidade,
        produto.valor
    )

    return {
        'mensagem': 'Produto atualizado com sucesso!'
    }


@app.delete('/produtos/{id_produto}')
def remover_produto(id_produto: int):
    remover_produto_db(id_produto)

    return{
        'mesagem': 'Produto removido com sucesso!'
    }


@app.get('/movimentacoes')
def listar_movimentacoes():
    movimentacoes = listar_movimentacoes_db()

    return movimentacoes


@app.post('/movimentacoes/entrada')
def registrar_entrada(movimentacao: MovimentacaoCriar):
    entrada_estoque_db(
        movimentacao.id_produto,
        movimentacao.quantidade   
    )

    return{
        'mensagem': 'Entrada de estoque registrada com sucesso!'
    }

@app.post('/movimentacoes/saida')
def registrar_saida(movimentacao: MovimentacaoCriar):
    saida_estoque_db(
        movimentacao.id_produto,
        movimentacao.quantidade
    )
    
    return{
        'mensagem': 'Saida de estoque registrada com sucesso!'
    }