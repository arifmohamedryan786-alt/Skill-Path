from sqlalchemy import Column, Integer, String
from backend.app.database import Base

class Glossary(Base):
    __tablename__ = "glossary"

    id = Column(Integer, primary_key=True, index=True)
    term = Column(String, unique=True, index=True, nullable=False)
    category = Column(String, index=True, default="General") # "AI", "Web", "Data", "Cloud", "General"
    plain_meaning = Column(String, nullable=False)           # Grade-8 reading level definition
    example = Column(String, default="")

