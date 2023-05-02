from pydantic import BaseModel
from typing import Optional, List
from model.personagem import Personagem

from schemas import ComentarioSchema


class PersonagemSchema(BaseModel):
    """ Define como um novo personagem a ser inserido deve ser representado
    """
    nome: str = "Bruenor"
    nivel: int = 1
    dinheiro: float = 100.00


class PersonagemBuscaSchema(BaseModel):
    """ Define como deve ser a estrutura que representa a busca. Que será
        feita apenas com base no nome do Personagem.
    """
    nome: str = "Teste"


class ListagemPersonagensSchema(BaseModel):
    """ Define como uma listagem de personagens será retornada.
    """
    personagens:List[PersonagemSchema]


def apresenta_personagens(personagens: List[Personagem]):
    """ Retorna uma representação do Personagem seguindo o schema definido em
        PersonagemViewSchema.
    """
    result = []
    for personagem in personagens:
        result.append({
            "nome": personagem.nome,
            "nível": personagem.nivel,
            "dinheiro": personagem.dinheiro,
        })

    return {"personagens": result}


class PersonagemViewSchema(BaseModel):
    """ Define como um personagem será retornado: personagem + comentários.
    """
    id: int = 1
    nome: str = "Bruenor"
    nivel: int = 1
    dinheiro: float = 100.00
    total_cometarios: int = 1
    comentarios:List[ComentarioSchema]


class PersonagemDelSchema(BaseModel):
    """ Define como deve ser a estrutura do dado retornado após uma requisição
        de remoção.
    """
    message: str
    nome: str

def apresenta_personagem(personagem: Personagem):
    """ Retorna uma representação do personagem seguindo o schema definido em
        PersonagemViewSchema.
    """
    return {
        "id": personagem.id,
        "nome": personagem.nome,
        "nível": personagem.nivel,
        "dinheiro": personagem.dinheiro,
        "total_cometarios": len(personagem.comentarios),
        "comentarios": [{"texto": c.texto} for c in personagem.comentarios]
    }
