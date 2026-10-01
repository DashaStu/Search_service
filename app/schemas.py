from pydantic import BaseModel, Field
from datetime import datetime
from typing import List


class SDocumentBase(BaseModel):
    rubric: List[str] = Field(..., description="List of rubrics associated with the document")
    text: str = Field(..., description="The text content of the document")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Timestamp when the document was created")


class SDocumentCreate(SDocumentBase):
    pass


class SDocument(SDocumentBase):
    id: int = Field(..., description="Unique identifier for the document")

    class Config:
        from_attributes = True


        
