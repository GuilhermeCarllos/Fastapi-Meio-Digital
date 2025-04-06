from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
import time
from sqlalchemy.exc import OperationalError

# A URL de conexão usa o nome do serviço 'db' do Docker Compose
SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://postgres:2024@db:5432/cursosdb")

# Função para criar o engine com retry
def create_engine_with_retry(url, max_retries=5, retry_delay=5):
    for attempt in range(max_retries):
        try:
            engine = create_engine(url)
            connection = engine.connect()
            connection.close()
            print("Conexão com o banco de dados estabelecida com sucesso!")
            return engine
        except OperationalError as e:
            print(f"Tentativa {attempt + 1} falhou: {e}")
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                raise Exception("Não foi possível conectar ao banco de dados após várias tentativas.")

# Cria o engine com retry
engine = create_engine_with_retry(SQLALCHEMY_DATABASE_URL)

# Cria a fábrica de sessões para o SQLAlchemy
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Define a base para os modelos
Base = declarative_base()

# Função que fornece uma sessão de banco de dados
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()