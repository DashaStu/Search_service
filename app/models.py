from sqlalchemy import Column, Integer, String, DateTime, ARRAY
from app.database import Base


class Document(Base):
    __tablename__ = 'documents'

    id = Column(Integer, primary_key=True)
    rubric = Column(ARRAY(String), nullable=False)
    text = Column(String, nullable=False)
    created_at = Column(DateTime, nullable=False)