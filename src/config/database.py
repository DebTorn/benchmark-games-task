import os
from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Környezeti változók beállítása
db_host = os.environ.get('DB_HOST')
db_database = os.environ.get('DB_DATABASE')
db_username = os.environ.get('DB_USERNAME')
db_password = os.environ.get('DB_PASSWORD')

# Adatbázis URL
DATABASE_URL = f'mysql://{db_username}:{db_password}@{db_host}/{db_database}'

engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)

Base = declarative_base()

def get_session():
    session = SessionLocal()
    try:
        yield session
    finally:
        session.close()