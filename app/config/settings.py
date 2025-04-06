import os
from dotenv import load_dotenv

# Carrega as variáveis de ambiente do arquivo .env
load_dotenv()

# Configuração da URL do banco de dados
DATABASE_URL = os.getenv("postgresql://postgres:2024@localhost:5432/cursosdb")

