from sqlalchemy_utils import database_exists, create_database
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
import os

# Importar elementos definidos no modelo
from model.base import Base
from model.comentario import Comentario
from model.personagem import Personagem # ALTERAR AQUI!!!!!!!!!!!

db_path = "database/"
# Verificar se o diretorio não existe
if not os.path.exists(db_path):
   # caso ele não exista, criar o diretorio
   os.makedirs(db_path)

# URL de acesso ao banco (essa é uma url de acesso ao sqlite local)
db_url = 'sqlite:///%s/db.sqlite3' % db_path

# Criar a engine de conexão com o banco
engine = create_engine(db_url, echo=False)

# Instanciar um criador de seção com o banco
Session = sessionmaker(bind=engine)

# Criar o banco se ele não existir 
if not database_exists(engine.url):
    create_database(engine.url) 

# Criar as tabelas do banco, caso não existam
Base.metadata.create_all(engine)
