from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .config import get_settings

settings = get_settings()

# Detecta se é Postgres para configurar pool adequadamente
is_postgres = "postgresql" in settings.database_url.lower()

# Configurações do engine
engine_kwargs = {
    "pool_pre_ping": True,  # Verify connections before using
    "echo": False  # Log SQL queries (disable in production)
}

# Configurações específicas para Postgres
if is_postgres:
    engine_kwargs.update({
        "pool_size": 5,
        "max_overflow": 10,
        "pool_recycle": 3600,  # Recycle connections after 1 hour
    })

# Create SQLAlchemy engine
engine = create_engine(
    settings.database_url,
    **engine_kwargs
)

# Create SessionLocal class
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create Base class for models
Base = declarative_base()


def get_db():
    """
    Dependency to get database session.
    Usage in FastAPI routes:
        @app.get("/items")
        def read_items(db: Session = Depends(get_db)):
            ...
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
