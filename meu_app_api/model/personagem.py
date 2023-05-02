from sqlalchemy import Column, String, Integer, DateTime, Float
from sqlalchemy.orm import relationship
from datetime import datetime
from typing import Union

from  model import Base, Comentario


class Personagem(Base):
    __tablename__ = 'personagem'

    id = Column("pk_personagem", Integer, primary_key=True)
    nome = Column(String(140), unique=True)
    nivel = Column(Integer)
    dinheiro = Column(Float)
    data_insercao = Column(DateTime, default=datetime.now())

    # Definir o relacionamento entre o personagem e o comentário.
    # Essa relação é implicita, não está salva na tabela 'personagem', o SQLAlchemy é que terá a responsabilidade de reconstruir esse relacionamento.
    comentarios = relationship("Comentario")

    def __init__(self, nome:str, nivel:int, dinheiro:float,
                 data_insercao:Union[DateTime, None] = None):
        """
        Cria um Personagem

        Arguments:
            nome: nome do Personagem.
            nivel: nivel de experiência do personagem
            dinheiro: riquezas que um personagem possui
            data_insercao: data de quando o personagem foi cadastrado à base
        """
        self.nome = nome
        self.nivel = nivel
        self.dinheiro = dinheiro

        # Caso não seja informada, será o data exata da inserção no banco
        if data_insercao:
            self.data_insercao = data_insercao

    def adiciona_comentario(self, comentario:Comentario):
        """ Adiciona um novo comentário ao Personagem
        """
        self.comentarios.append(comentario)

