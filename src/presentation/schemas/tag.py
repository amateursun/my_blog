# src/presentation/schemas/tag.py
from pydantic import BaseModel, ConfigDict


class TagOut(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class TagCreate(BaseModel):
    name: str

