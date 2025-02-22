from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

DATABASE_URL = "postgresql://tpl522_6@localhost/postgres"

# Create the engine (connects to PostgreSQL)
engine = create_engine(DATABASE_URL)

# Base class for ORM models
Base = declarative_base()

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
