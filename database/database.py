# Crea la conexión con la base de datos y la sesión para interactuar con ella
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Definimos los parámetros de la conexión a la base de datos
DATABASE_URL = "mysql+mysqlconnector://devuser:devpass@localhost:3306/tasks"

# Con create_engine nos conectamos a la base de datos
engine = create_engine(DATABASE_URL)

# Una instancia de SessionLocal es lo que se usa para las conexiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Esto se usa para después crear la conexión entre el ORM y las tablas físicas
Base = declarative_base()


# Este método es el que abre una sesión con la bd y la cierra cuando finaliza
def get_database_session():
    try:
        db = SessionLocal()
        # Se usa yield en lugar de return para que cuando acabe vuelva al método
        yield db
    finally:
        db.close()
