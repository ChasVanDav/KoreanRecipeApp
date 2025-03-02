from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect
from models import Base, Recipe, Image
import os
from dotenv import load_dotenv

load_dotenv()


DATABASE_URL = os.getenv('DATABASE_URL')
# Create the engine
engine = create_engine(DATABASE_URL)

# Create tables
try:
    print("Creating tables...")
    Base.metadata.create_all(engine)
    print("Tables created!")
except Exception as e:
    print(f"An error occurred while creating the tables: {e}")


try:
    inspector = inspect(engine)
    tables = inspector.get_table_names()
    print(f"Tables in the database: {tables}")
except Exception as e:
    print(f"An error occurred while listing the tables: {e}")
