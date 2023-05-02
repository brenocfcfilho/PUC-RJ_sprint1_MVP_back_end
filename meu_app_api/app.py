from flask_openapi3 import OpenAPI, Info, Tag
from flask import redirect
from urllib.parse import unquote

from sqlalchemy.exc import IntegrityError

from model import Session, Personagem, Comentario
from logger import logger
from schemas import *
from flask_cors import CORS

info = Info(title="Minha API", version="1.0.0")
app = OpenAPI(__name__, info=info)
CORS(app)

# Definir tags
home_tag = Tag(name="Documentação", description="Seleção de documentação: Swagger, Redoc ou RapiDoc")
personagem_tag = Tag(name="Personagem", description="Adição, visualização e remoção de personagens da base")
comentario_tag = Tag(name="Comentario", description="Adição de um comentário aos personagens cadastrados na base")


@app.get('/', tags=[home_tag])
def home():
    """Redireciona para /openapi, tela que permite a escolha do estilo de documentação.
    """
    return redirect('/openapi')


@app.post('/personagem', tags=[personagem_tag],
          responses={"200": PersonagemViewSchema, "409": ErrorSchema, "400": ErrorSchema})
def add_personagem(form: PersonagemSchema):
    """Adicionar um novo Personagem à base de dados

    Retorna uma representação dos personagens e comentários associados.
    """
    personagem = Personagem(
        nome=form.nome,
        nivel=form.nivel,
        dinheiro=form.dinheiro)
    logger.debug(f"Adicionando o persoangem à mesa de RPG: '{personagem.nome}'")
    try:
        # Criar conexão com a base
        session = Session()
        # Adicionar personagem
        session.add(personagem)
        # Efetivar o comando de adição de novo item na tabela
        session.commit()
        logger.debug(f"Adicionando o personagem à mesa de RPG: '{personagem.nome}'")
        return apresenta_personagem(personagem), 200

    except IntegrityError as e:
        # Quando a duplicidade do nome é a provável razão do IntegrityError
        error_msg = "Personagem de mesmo nome já salvo na base :/"
        logger.warning(f"Erro ao adicionar o novo Personagem '{personagem.nome}', {error_msg}")
        return {"message": error_msg}, 409

    except Exception as e:
        # Quando ocorrer um erro fora do previsto
        error_msg = "Não foi possível salvar novo persoangem :/"
        logger.warning(f"Erro ao adicionar persoangem '{personagem.nome}', {error_msg}")
        return {"message": error_msg}, 400


@app.get('/personagens', tags=[personagem_tag],
         responses={"200": ListagemPersonagensSchema, "404": ErrorSchema})
def get_personagens():
    """Faz a busca por todos os Personagens cadastrados na mesa de RPG

    Retorna uma representação da listagem de personagens.
    """
    logger.debug(f"Coletando personagens ")
    # Criar conexão com a base
    session = Session()
    # Realizar a busca
    personagens = session.query(Personagem).all()

    if not personagens:
        # Quando não houver personagens cadastrados
        return {"personagens": []}, 200
    else:
        logger.debug(f"%d personagens encontrados" % len(personagens))
        # Retornar a representação do personagem
        print(personagens)
        return apresenta_personagens(personagens), 200


@app.get('/personagem', tags=[personagem_tag],
         responses={"200": PersonagemViewSchema, "404": ErrorSchema})
def get_personagem(query: PersonagemBuscaSchema):
    """Realizar busca por um Personagem a partir do id do Personagem

    Retorna uma representação dos personagens e comentários associados.
    """
    personagem_id = query.id
    logger.debug(f"Coletando dados sobre o personagem #{personagem_id}")
    # Criar conexão com a base
    session = Session()
    # Realziar busca
    personagem = session.query(Personagem).filter(Personagem.id == personagem_id).first()

    if not personagem:
        # Caso o personagem não seja encontrado na base
        error_msg = "Personagem não encontrado na base :/"
        logger.warning(f"Erro ao buscar personagem '{personagem_id}', {error_msg}")
        return {"message": error_msg}, 404
    else:
        logger.debug(f"Persoangem encontrado: '{personagem.nome}'")
        # Retornar a representação de personagem
        return apresenta_personagem(personagem), 200


@app.delete('/personagem', tags=[personagem_tag],
            responses={"200": PersonagemDelSchema, "404": ErrorSchema})
def del_personagem(query: PersonagemBuscaSchema):
    """Deleta um Persoangem a partir do nome do persoangem informado

    Retorna uma mensagem de confirmação da remoção.
    """
    personagem_nome = unquote(unquote(query.nome))
    print(personagem_nome)
    logger.debug(f"Deletando dados sobre persoangem #{personagem_nome}")
    # Criar conexão com a base
    session = Session()
    # Realizar a remoção
    count = session.query(Personagem).filter(Personagem.nome == personagem_nome).delete()
    session.commit()

    if count:
        # Retornar a representação da mensagem de confirmação
        logger.debug(f"Deletado personagem #{personagem_nome}")
        return {"message": "Personagem removido", "id": personagem_nome}
    else:
        # Caso o personagem não foi encontrado
        error_msg = "Personagem não encontrado na base :/"
        logger.warning(f"Erro ao deletar personagem #'{personagem_nome}', {error_msg}")
        return {"message": error_msg}, 404


@app.post('/cometário', tags=[comentario_tag],
          responses={"200": PersonagemViewSchema, "404": ErrorSchema})
def add_comentario(form: ComentarioSchema):
    """Adicionar um novo comentário à um dos personagens cadastrados na base que esteja identificado pelo id

    Retorna uma representação dos personagens e comentários associados.
    """
    personagem_id  = form.personagem_id
    logger.debug(f"Adicionando comentários ao personagem #{personagem_id}")
    # Criar conexão com a base
    session = Session()
    # Realizar a busca pelo personagem
    personagem = session.query(Personagem).filter(Personagem.id == personagem_id).first()

    if not personagem:
        # Caso o personagem não seja encontrado
        error_msg = "Personagem não encontrado na base :/"
        logger.warning(f"Erro ao adicionar comentário ao persoangem '{personagem_id}', {error_msg}")
        return {"message": error_msg}, 404

    # Criar comentário
    texto = form.texto
    comentario = Comentario(texto)

    # Adcionar o comentário ao personagem
    personagem.adiciona_comentario(comentario)
    session.commit()

    logger.debug(f"Adicionado comentário ao personagem #{personagem_id}")

    # retorna a representação de personagem
    return apresenta_personagem(personagem), 200
