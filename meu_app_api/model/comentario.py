from sqlalchemy import Column, String, Integer, DateTime, ForeignKey
from datetime import datetime
from typing import Union

from  model import Base


class Comentario(Base):
    __tablename__ = 'comentário'

    id = Column(Integer, primary_key=True)
    texto = Column(String(4000))
    data_insercao = Column(DateTime, default=datetime.now())

    # Definir o relacionamento entre o comentário e o personagem.
    # Em seguida, definir a coluna 'personagem', a qual irá guardar a referêrncia ao personagem, a chave estrangeira que relaciona um personagem ao comentário.
    personagem = Column(Integer, ForeignKey("personagem.pk_personagem"), nullable=False)

    def __init__(self, texto:str, data_insercao:Union[DateTime, None] = None):
        """
        Cria um Comentário

        Arguments:
            texto: o texto de um comentário.
            data_insercao: data de quando o comentário foi feito ou inserido
                           à base
        """
        self.texto = texto
        if data_insercao:
            self.data_insercao = data_insercao
