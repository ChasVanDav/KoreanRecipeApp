from sqlalchemy import Column, Integer, String, JSON, ForeignKey, LargeBinary
from sqlalchemy.orm import declarative_base, relationship
from sqlalchemy_utils.types import TSVectorType
from datetime import datetime 
from sqlalchemy import DateTime 

Base = declarative_base()

class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True, autoincrement=True)
    recipe_title = Column(String, unique=True, nullable=False)
    recipe_content = Column(String, nullable=False)
    video_id = Column(String, nullable=True)
    video_url = Column(String, nullable=True)
    video_title = Column(String, nullable=True)
    video_metadata = Column(JSON, nullable=True)

    # Adding the search vector
    search_vector = Column(TSVectorType('recipe_title', 'recipe_content'))
    
    # Relationship with Image model
    images = relationship("Image", back_populates="recipe")


class Image(Base):
    __tablename__ = "images"

    id = Column(Integer, primary_key=True, autoincrement=True)
    filename = Column(String, nullable=False)
    image_data = Column(LargeBinary, nullable=False) 
    upload_date = Column(DateTime, default=datetime.utcnow)
    recipe_id = Column(Integer, ForeignKey("recipe.id"), nullable=False)  # Link to Recipe

    recipe = relationship("Recipe", back_populates="images")  # Relationship to Recipe

