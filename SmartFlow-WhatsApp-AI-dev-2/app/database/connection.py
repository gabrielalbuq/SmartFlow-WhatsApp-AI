#Exclusivo para fazer a conexão com o BD

import os
from pathlib import Path

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

#Carrega diretamente os arquivos da pasta ambientevirtual
load_dotenv()

database_url = os.getenv("DATABASE_URL")

if database_url == "sqlite:///smartflow.db":
    project_root = Path(__file__).resolve().parents[2]
    interface_db = project_root / "interface" / "instance" / "smartflow.db"
    if interface_db.exists():
        database_url = f"sqlite:///{interface_db.as_posix()}"

engine = create_engine(
    database_url, 
    echo=False, 
    pool_size=10, 
    max_overflow=20, 
    pool_timeout=120, 
    pool_recycle=1800
    )

SessinLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def init_db():
    return SessinLocal()
