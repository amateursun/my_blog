# src/core/entities/tag.py
from dataclasses import dataclass


@dataclass
class Tag:
    id: int | None = None
    name: str = ""